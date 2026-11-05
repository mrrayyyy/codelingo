"""Single-user self-hosted API. Browser access goes through the Next.js proxy."""
from __future__ import annotations

import csv
import asyncio
import html
import io
import secrets
import zipfile
from contextlib import asynccontextmanager, suppress
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Literal
from zoneinfo import ZoneInfo

import genanki
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import BackgroundTasks, Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from starlette.background import BackgroundTask
from pydantic import BaseModel, Field
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from .config import settings
from .contracts import Answer, Context, Exercise, UserProfile, Vocab
from .db import Attempt, ContextSentence, ExerciseRow, ImportJob, Plugin, Repo, RepoVocab, ReviewSchedule, SessionLocal, User, VocabItem, get_db, init_db, now, uid
from .imports import cleanup_spool, github_repository, process_import
from .srs import srs_adapter


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    from .plugins import registry
    with SessionLocal.begin() as db:
        for plugin in registry.values():
            manifest = plugin.manifest
            db.merge(Plugin(id=manifest.id, version=manifest.version, skills=[s.value for s in manifest.skills], services=manifest.services))
    settings.spool_dir.mkdir(parents=True, exist_ok=True)
    await cleanup_spool({})
    async def maintenance():
        while True:
            await asyncio.sleep(300)
            try:
                await cleanup_spool({})
            except Exception:
                # No keep-alive traffic; the task stops when the host sleeps.
                pass
    task = asyncio.create_task(maintenance())
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(401, "A valid API key is required")


app = FastAPI(title="CodeLingo", version="0.1.0", lifespan=lifespan, dependencies=[Depends(require_key)])
DB = Annotated[Session, Depends(get_db)]
USER = "local-user"


