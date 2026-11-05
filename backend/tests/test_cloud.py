import asyncio
import json
import subprocess
import sys

import httpx
import pytest

from app.adapters import GroqGateway, GroqLLM, GroqSTT, GroqTTS, ServiceUnavailable
from app.config import settings
from app.contracts import Vocab
from app.db import ImportJob, Repo, SessionLocal


def test_web_does_not_import_heavy_nlp():
    command = "import app.main, sys; assert not {'spacy', 'wordfreq', 'tree_sitter', 'numpy'} & sys.modules.keys()"
    subprocess.run([sys.executable, "-c", command], check=True)


def test_cloud_input_archive_and_idempotent_completion(client):
    with SessionLocal.begin() as db:
        repo = Repo(user_id="local-user", name="cloud-example")
        db.add(repo)
        db.flush()
        job = ImportJob(repo_id=repo.id)
        db.add(job)
        db.flush()
        job_id = job.id
    assert client.get(f"/cloud/jobs/{job_id}").json()["source_url"] is None
    archive = settings.spool_dir / f"{job_id}.zip"
    archive.write_bytes(b"source-placeholder-for-transfer-test")
    assert client.get(f"/cloud/jobs/{job_id}/archive").content == b"source-placeholder-for-transfer-test"
    assert not archive.exists()
    assert client.get(f"/cloud/jobs/{job_id}/archive").status_code == 410
    assert client.post(f"/cloud/jobs/{job_id}/progress", json={"progress": 20}).status_code == 200
    result = {"items": [Vocab(id="", lemma="retrieve", part_of_speech="VERB", frequency=4,
                            cefr="B2", definition="Get stored information back.").model_dump()]}
    assert client.post(f"/cloud/jobs/{job_id}/complete", json=result).status_code == 200
    assert client.post(f"/cloud/jobs/{job_id}/complete", json=result).status_code == 200
    assert len(client.get("/vocab").json()) == 1
    assert len(client.get("/review").json()) == 1
    # A delayed heartbeat cannot revert a completed import.
    client.post(f"/cloud/jobs/{job_id}/progress", json={"progress": 40})
    assert client.get(f"/jobs/{job_id}").json()["status"] == "completed"


def test_remote_dispatch_has_only_a_job_id(client, monkeypatch):
    from app import cloud_jobs
    monkeypatch.setattr(settings, "job_mode", "github_actions")
    monkeypatch.setattr(settings, "github_actions_repo", "example/codelingo")
    monkeypatch.setattr(settings, "github_actions_token", "test-private-token")
    observed = []
    class Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, **kwargs):
            observed.append((url, kwargs))
            return httpx.Response(204, request=httpx.Request("POST", url))
    monkeypatch.setattr(cloud_jobs.httpx, "AsyncClient", lambda **kwargs: Client())
    response = client.post("/imports/github", json={"url": "https://github.com/example/atlas"})
    assert response.status_code == 202
    assert observed[0][1]["json"]["inputs"] == {"job_id": response.json()["id"]}
    assert "atlas" not in json.dumps(observed[0][1]["json"])


def test_cloud_modules_do_not_need_local_model_paths(client, monkeypatch):
    for service in ["tts", "stt", "llm"]:
        monkeypatch.setattr(settings, f"{service}_provider", "groq")
    monkeypatch.setattr(settings, "groq_api_key", "")
    modules = client.get("/plugins").json()
    assert all(not p["available"] for p in modules if p["services"])
    monkeypatch.setattr(settings, "groq_api_key", "test-key")
    assert all(p["available"] for p in client.get("/plugins").json())


def test_groq_adapters_with_mock_transport(monkeypatch):
    async def response(self, path, **kwargs):
        if path == "audio/speech":
            assert kwargs["json"]["voice"] == "troy"
            return httpx.Response(200, content=b"RIFF-mocked-audio")
        if path == "audio/transcriptions":
            return httpx.Response(200, json={"text": "Validate the session"})
        schema = kwargs["json"]["response_format"]["json_schema"]
        assert schema["strict"] and not schema["schema"]["additionalProperties"]
        return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps({
            "score": .8, "explanation": "Clear and relevant.", "corrections": [], "reference": None})}}]})
    monkeypatch.setattr(GroqGateway, "request", response)
    async def run():
        assert (await GroqTTS().synthesize("Validate the session", "en_US")).startswith(b"RIFF")
        assert await GroqSTT().transcribe(b"audio", "audio.webm") == "Validate the session"
        assert (await GroqLLM().grade_writing("Write a commit", "Validate sessions")).score == .8
    asyncio.run(run())


def test_groq_quota_error_does_not_fall_back(monkeypatch):
    monkeypatch.setattr(settings, "groq_api_key", "test-key")
    class Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, **kwargs):
            return httpx.Response(429, request=httpx.Request("POST", url))
    import app.adapters as adapters
    monkeypatch.setattr(adapters.httpx, "AsyncClient", lambda **kwargs: Client())
    with pytest.raises(ServiceUnavailable, match="free quota"):
        asyncio.run(GroqGateway().request("audio/speech", json={}))
