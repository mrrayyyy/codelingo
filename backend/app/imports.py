"""Safe archive handling, temporary-source lifecycle, and durable job dispatch."""
from __future__ import annotations

import asyncio
import re
import shutil
import stat
import time
import zipfile
from pathlib import Path, PurePosixPath
from datetime import timezone
from tempfile import TemporaryDirectory

import httpx
from sqlalchemy import select

from .config import settings
from .contracts import Vocab
from .db import ContextSentence, ImportJob, Repo, RepoVocab, ReviewSchedule, SessionLocal, User, VocabItem, now
from .srs import srs_adapter

_import_lock = asyncio.Lock()


def github_repository(url: str) -> tuple[str, str]:
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?", url.strip())
    if not match or any(part in {".", ".."} or part.startswith(".") for part in match.groups()):
        raise ValueError("Use a public repository URL: https://github.com/owner/repository")
    return match.group(1), match.group(2)


async def download_github(url: str, target: Path) -> None:
    owner, repository = github_repository(url)
    # Fixed host/path, no arbitrary URL fetch, redirects disabled.
    archive = f"https://codeload.github.com/{owner}/{repository}/zip/HEAD"
    async with httpx.AsyncClient(timeout=90, follow_redirects=False, trust_env=False) as client:
        async with client.stream("GET", archive) as response:
            response.raise_for_status()
            total = 0
            with target.open("wb") as output:
                async for chunk in response.aiter_bytes():
                    total += len(chunk)
                    if total > settings.max_upload_bytes:
                        raise ValueError("GitHub archive exceeds 20 MiB; upload a smaller ZIP")
                    output.write(chunk)


def unpack_archive(archive: Path, root: Path) -> Path:
    """No extractall: enforce path, symlink, count and expanded-byte limits."""
    with zipfile.ZipFile(archive) as zipped:
        entries = zipped.infolist()
        if len(entries) > settings.max_files:
            raise ValueError("Archive exceeds the 5,000-entry limit")
        total = 0
        for entry in entries:
            path = PurePosixPath(entry.filename)
            mode = entry.external_attr >> 16
            if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or ":" in entry.filename:
                raise ValueError("Archive contains an unsafe file path")
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                raise ValueError("Archive contains a link or unsupported file type")
            total += entry.file_size
            if total > settings.max_expanded_bytes:
                raise ValueError("Expanded archive exceeds 50 MiB")
            destination = root.joinpath(*path.parts)
            if entry.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zipped.open(entry) as source, destination.open("wb") as output:
                copied = 0
                while chunk := source.read(64 * 1024):
                    copied += len(chunk)
                    if copied > entry.file_size:
                        raise ValueError("Invalid archive size metadata")
                    output.write(chunk)
    children = list(root.iterdir())
    return children[0] if len(children) == 1 and children[0].is_dir() else root


def update_job(job_id: str, progress: int, message: str, status: str = "processing") -> None:
    with SessionLocal.begin() as db:
        job = db.get(ImportJob, job_id)
        if job:
            job.progress, job.message, job.status, job.updated_at = progress, message, status, now()
            repo = db.get(Repo, job.repo_id)
            if repo:
                repo.status = status


