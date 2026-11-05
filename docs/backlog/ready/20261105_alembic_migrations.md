---
type: infra
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Add Alembic schema migrations before hosted data exists

## Context
The schema is created with SQLAlchemy `create_all` (README: "do not use it as a
schema upgrade strategy"). Phase 2 adds columns (Vietnamese gloss, phrases). Once
learning history lives in Neon, a schema change without migrations means manual
SQL or data loss. Doing this before the first deploy keeps it `routine`; after,
every migration is `irreversible`.

## Acceptance Criteria
- [ ] `alembic upgrade head` creates the current schema on empty SQLite and PostgreSQL.
- [ ] The baseline revision matches `create_all` (autogenerate shows no diff).
- [ ] API startup runs migrations (or refuses to start on an out-of-date schema) in every job mode.
- [ ] Tests run against the migrated schema; CI green.
- [ ] README and architecture.md describe how to add a migration.

## Plan
### Setup
- [ ] Add `alembic` to `backend/pyproject.toml` and regenerate `backend/requirements.lock`
- [ ] `backend/alembic/` with `env.py` reading `settings.database_url` and `db.Base.metadata`
- [ ] Baseline revision `0001_initial` from the current models in `backend/app/db.py`
### Wire-up
- [ ] Replace `create_all` in the API lifespan (`backend/app/main.py`) with an upgrade-to-head
- [ ] Same for `scripts/cloud_start.py` and the Compose `api` service
- [ ] `backend/tests/conftest.py` builds the test DB through migrations
### Verify and document
- [ ] Autogenerate against the baseline → empty diff
- [ ] pytest, typecheck; CI run green (link the run)
- [ ] Doc sync: README "Run without Docker", architecture.md note on migrations

## Implementation Log

## Deviations