def aware(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def vocabulary(db: Session, repo_id: str | None = None) -> list[Vocab]:
    links = db.scalars(select(RepoVocab).where(RepoVocab.repo_id == repo_id) if repo_id else select(RepoVocab)).all()
    by_word: dict[str, list[RepoVocab]] = {}
    for link in links:
        by_word.setdefault(link.vocab_id, []).append(link)
    contexts = db.scalars(select(ContextSentence).where(ContextSentence.repo_vocab_id.in_([l.id for l in links]))).all() if links else []
    by_link: dict[str, list[Context]] = {}
    for context in contexts:
        by_link.setdefault(context.repo_vocab_id, []).append(Context(text=context.text, file_path=context.file_path,
                       line_number=context.line_number, kind=context.kind))
    query = select(VocabItem).where(VocabItem.user_id == USER)
    if repo_id:
        query = query.where(VocabItem.id.in_(by_word))
    result = []
    for word in db.scalars(query).all():
        word_links = by_word.get(word.id, [])
        word_contexts = [c for link in word_links for c in by_link.get(link.id, [])]
        unique = list({(c.text, c.file_path, c.line_number): c for c in word_contexts}.values())
        unique.sort(key=lambda c: c.kind == "identifier")
        result.append(Vocab(id=word.id, lemma=word.lemma, part_of_speech=word.part_of_speech,
            cefr=word.cefr, cefr_estimated=word.cefr_estimated, ipa=word.ipa, definition=word.definition,
            tags=word.tags, frequency=sum(l.frequency for l in word_links),
            rank=max((l.rank for l in word_links), default=0), contexts=unique[:3]))
    return sorted(result, key=lambda v: (-v.rank, v.lemma))


@app.get("/health")
def health(db: DB):
    db.execute(select(1))
    return {"status": "ok", "job_mode": settings.job_mode}


@app.get("/profile")
def profile(db: DB):
    user = db.get(User, USER)
    return UserProfile(native_language=user.native_language, target_level=user.target_level,
                       daily_goal=user.daily_goal, tts_voice=user.tts_voice)


class ProfileUpdate(BaseModel):
    native_language: Literal["en", "vi"]
    target_level: Literal["A2", "B1", "B2"]
    daily_goal: int = Field(ge=1, le=100)
    tts_voice: str = Field(min_length=1, max_length=100)


@app.patch("/profile")
def update_profile(body: ProfileUpdate, db: DB):
    user = db.get(User, USER)
    for key, value in body.model_dump().items():
        setattr(user, key, value)
    db.commit()
    return profile(db)


@app.get("/dashboard")
def dashboard(db: DB):
    current = now()
    tz = ZoneInfo(settings.timezone)
    today = current.astimezone(tz).date()
    schedules = db.scalars(select(ReviewSchedule).where(ReviewSchedule.user_id == USER)).all()
    attempts = db.scalars(select(Attempt).where(Attempt.user_id == USER).order_by(Attempt.created_at.desc())).all()
    daily: dict[str, int] = {}
    skills: dict[str, list[float]] = {}
    for attempt in attempts:
        date = aware(attempt.created_at).astimezone(tz).date().isoformat()
        daily[date] = daily.get(date, 0) + 1
        skill = attempt.answer.get("skill", "review")
        skills.setdefault(skill, []).append(attempt.score)
    streak, day = 0, today
    if day.isoformat() not in daily:
        day -= timedelta(days=1)
    while day.isoformat() in daily:
        streak += 1
        day -= timedelta(days=1)
    mastered = sum(s.reviews >= 3 and (s.card.get("stability") or 0) >= 14 for s in schedules)
    words = vocabulary(db)
    tags: dict[str, int] = {}
    for word in words:
        for tag in word.tags:
            tags[tag] = tags.get(tag, 0) + 1
    return {"total_words": len(words), "mastered": mastered,
        "due": sum(aware(s.due) <= current for s in schedules), "streak": streak,
        "today_reviews": daily.get(today.isoformat(), 0), "daily_goal": db.get(User, USER).daily_goal,
        "repos": db.scalar(select(func.count()).select_from(Repo).where(Repo.user_id == USER)),
        "activity": [{"date": (today - timedelta(days=i)).isoformat(), "count": daily.get((today - timedelta(days=i)).isoformat(), 0)} for i in range(6, -1, -1)],
        "skills": {k: {"score": round(sum(v) / len(v) * 100), "attempts": len(v)} for k, v in skills.items()},
        "topics": tags}


@app.get("/repos")
def repos(db: DB):
    rows = db.scalars(select(Repo).where(Repo.user_id == USER).order_by(Repo.created_at.desc())).all()
    return [{"id": r.id, "name": r.name, "source_url": r.source_url, "status": r.status,
             "created_at": aware(r.created_at).isoformat(),
             "words": db.scalar(select(func.count()).select_from(RepoVocab).where(RepoVocab.repo_id == r.id)),
             "job": job_dict(db.scalar(select(ImportJob).where(ImportJob.repo_id == r.id).order_by(ImportJob.updated_at.desc())))} for r in rows]


def job_dict(job: ImportJob | None):
    if job is None:
        return None
    return {"id": job.id, "repo_id": job.repo_id, "status": job.status, "progress": job.progress, "message": job.message}


def new_job(db: Session, name: str, source_url: str | None = None) -> ImportJob:
    if settings.job_mode == "github_actions":
        db.scalar(select(User).where(User.id == USER).with_for_update())
        if db.scalar(select(ImportJob.id).where(ImportJob.status.in_(["queued", "processing"])).limit(1)):
            raise HTTPException(409, "One cloud import can run at a time. Wait for the current import to finish.")
    repo = Repo(user_id=USER, name=name[:150], source_url=source_url)
    db.add(repo)
    db.flush()
    job = ImportJob(repo_id=repo.id)
    db.add(job)
    db.commit()
    return job


async def dispatch(job: ImportJob, background: BackgroundTasks):
    if settings.job_mode == "github_actions":
        from .cloud_jobs import dispatch_remote
        try:
            await dispatch_remote(job.id)
        except Exception:
            from .imports import update_job
            update_job(job.id, 0, "Cloud extractor unavailable. Check the GitHub Actions token, repository and workflow.", "failed")
            (settings.spool_dir / f"{job.id}.zip").unlink(missing_ok=True)
            raise HTTPException(503, "Cloud extractor unavailable. Check GitHub Actions configuration.")
    elif settings.job_mode == "arq":
        try:
            redis = await create_pool(RedisSettings.from_dsn(settings.redis_url))
            try:
                await redis.enqueue_job("process_import", job.id, _job_id=job.id)
            finally:
                await redis.aclose()
        except Exception:
            from .imports import update_job
            update_job(job.id, 0, "Job queue unavailable. Check Redis and retry the import.", "failed")
            (settings.spool_dir / f"{job.id}.zip").unlink(missing_ok=True)
            raise HTTPException(503, "Job queue unavailable")
    else:
        background.add_task(process_import, {}, job.id)


@app.post("/imports/zip", status_code=202)
async def import_zip(background: BackgroundTasks, db: DB, file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(422, "Upload a .zip repository archive")
    settings.spool_dir.mkdir(parents=True, exist_ok=True)
    staged = settings.spool_dir / f"{uid()}.part"
    try:
        size = 0
        with staged.open("wb") as output:
            while chunk := await file.read(64 * 1024):
                size += len(chunk)
                if size > settings.max_upload_bytes:
                    raise HTTPException(413, "Archive exceeds 20 MiB")
                output.write(chunk)
        if not zipfile.is_zipfile(staged):
            raise HTTPException(422, "This file is not a valid ZIP archive")
        job = new_job(db, Path(file.filename).stem)
        staged.rename(settings.spool_dir / f"{job.id}.zip")
        await dispatch(job, background)
        return job_dict(job)
    finally:
        staged.unlink(missing_ok=True)
        await file.close()


class GitHubImport(BaseModel):
    url: str = Field(max_length=300)


@app.post("/imports/github", status_code=202)
async def import_github(body: GitHubImport, background: BackgroundTasks, db: DB):
    try:
        owner, name = github_repository(body.url)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    job = new_job(db, f"{owner}/{name}", body.url.strip())
    await dispatch(job, background)
    return job_dict(job)


@app.post("/imports/sample", status_code=202)
async def import_sample(background: BackgroundTasks, db: DB):
    sample = Path(__file__).resolve().parent.parent / "tests/fixtures/sample_repo"
    job = new_job(db, "atlas-api · sample")
    with zipfile.ZipFile(settings.spool_dir / f"{job.id}.zip", "w") as zipped:
        for path in sample.rglob("*"):
            if path.is_file():
                zipped.write(path, path.relative_to(sample))
    await dispatch(job, background)
    return job_dict(job)


@app.get("/jobs/{job_id}")
def job_status(job_id: str, db: DB):
    job = db.get(ImportJob, job_id)
    if not job:
        raise HTTPException(404, "Import job not found")
    return job_dict(job)


@app.delete("/repos/{repo_id}", status_code=204)
def delete_repo(repo_id: str, db: DB):
    repo = db.get(Repo, repo_id)
    if not repo or repo.user_id != USER:
        raise HTTPException(404, "Repository not found")
    if repo.status in {"queued", "processing"}:
        raise HTTPException(409, "Wait for the import to finish before removing it")
    db.delete(repo)
    db.commit()


@app.get("/vocab")
def list_vocab(db: DB, repo_id: str | None = None):
    return vocabulary(db, repo_id)


@app.delete("/vocab/{vocab_id}", status_code=204)
def delete_word(vocab_id: str, db: DB):
    word = db.get(VocabItem, vocab_id)
    if not word or word.user_id != USER:
        raise HTTPException(404, "Word not found")
    db.delete(word)
    db.commit()


@app.get("/review")
def due_cards(db: DB):
    due = db.scalars(select(ReviewSchedule).where(ReviewSchedule.user_id == USER, ReviewSchedule.due <= now())
                     .order_by(ReviewSchedule.due).limit(50)).all()
    words = {w.id: w for w in vocabulary(db)}
    return [{"vocab": words[s.vocab_id], "version": s.version, "reviews": s.reviews,
             "due": aware(s.due).isoformat()} for s in due if s.vocab_id in words]


class ReviewAnswer(BaseModel):
    vocab_id: str
    rating: Literal[1, 2, 3, 4]
    version: int = Field(ge=0)
    submission_id: str = Field(min_length=36, max_length=36)


@app.post("/review")
def review(body: ReviewAnswer, db: DB):
    previous = db.scalar(select(Attempt).where(Attempt.submission_id == body.submission_id))
    if previous:
        if previous.vocab_id != body.vocab_id or previous.answer.get("rating") != body.rating:
            raise HTTPException(409, "Submission ID already used for a different answer")
        return previous.feedback
    row = db.scalar(select(ReviewSchedule).where(ReviewSchedule.user_id == USER, ReviewSchedule.vocab_id == body.vocab_id))
    if not row:
        raise HTTPException(404, "Flashcard not found")
    if row.version != body.version or aware(row.due) > now():
        raise HTTPException(409, "This card has changed or is not due. Refresh your review queue.")
    scheduled = srs_adapter.review(row.card, body.rating, now())
    result = {"due": scheduled.due.isoformat(), "version": row.version + 1,
              "rating": body.rating, "review_log": scheduled.log}
    changed = db.execute(update(ReviewSchedule).where(ReviewSchedule.id == row.id, ReviewSchedule.version == body.version)
        .values(card=scheduled.card, due=scheduled.due, version=body.version + 1, reviews=row.reviews + 1,
                lapses=row.lapses + int(body.rating == 1)))
    if changed.rowcount != 1:
        db.rollback()
        raise HTTPException(409, "Card already reviewed. Refresh your review queue.")
    db.add(Attempt(user_id=USER, vocab_id=body.vocab_id, submission_id=body.submission_id,
                   answer={"rating": body.rating, "skill": "review"}, score=(body.rating - 1) / 3, feedback=result))
    db.commit()
    return result


def csv_safe(value: str) -> str:
    return "'" + value if value[:1] in {"=", "+", "-", "@", "\t", "\r", "\n"} else value


@app.get("/export/csv")
def export_csv(db: DB):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["lemma", "part_of_speech", "cefr_estimate", "definition", "ipa", "frequency", "context", "reference"])
    for word in vocabulary(db):
        context = word.contexts[0] if word.contexts else None
        writer.writerow([csv_safe(str(v)) for v in [word.lemma, word.part_of_speech, word.cefr, word.definition or "",
            word.ipa or "", word.frequency, context.text if context else "",
            f"{context.file_path}:{context.line_number}" if context else ""]])
    return Response("\ufeff" + output.getvalue(), media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="codelingo-vocabulary.csv"'})


@app.get("/export/anki")
def export_anki(db: DB):
    model = genanki.Model(1738914021, "CodeLingo context", fields=[{"name": "Word"}, {"name": "Meaning"}, {"name": "Context"}],
        templates=[{"name": "Vocabulary", "qfmt": "{{Word}}<br>{{Context}}", "afmt": '{{FrontSide}}<hr id="answer">{{Meaning}}'}])
    deck = genanki.Deck(1738914022, "CodeLingo — My project vocabulary")
    for word in vocabulary(db):
        context = word.contexts[0] if word.contexts else None
        text = f"{context.text} ({context.file_path}:{context.line_number})" if context else ""
        deck.add_note(genanki.Note(model=model, fields=[html.escape(word.lemma), html.escape(word.definition or "Definition not available offline"), html.escape(text)], guid=genanki.guid_for(word.id)))
    with TemporaryDirectory() as temp:
        path = Path(temp) / "words.apkg"
        genanki.Package(deck).write_to_file(str(path))
        data = path.read_bytes()
    return Response(data, media_type="application/octet-stream", headers={"Content-Disposition": 'attachment; filename="codelingo.apkg"'})


def service_reason(plugin_id: str) -> str | None:
    from .adapters import PiperTTS
    from .plugins import registry
    plugin = registry.get(plugin_id)
    if not plugin:
        return "Unknown learning module"
    for service in plugin.manifest.services:
        provider = {"tts": settings.tts_provider, "stt": settings.stt_provider, "llm": settings.llm_provider}.get(service)
        if provider == "groq":
            if not settings.groq_api_key:
                return "Add GROQ_API_KEY on the cloud host. No local speech or AI model is needed."
            continue
        if service == "tts" and not PiperTTS.available():
            return "Configure PIPER_BINARY and PIPER_MODEL to enable local audio."
        if service == "stt" and not settings.whisper_url:
            return "Configure WHISPER_URL with a local transcription server."
        if service == "llm" and not (settings.ollama_url and settings.ollama_model):
            return "Configure OLLAMA_URL and OLLAMA_MODEL to enable local writing feedback."
    return None


@app.get("/plugins")
def list_plugins():
    from .plugins import registry
    return [{**p.manifest.model_dump(), "available": service_reason(p.manifest.id) is None,
             "unavailable_reason": service_reason(p.manifest.id)} for p in registry.values()]


@app.post("/practice/{plugin_id}")
async def generate_practice(plugin_id: str, db: DB):
    from .plugins import registry
    plugin = registry.get(plugin_id)
    if not plugin:
        raise HTTPException(404, "Learning module not found")
    reason = service_reason(plugin_id)
    if reason:
        raise HTTPException(503, reason)
    exercises = await plugin.generate(vocabulary(db), profile(db))
    for exercise in exercises:
        payload = exercise.model_dump(exclude={"answer_key"})
        db.add(ExerciseRow(id=exercise.id, vocab_id=exercise.vocab_id, plugin_id=plugin_id,
                           payload=payload, answer_key=exercise.answer_key))
    db.commit()
    return [e.model_dump(exclude={"answer_key"}) for e in exercises]


@app.get("/practice/{exercise_id}/audio")
async def exercise_audio(exercise_id: str, db: DB):
    from .adapters import ServiceUnavailable, tts_adapter
    row = db.get(ExerciseRow, exercise_id)
    if not row or row.plugin_id != "listening.dictation":
        raise HTTPException(404, "Dictation exercise not found")
    try:
        audio = await tts_adapter().synthesize(row.answer_key["transcript"], row.payload["payload"].get("voice", "en_US"))
        return Response(audio, media_type="audio/wav", headers={"Cache-Control": "no-store"})
    except ServiceUnavailable as exc:
        raise HTTPException(503, str(exc))


class PracticeAnswer(Answer):
    submission_id: str = Field(min_length=36, max_length=36)


@app.post("/practice/{exercise_id}/grade")
async def grade_practice(exercise_id: str, body: PracticeAnswer, db: DB):
    from .adapters import ServiceUnavailable
    from .plugins import registry
    if not body.text.strip():
        raise HTTPException(422, "Write or record an answer first")
    previous = db.scalar(select(Attempt).where(Attempt.submission_id == body.submission_id))
    if previous:
        if previous.exercise_id != exercise_id or previous.answer.get("text") != body.text:
            raise HTTPException(409, "Submission ID already used for a different answer")
        return previous.feedback
    row = db.get(ExerciseRow, exercise_id)
    if not row:
        raise HTTPException(404, "Exercise not found")
    plugin = registry[row.plugin_id]
    exercise = Exercise(**row.payload, answer_key=row.answer_key)
    try:
        feedback = await plugin.grade(exercise, Answer(text=body.text))
    except ServiceUnavailable as exc:
        raise HTTPException(503, str(exc))
    db.add(Attempt(user_id=USER, vocab_id=row.vocab_id, exercise_id=row.id, submission_id=body.submission_id,
        answer={"text": body.text, "skill": plugin.manifest.skills[0].value}, score=feedback.score, feedback=feedback.model_dump()))
    db.commit()
    return feedback


@app.post("/speech/transcribe")
async def transcribe(file: UploadFile = File(...)):
    from .adapters import ServiceUnavailable, stt_adapter
    try:
        audio = await file.read(10 * 1024 * 1024 + 1)
        if not audio or len(audio) > 10 * 1024 * 1024:
            raise HTTPException(413, "Audio must be between 1 byte and 10 MiB")
        suffix = Path(file.filename or "recording.webm").suffix.lower()
        if suffix not in {".wav", ".webm", ".mp3", ".m4a", ".ogg", ".mp4"}:
            raise HTTPException(422, "Use WAV, WebM, MP3, M4A, OGG, or MP4 audio")
        return {"text": await stt_adapter().transcribe(audio, f"recording{suffix}")}
    except ServiceUnavailable as exc:
        raise HTTPException(503, str(exc))
    finally:
        await file.close()


@app.post("/vocab/{vocab_id}/dictionary")
async def lookup_dictionary(vocab_id: str, db: DB):
    from .adapters import FreeDictionary
    word = db.get(VocabItem, vocab_id)
    if not word:
        raise HTTPException(404, "Word not found")
    entry = await FreeDictionary().lookup(word.lemma)
    if entry.definition:
        word.definition, word.ipa = entry.definition, entry.ipa
        db.commit()
    return entry


@app.get("/cloud/jobs/{job_id}")
def cloud_job_input(job_id: str, db: DB):
    job = db.get(ImportJob, job_id)
    if not job:
        raise HTTPException(404, "Import job not found")
    repo = db.get(Repo, job.repo_id)
    return {"job_id": job.id, "status": job.status, "source_url": repo.source_url}


@app.get("/cloud/jobs/{job_id}/archive")
def cloud_job_archive(job_id: str, db: DB):
    job = db.get(ImportJob, job_id)
    if not job or job.status in {"completed", "failed"}:
        raise HTTPException(404, "Active import not found")
    archive = settings.spool_dir / f"{job.id}.zip"
    if not archive.is_file():
        raise HTTPException(410, "Temporary archive expired or host restarted. Please upload it again.")
    return FileResponse(archive, media_type="application/zip", headers={"Cache-Control": "no-store"},
                        background=BackgroundTask(archive.unlink, missing_ok=True))


class CloudProgress(BaseModel):
    progress: int = Field(ge=0, le=95)
    failed: bool = False


@app.post("/cloud/jobs/{job_id}/progress")
def cloud_job_progress(job_id: str, body: CloudProgress, db: DB):
    from .imports import update_job
    job = db.get(ImportJob, job_id)
    if not job:
        raise HTTPException(404, "Import job not found")
    if job.status not in {"completed", "failed"}:
        update_job(job_id, body.progress, "Cloud extraction failed. Check the workflow run and retry the import." if body.failed
            else "Extracting vocabulary on a cloud runner", "failed" if body.failed else "processing")
    return {"ok": True}


class CloudResult(BaseModel):
    items: list[Vocab] = Field(max_length=500)


@app.post("/cloud/jobs/{job_id}/complete")
def cloud_job_complete(job_id: str, body: CloudResult, db: DB):
    from .imports import persist_items
    if not db.get(ImportJob, job_id):
        raise HTTPException(404, "Import job not found")
    persist_items(job_id, body.items)
    (settings.spool_dir / f"{job_id}.zip").unlink(missing_ok=True)
    return {"ok": True}
