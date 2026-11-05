import io
import zipfile
from uuid import uuid4

from app.config import settings


def test_import_review_deduplicate_delete_export(client):
    response = client.post("/imports/sample")
    assert response.status_code == 202
    job = client.get(f"/jobs/{response.json()['id']}").json()
    assert job["status"] == "completed", job
    assert job["progress"] == 100
    assert not list(settings.spool_dir.glob("*.zip"))
    words = client.get("/vocab").json()
    assert len(words) > 5
    card = client.get("/review").json()[0]
    submission = {"vocab_id": card["vocab"]["id"], "rating": 3, "version": card["version"], "submission_id": str(uuid4())}
    answer = client.post("/review", json=submission)
    assert answer.status_code == 200, answer.text
    assert answer.json()["version"] == 1
    assert client.post("/review", json=submission).json() == answer.json()
    submission["submission_id"] = str(uuid4())
    assert client.post("/review", json=submission).status_code == 409
    stats = client.get("/dashboard").json()
    assert stats["today_reviews"] == 1 and stats["streak"] == 1
    assert stats["due"] == len(words) - 1
    assert client.post("/imports/sample").status_code == 202
    assert len(client.get("/vocab").json()) == len(words)
    assert client.get("/export/csv").text.startswith("\ufefflemma")
    assert zipfile.is_zipfile(io.BytesIO(client.get("/export/anki").content))
    assert client.delete(f"/repos/{job['repo_id']}").status_code == 204
    assert len(client.get("/vocab").json()) == len(words)
    word_id = words[0]["id"]
    assert client.delete(f"/vocab/{word_id}").status_code == 204
    assert len(client.get("/vocab").json()) == len(words) - 1


def test_zip_import_and_failure(client, sample):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zipped:
        for path in sample.rglob("*"):
            if path.is_file():
                zipped.writestr(str(path.relative_to(sample)), path.read_text())
    response = client.post("/imports/zip", files={"file": ("my-project.zip", archive.getvalue(), "application/zip")})
    assert response.status_code == 202
    assert client.get(f"/jobs/{response.json()['id']}").json()["status"] == "completed"
    bad = io.BytesIO()
    with zipfile.ZipFile(bad, "w") as zipped:
        zipped.writestr("../escape.txt", "unsafe")
    response = client.post("/imports/zip", files={"file": ("bad.zip", bad.getvalue())})
    assert client.get(f"/jobs/{response.json()['id']}").json()["status"] == "failed"
    assert not list(settings.spool_dir.glob("*.zip"))
    assert client.post("/imports/zip", files={"file": ("bad.zip", b"not a zip")}).status_code == 422


def test_auth_and_settings(client):
    assert client.get("/vocab", headers={"X-API-Key": "wrong"}).status_code == 401
    assert client.patch("/profile", json={"native_language": "vi", "target_level": "B2", "daily_goal": 15, "tts_voice": "en_US"}).status_code == 200
    assert client.get("/profile").json()["daily_goal"] == 15
    assert client.post("/imports/github", json={"url": "https://internal.invalid"}).status_code == 422
