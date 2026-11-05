---
type: process-gap
status: open
discovered: 2026-11-05
next_review: 2026-11-19
source: product review in 20261105_agent_docs_workflow_bootstrap
severity: high
owner: user
---

# Importing employer code into the cloud profile may breach workplace policy

## Context & Evidence
The point of CodeLingo is to learn from the code the owner works with, which is
mostly employer-owned. In the cloud profile
([ADR 0001](../../decisions/0001-cloud-first-free-tier.md)) an imported
repository is downloaded by a GitHub Actions runner of a **public** repository
(`.github/workflows/extract.yml`), its context sentences (comments, docstrings,
strings with file paths and line numbers) are stored in Neon
(`context_sentences` in `docs/architecture.md`), and practice text can be sent to
Groq (`backend/app/adapters.py`). `scripts/cloud_extract.py` logs counts only,
so nothing leaks through public Actions logs — but the data still leaves the
employer's control. Established by reading those files, 2026-11-05.

## Recommended Action
Owner decides one of:
1. Import only public/own repositories in the cloud profile; use the local
   profile (inline mode, no LLM) for work code.
2. Check workplace policy and, if allowed, document which repositories are fine.
3. Add a "paste prose only" import (commit messages, PR text the owner wrote)
   that never uploads source.

Until decided, [SECRETS.md](../../protocol/SECRETS.md) restricts agents to
public repositories and the sample.
