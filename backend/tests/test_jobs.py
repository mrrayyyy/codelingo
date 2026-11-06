import asyncio
import os
import time
from datetime import timedelta

import pytest
from pydantic import ValidationError

from app.config import Settings, settings
from app.db import ImportJob, Repo, SessionLocal, now
from app.imports import cleanup_spool


@pytest.mark.parametrize("mode", ["inline", "github_actions"])
def test_supported_job_modes(monkeypatch, mode):
    monkeypatch.setenv("JOB_MODE", mode)
    assert Settings().job_mode == mode


def test_arq_job_mode_rejected(monkeypatch):
    # ADR 0004: ARQ/Redis was removed; a stale .env must fail loudly at startup.
    monkeypatch.setenv("JOB_MODE", "arq")
    with pytest.raises(ValidationError):
        Settings()


def test_cleanup_spool_removes_stale_files_and_expires_stuck_jobs(client):
    settings.spool_dir.mkdir(parents=True, exist_ok=True)
    stale_file = settings.spool_dir / "stale.zip"
    stale_dir = settings.spool_dir / "codelingo-stale"
    fresh_file = settings.spool_dir / "fresh.zip"
    stale_file.write_bytes(b"old")
    stale_dir.mkdir()
    (stale_dir / "source.py").write_text("x = 1")
    fresh_file.write_bytes(b"new")
    two_hours_ago = time.time() - 7200
    os.utime(stale_file, (two_hours_ago, two_hours_ago))
    os.utime(stale_dir, (two_hours_ago, two_hours_ago))

    with SessionLocal.begin() as db:
        repo = Repo(user_id="local-user", name="stuck")
        db.add(repo)
        db.flush()
        stuck = ImportJob(repo_id=repo.id, status="processing", updated_at=now() - timedelta(hours=2))
        active = ImportJob(repo_id=repo.id, status="processing", updated_at=now())
        db.add_all([stuck, active])
        db.flush()
        stuck_id, active_id = stuck.id, active.id

    asyncio.run(cleanup_spool())

    assert not stale_file.exists()
    assert not stale_dir.exists()
    assert fresh_file.exists()
    with SessionLocal() as db:
        assert db.get(ImportJob, stuck_id).status == "failed"
        assert db.get(ImportJob, active_id).status == "processing"
    fresh_file.unlink()
