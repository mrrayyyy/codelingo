---
type: tech-debt
status: open
discovered: 2026-11-05
next_review: 2026-11-26
source: backend test run, 20261105_agent_docs_workflow_bootstrap
severity: low
owner: claude
---

# Test client deprecation warning: httpx with starlette.testclient

## Context & Evidence
`.venv/bin/python -m pytest backend/tests -q` on 2026-11-05 → `53 passed, 1
warning`: `StarletteDeprecationWarning: Using httpx with starlette.testclient is
deprecated; install httpx2 instead` (raised from `fastapi/testclient.py:1`).
Harmless now; a future Starlette release may remove the path and break every API
test at once.

## Recommended Action
Check the Starlette release notes for the replacement, pin or migrate in
`backend/pyproject.toml` and `backend/requirements.lock`, confirm the warning is
gone and tests still pass.
