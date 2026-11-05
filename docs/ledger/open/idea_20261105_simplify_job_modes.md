---
type: idea
status: open
discovered: 2026-11-05
next_review: 2026-11-19
source: product review in 20261105_agent_docs_workflow_bootstrap
severity: normal
owner: user
---

# Consider dropping the ARQ/Redis job mode and the Compose profile

## Context & Evidence
`backend/app/config.py` defines `job_mode: Literal["inline", "arq",
"github_actions"]`; `compose.yaml` runs PostgreSQL, Redis, API and worker;
`Dockerfile.cloud` + `render.yaml` run the cloud profile. Each mode has its own
dispatch path in `backend/app/main.py` (`dispatch`) and its own operational
docs. The owner chose cloud-first (ADR 0001) and is the only user. Read
2026-11-05.

## Recommended Action
Owner decides whether to keep `arq` + Compose. If dropped: keep `inline` for
dev/CI and `github_actions` for hosted; remove Redis/ARQ code, `compose.yaml`
worker and docs sections; record as ADR 0004 superseding part of the original
architecture. If kept: no action, cancel this entry with the reason.
