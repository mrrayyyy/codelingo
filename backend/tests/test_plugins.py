import asyncio
from uuid import uuid4

import pytest

from app.adapters import OfflineDictionary, OllamaLLM, PiperTTS, ServiceUnavailable, WhisperSTT
from app.config import settings
from app.contracts import Answer, Context, Feedback, UserProfile, Vocab
from app.plugins import DictationPlugin, ReadAloudPlugin, WritingPlugin, word_error_rate


@pytest.mark.parametrize("reference,answer,expected", [
    ("Validate the session.", "validate THE session!", 0),
    ("Validate the session", "Validate session", 1 / 3),
    ("Validate the session", "Validate a session", 1 / 3),
    ("Validate the session", "Validate the old session", 1 / 3),
    ("Validate the session", "", 1),
    ("", "", 0),
    ("Don't retry", "Don’t retry", 0),
])
def test_dictation_edit_distance(reference, answer, expected):
    assert word_error_rate(reference, answer) == pytest.approx(expected)


def word():
    return Vocab(id=str(uuid4()), lemma="validate", part_of_speech="VERB", frequency=3, cefr="B2",
        contexts=[Context(text="Validate the session before retrieving protected resources.", file_path="auth.ts", line_number=1, kind="comment")])


def test_fully_worked_dictation_contract():
    async def run():
        plugin = DictationPlugin()
        exercises = await plugin.generate([word()], UserProfile())
        assert plugin.manifest.services == ["tts"]
        assert exercises[0].answer_key["transcript"].startswith("Validate")
        assert "transcript" not in str(exercises[0].payload)
        grade = await plugin.grade(exercises[0], Answer(text=exercises[0].answer_key["transcript"]))
        assert grade.score == 1
        partial = await plugin.grade(exercises[0], Answer(text="Validate the session"))
        assert 0 < partial.score < 1 and partial.corrections
    asyncio.run(run())


def test_read_aloud_does_not_claim_pronunciation():
    async def run():
        plugin = ReadAloudPlugin()
        exercise = (await plugin.generate([word()], UserProfile()))[0]
        grade = await plugin.grade(exercise, Answer(text=exercise.answer_key["transcript"]))
        assert exercise.plugin_id == "speaking.read-aloud"
        assert "not pronunciation" in grade.explanation
    asyncio.run(run())


def test_writing_adapter_can_be_replaced():
    class TestModel:
        async def grade_writing(self, prompt, answer):
            assert "validate" in prompt
            return Feedback(score=.8, explanation="A clear commit message.")
    async def run():
        plugin = WritingPlugin(TestModel())
        exercise = (await plugin.generate([word()], UserProfile()))[0]
        assert (await plugin.grade(exercise, Answer(text="Validate sessions before accessing resources"))).score == .8
    asyncio.run(run())


def test_missing_services_fail_explicitly(monkeypatch):
    monkeypatch.setattr(settings, "piper_binary", "")
    monkeypatch.setattr(settings, "whisper_url", "")
    monkeypatch.setattr(settings, "ollama_url", "")
    async def run():
        for call in [PiperTTS().synthesize("Validate the session", "en_US"), WhisperSTT().transcribe(b"test", "test.wav"), OllamaLLM().grade_writing("task", "answer")]:
            with pytest.raises(ServiceUnavailable):
                await call
        assert (await OfflineDictionary().lookup("retrieve")).definition
        assert (await OfflineDictionary().lookup("unlistedterm")).definition is None
    asyncio.run(run())


def test_practice_api_keeps_keys_private_and_records_grade(client):
    client.post("/imports/sample")
    exercises = client.post("/practice/reading.context")
    assert exercises.status_code == 200
    exercise = exercises.json()[0]
    assert "answer_key" not in exercise
    word = next(w for w in client.get("/vocab").json() if w["id"] == exercise["vocab_id"])
    body = {"text": word["definition"], "submission_id": str(uuid4())}
    response = client.post(f"/practice/{exercise['id']}/grade", json=body)
    assert response.status_code == 200 and response.json()["score"] == 1
    assert client.post(f"/practice/{exercise['id']}/grade", json=body).json() == response.json()
    assert client.get("/dashboard").json()["skills"]["reading"]["attempts"] == 1
    assert client.post("/practice/listening.dictation").status_code == 503
    assert client.post("/practice/writing.commit").status_code == 503
    assert client.get("/plugins").json()[0]["available"]
