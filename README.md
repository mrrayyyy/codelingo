# CodeLingo

English practice from the source code you work with. A local-first, single-user MVP with a Next.js interface, a Python extraction pipeline, durable import jobs, and FSRS flashcards.

**Preferred deployment: cloud, no local Docker or models required.** Following the updated product decision, use [the free-tier cloud deployment guide](docs/cloud-deployment.vi.md): Render hosts the lightweight app, Neon stores learning data, GitHub Actions performs NLP on demand, and optional Groq APIs handle speech/writing. The original local/self-hosted profile below remains available for development.

## Design deliverables

Read [the architecture review, Mermaid system diagram, ERD, and milestone plan](docs/architecture.md). The matching plugin contracts are in [TypeScript](shared/plugins.ts) and [Python](backend/app/contracts.py); [the dictation module](backend/app/plugins.py) is a fully worked generation/grading example.

The chosen MVP uses ZIP/public GitHub imports and offline dictionary defaults. Multi-user sign-in and private GitHub OAuth are intentionally deferred, as confirmed during design.

## Run with Docker Compose

Requires Docker with Compose. From this directory:

```sh
cp .env.example .env
# Edit .env: set two different random values for API_KEY and POSTGRES_PASSWORD.
# Generate each with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
docker compose up --build -d
```

Open **http://localhost:3000**. Choose **Import repository → Try the Atlas API sample repository**, or import your own public GitHub URL / ZIP. Follow import progress under My repositories, explore Vocabulary, and open Spaced review. Reveal a word's meaning, then rate your recall; the server persists its next FSRS review time.

The web port binds to loopback. PostgreSQL, Redis, and the API are internal services. Remote use needs TLS and authentication at a reverse proxy; the single-user workspace does not implement login. `.env` is ignored by Git. Passwords in connection URLs must be URL-safe; `secrets.token_urlsafe` is suitable. Set `WEB_PORT` if port 3000 is occupied.

```sh
docker compose logs -f api worker
docker compose down                 # stops services, keeps learning data
```

Do not run `docker compose down -v` unless you intend to delete the stored learning data. Back up PostgreSQL with `pg_dump`; Redis uses AOF persistence for queued jobs.

## Run without Docker

