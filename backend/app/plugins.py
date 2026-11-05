"""Independent modules sharing contracts and injectable service adapters."""
from __future__ import annotations

import re
from uuid import uuid4

from .adapters import llm_adapter
from .contracts import Answer, DictationPayload, DictationAnswerKey, Exercise, Feedback, LearningPlugin, LLMAdapter, PluginManifest, Skill, UserProfile, Vocab


def normalized_words(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?|[0-9]+", text.lower().replace("’", "'"))


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Word-level Levenshtein distance / reference length, capped at one."""
    expected, actual = normalized_words(reference), normalized_words(hypothesis)
    if not expected:
        return 0.0 if not actual else 1.0
    row = list(range(len(actual) + 1))
    for i, word in enumerate(expected, 1):
        previous, row = row, [i]
        for j, candidate in enumerate(actual, 1):
            row.append(min(row[-1] + 1, previous[j] + 1, previous[j - 1] + (word != candidate)))
    return min(1.0, row[-1] / len(expected))


class DictationPlugin:
    manifest = PluginManifest(id="listening.dictation", version="1.0.0", title="Listen & write",
                              skills=[Skill.listening], services=["tts"])

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]:
        exercises = []
        seen: set[str] = set()
        for word in vocabulary:
            context = next((c for c in word.contexts if c.kind != "identifier"), None)
            if not context or context.text in seen:
                continue
            seen.add(context.text)
            payload: DictationPayload = {"voice": profile.tts_voice, "audio_available": True}
            key: DictationAnswerKey = {"transcript": context.text}
            exercises.append(Exercise(id=str(uuid4()), plugin_id=self.manifest.id, vocab_id=word.id,
                kind="dictation", prompt="Listen to the sentence from your project. Type what you hear.",
                payload=payload, answer_key=key))
        return exercises[:20]

    async def grade(self, exercise: Exercise, answer: Answer) -> Feedback:
        expected = exercise.answer_key["transcript"]
        score = round(1 - word_error_rate(expected, answer.text), 3)
        return Feedback(score=score, explanation="Word agreement with the original sentence; punctuation and letter case are ignored.",
                        corrections=[] if score == 1 else ["Compare missing, extra, or changed words with the original sentence."], reference=expected)


class ReadingPlugin:
    manifest = PluginManifest(id="reading.context", version="1.0.0", title="Read in context", skills=[Skill.reading], services=[])

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]:
        choices = [w for w in vocabulary if w.definition and any(c.kind != "identifier" for c in w.contexts)]
        results = []
        for i, word in enumerate(choices):
            distractors = list(dict.fromkeys(w.definition for w in choices if w.lemma != word.lemma and w.definition != word.definition))[:3]
            if len(distractors) < 2:
                continue
            options = distractors + [word.definition]
            offset = i % len(options)
            options = options[offset:] + options[:offset]
            context = next(c for c in word.contexts if c.kind != "identifier")
            results.append(Exercise(id=str(uuid4()), plugin_id=self.manifest.id, vocab_id=word.id, kind="word_in_context",
                prompt=f'What does “{word.lemma}” mean in this context?',
                payload={"context": context.text, "options": options, "lemma": word.lemma}, answer_key={"text": word.definition}))
        return results[:20]

    async def grade(self, exercise: Exercise, answer: Answer) -> Feedback:
        expected = exercise.answer_key["text"]
        correct = answer.text.strip() == expected
        return Feedback(score=int(correct), explanation="Correct — connect this meaning to the original context." if correct else "Read the context again and compare the meanings.", reference=expected)


class ReadAloudPlugin(DictationPlugin):
    manifest = PluginManifest(id="speaking.read-aloud", version="1.0.0", title="Read aloud", skills=[Skill.speaking], services=["stt"])

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]:
        exercises = await super().generate(vocabulary, profile)
        for exercise in exercises:
            exercise.kind = "read_aloud"
            exercise.prompt = "Read this sentence aloud, then check the transcript."
            exercise.payload = {"context": exercise.answer_key["transcript"], "metric": "transcript_agreement"}
        return exercises

    async def grade(self, exercise: Exercise, answer: Answer) -> Feedback:
        feedback = await super().grade(exercise, answer)
        feedback.explanation = "Transcript agreement with the original sentence. This measures recognized words, not pronunciation or phoneme accuracy."
        return feedback


class WritingPlugin:
    manifest = PluginManifest(id="writing.commit", version="1.0.0", title="Workplace writing", skills=[Skill.writing], services=["llm"])

    def __init__(self, llm: LLMAdapter | None = None):
        self.llm = llm or llm_adapter()

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]:
        return [Exercise(id=str(uuid4()), plugin_id=self.manifest.id, vocab_id=w.id, kind="commit_rewrite",
            prompt=f'Write a clear commit message about a change to your project using “{w.lemma}”. Include what changed and why.',
            payload={"context": w.contexts[0].text, "target_level": profile.target_level}, answer_key={})
            for w in vocabulary[:20] if w.contexts]

    async def grade(self, exercise: Exercise, answer: Answer) -> Feedback:
        task = exercise.prompt + "\nLearner target level: " + str(exercise.payload.get("target_level", "B1"))
        task += "\nOriginal project context: " + str(exercise.payload.get("context", ""))
        return await self.llm.grade_writing(task, answer.text)


class CodeReviewPlugin(WritingPlugin):
    manifest = PluginManifest(id="workplace.review", version="1.0.0", title="Code review practice", skills=[Skill.workplace], services=["llm"])

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]:
        exercises = await super().generate(vocabulary, profile)
        for exercise in exercises:
            word = next(w for w in vocabulary if w.id == exercise.vocab_id)
            exercise.kind = "code_review_comment"
            exercise.prompt = f'Write a constructive code review comment using “{word.lemma}”. Ask one clear question about the behavior described below.'
        return exercises


registry: dict[str, LearningPlugin] = {p.manifest.id: p for p in [ReadingPlugin(), DictationPlugin(), ReadAloudPlugin(), WritingPlugin(), CodeReviewPlugin()]}
