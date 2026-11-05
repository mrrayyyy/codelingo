---
type: tech-debt
status: open
discovered: 2026-11-05
next_review: 2026-11-26
source: product review in 20261105_agent_docs_workflow_bootstrap
severity: low
owner: claude
---

# All 26 API routes live in one 549-line module

## Context & Evidence
`grep -c '^@app\.' backend/app/main.py` → 26 routes; `wc -l` → 549 lines
(2026-11-05). Profile, dashboard, imports, vocabulary, review, export, practice,
speech, dictionary and cloud-callback routes share one file. Fine today; the
speaking and listening plugins will add session routes.

## Recommended Action
When the first Phase 3 ticket starts, split into `APIRouter` modules
(`routes/imports.py`, `routes/review.py`, `routes/practice.py`,
`routes/cloud.py`, …) as its first plan item, with no behaviour change and the
existing tests as the safety net.