def persist_vocabulary(job_id: str, root: Path) -> None:
    # Import heavy NLP libraries only in the extractor process, never the cloud web server.
    from .extraction import extract_repository
    def progress(done: int, total: int):
        if done == total or done % max(1, total // 10) == 0:
            update_job(job_id, 20 + int(65 * done / max(total, 1)), f"Extracting vocabulary · {done}/{total} files")

    items = extract_repository(root, progress)
    persist_items(job_id, items)


def persist_items(job_id: str, items: list[Vocab]) -> None:
    with SessionLocal.begin() as db:
        # Serialize cloud callbacks per user to keep cross-repo deduplication atomic.
        db.scalar(select(User).where(User.id == "local-user").with_for_update())
        job = db.scalar(select(ImportJob).where(ImportJob.id == job_id).with_for_update())
        if not job or job.status in {"completed", "failed"}:
            return
        repo = db.get(Repo, job.repo_id)
        for item in items:
            word = db.scalar(select(VocabItem).where(VocabItem.user_id == repo.user_id,
                             VocabItem.lemma == item.lemma, VocabItem.part_of_speech == item.part_of_speech))
            if word is None:
                word = VocabItem(user_id=repo.user_id, **item.model_dump(exclude={"id", "frequency", "rank", "contexts"}))
                db.add(word)
                db.flush()
                scheduled = srs_adapter.new_card()
                db.add(ReviewSchedule(user_id=repo.user_id, vocab_id=word.id, card=scheduled.card, due=scheduled.due))
            link = db.scalar(select(RepoVocab).where(RepoVocab.repo_id == repo.id, RepoVocab.vocab_id == word.id))
            if link:
                continue  # A retried worker never duplicates contexts or resets a card.
            link = RepoVocab(repo_id=repo.id, vocab_id=word.id, frequency=item.frequency, rank=item.rank)
            db.add(link)
            db.flush()
            for context in item.contexts:
                db.add(ContextSentence(repo_vocab_id=link.id, **context.model_dump()))
        repo.status = job.status = "completed"
        job.progress = 100
        job.message = f"Ready to learn · {len(items)} vocabulary items extracted"
        job.updated_at = now()


async def process_import(job_id: str) -> None:
    # Imports run inside the API process; one at a time keeps memory bounded.
    async with _import_lock:
        await _process_import(job_id)


async def _process_import(job_id: str) -> None:
    spool = settings.spool_dir / f"{job_id}.zip"
    try:
        with SessionLocal() as db:
            job = db.get(ImportJob, job_id)
            if not job or job.status in {"completed", "failed"}:
                return
            repo = db.get(Repo, job.repo_id)
            url = repo.source_url
        update_job(job_id, 5, "Preparing repository")
        if url:
            await download_github(url, spool)
        update_job(job_id, 15, "Checking archive and extracting text")
        with TemporaryDirectory(prefix="codelingo-", dir=settings.spool_dir) as temporary:
            root = await asyncio.to_thread(unpack_archive, spool, Path(temporary))
            await asyncio.to_thread(persist_vocabulary, job_id, root)
    except Exception as exc:
        # Never expose arbitrary exception strings containing source or credentials.
        if isinstance(exc, (ValueError, zipfile.BadZipFile)):
            message = str(exc)[:180]
        elif isinstance(exc, httpx.HTTPStatusError):
            message = f"GitHub returned HTTP {exc.response.status_code}. Check that the repository is public."
        elif isinstance(exc, httpx.HTTPError):
            message = "Could not download the repository. Check the network and retry."
        else:
            message = "Import failed. Check the NLP model installation and database connection."
        update_job(job_id, 0, message, "failed")
    finally:
        spool.unlink(missing_ok=True)


async def cleanup_spool() -> None:
    """Remove temporary source after crashes; uploads have a one-hour hard TTL."""
    settings.spool_dir.mkdir(parents=True, exist_ok=True)
    cutoff = time.time() - 3600
    for entry in settings.spool_dir.iterdir():
        if entry.stat().st_mtime < cutoff:
            if entry.is_dir():
                shutil.rmtree(entry)
            else:
                entry.unlink(missing_ok=True)
    with SessionLocal() as db:
        jobs = db.scalars(select(ImportJob).where(ImportJob.status.in_(["queued", "processing"]))).all()
        for job in jobs:
            timestamp = job.updated_at.replace(tzinfo=timezone.utc) if job.updated_at.tzinfo is None else job.updated_at
            if timestamp.timestamp() < cutoff:
                update_job(job.id, 0, "Import expired. Please import the repository again.", "failed")