Requires **Python 3.11** and **Node.js 22+**. Uses SQLite and a background task in the API process, so imports are not durable across a process crash. Compose is the deployment configuration.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
.venv/bin/python -m pip install --no-deps -e backend
npm --prefix frontend ci
.venv/bin/python scripts/dev.py
```

The lockfile installs the spaCy English model. If installing directly from `pyproject.toml` instead, run `.venv/bin/python -m spacy download en_core_web_sm` too. Local services listen at http://localhost:3000 and http://127.0.0.1:8000. Ctrl-C stops both. The dev launcher loads root `.env` and shares the API key with Next.js. Without an `.env`, it uses an explicit development key; Compose requires configured secrets.

## What is implemented

- Bounded ZIP and public GitHub imports, progress polling, temporary-source cleanup, retry-safe persistence, PostgreSQL + Redis/ARQ in Compose.
- Tree-sitter comments, Python docstrings, strings, and identifiers for TypeScript/TSX, JavaScript/JSX, Python, Java, and Go. Markdown prose outside fenced blocks. Source code is never run.
- camelCase / snake_case / acronym splitting; spaCy lemmatization/POS; stopword, keyword, and A1-seed exclusion; language and secret-pattern filters; per-repo frequency, estimated CEFR, tags, and ranked vocabulary. Ranking uses logarithmic frequency so repeated generated identifiers do not dominate prose.
- Vocabulary deduplication across repos within the user, 1–3 original contexts with source lines, read-only Monaco excerpts with word highlighting, search/filter controls.
- FSRS adapter, persistent review schedules, stale-card protection, idempotent submissions, learning streaks, daily goals, and measured practice scores. “Mastered” means at least 3 reviews and FSRS stability of at least 14 days; it is a product heuristic, not a language certification.
- Reading multiple choice; worked listening dictation plugin; read-aloud transcript comparison; commit-message and code-review writing plugins. Optional speech/model services are disabled until configured.
- English/Vietnamese interface, learning settings, CSV and Anki `.apkg` exports, repository context deletion, and vocabulary deletion API. Removing a repo preserves learned words and their review schedules.
- Offline dictionary seed definitions and IPA where available; opt-in Free Dictionary API adapter, called with a lemma only. `POST /vocab/{id}/dictionary` enriches one word. Unknown definitions are shown as unavailable instead of generated facts.

Scope remaining for v1: private GitHub OAuth; git-log/PR extraction; highlighted full reading passages/comprehension generation; listening gap-fill; phoneme-based pronunciation scoring; shadowing/free speech; multi-turn standups/interviews; richer writing variants; calibrated CEFR corpus; plugin installation/isolation; Alembic schema migrations. The initial schema uses SQLAlchemy `create_all`; do not use it as a schema upgrade strategy.

## Optional local services — in sequence

First verify import → extract → review. Then enable speech/writing services independently. No speech or LLM service is needed for imports, vocabulary, reading, or flashcards.

1. **TTS / Piper.** Install a Piper CLI and an English `.onnx` voice model with its companion JSON. Set `PIPER_BINARY` and `PIPER_MODEL` to paths **inside the API runtime**. The adapter sends the sentence over stdin, runs without a shell, bounds execution time, and deletes its temporary WAV. The configured model determines the voice; the stored voice label is an adapter hint. With Docker, extend `backend/Dockerfile` to install a compatible Piper runtime and mount the voice files read-only; setting a host executable path alone cannot install Piper inside a container.
2. **STT / Whisper.** Run a local faster-whisper service exposing OpenAI-compatible `POST /v1/audio/transcriptions`, then set `WHISPER_URL` to its base URL. The browser records at most 60 seconds and the API accepts at most 10 MiB. Audio is forwarded transiently and not stored by CodeLingo. Read-aloud grading reports transcript agreement; it does not measure phonemes or pronunciation. Configure the service itself not to retain audio.
3. **LLM / Ollama.** Pull a model appropriate for your hardware, then set `OLLAMA_URL` and `OLLAMA_MODEL`. The adapter calls `/api/chat` with a strict JSON feedback schema. Invalid or unavailable results produce a service error without recording a grade. Feedback is explicitly an AI estimate. Only the chosen exercise context and learner answer are sent to the configured model.

For services on a Docker Desktop host, use `http://host.docker.internal:PORT`; Linux needs an explicit host gateway mapping or services on the Compose network. Restart API/web after environment changes. Configured STT/LLM services are checked on use; a configured URL is not a live health guarantee.

`DICTIONARY_ONLINE=false` keeps dictionary requests offline. Set it to `true` only if you want vocabulary words sent to https://api.dictionaryapi.dev. The optional adapter never sends a repository sentence.

## Verification

```sh
.venv/bin/python -m pytest backend/tests -q
npm --prefix frontend run typecheck
npm --prefix frontend run build
# Against the running local or Compose web app:
cd frontend
npx playwright install chromium
npm run test:e2e
```

Browser tests use the included sample fixture, create learning records, and remove their imported repository context afterward. Run against a development database. Set `BASE_URL` to test another local port. Model-backed adapters are tested with replacement providers and explicit unavailable-service behavior; real TTS/STT/LLM output requires installing those services.

To run the extractor alone:

```sh
.venv/bin/python -m app.extraction backend/tests/fixtures/sample_repo
```

## Layout

```text
backend/app/
  contracts.py     typed plugin and service contracts
  extraction.py    tree-sitter → spaCy → filters → ranking
  lexicon.py       editorial definitions and CEFR estimate seeds
  imports.py       archive boundaries, source lifecycle, ARQ worker
  db.py            relational model and initial schema
  srs.py           replaceable FSRS adapter
  plugins.py       reading, dictation, read-aloud, writing, code review
  adapters.py      Piper, Whisper, Ollama, offline/remote dictionary
  main.py          import, vocabulary, review, exercise, settings/export APIs
backend/tests/     extraction, archive, plugin, and end-to-end API tests
frontend/          Next.js App Router, server-only API proxy, UI, browser tests
shared/            TypeScript plugin contracts
docs/              architecture, ERD, decisions, milestones
scripts/dev.py     local two-service launcher
compose.yaml       PostgreSQL, Redis, API, worker, Next.js
```

No repository is preloaded automatically. **Atlas API** is a small, authored test repository; the decorative dashboard code illustration is not extracted user content. Fonts, Monaco, and its workers are served locally. Monaco is rebuilt from ESM to include the patched DOMPurify override rather than a vendor bundle with an embedded older version.
