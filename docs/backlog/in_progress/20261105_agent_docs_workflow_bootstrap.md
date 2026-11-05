---
type: docs
owner: claude
stakes: routine
opened: 2026-11-05
---

# Adopt a docs-as-code task and documentation workflow

## Context
CodeLingo had no task tracking, no decision record and no git history. The
owner's AIOps workspace already runs a provider-neutral protocol (status by
directory for tickets, a ledger for findings, ADRs, a doc-sync rule and a
doc-manager skill). This ticket adapts that model to a single-developer
application repository worked on by Claude Code and Gemini/Antigravity, drops
the infrastructure-specific parts (Vault, Kubernetes, SSH, command logging), and
seeds the backlog from a product review.

Decisions taken with the owner on 2026-11-05 (question dialog):
- Purpose: personal learning tool.
- Agents: Claude Code and Gemini/Antigravity.
- Depth: "just enough" — protocol, backlog, ledger, ADRs, skill, link check and
  housekeeping; no hooks or command logger.
- Repository: public `mrrayyyy/codelingo` on GitHub; agents commit and push
  automatically.
- Priorities for the next 1–2 months: daily cloud use, workplace English
  practice, vocabulary/content quality. Skill focus: speaking, listening,
  reading/vocabulary.

## Acceptance Criteria
- [x] `docs/protocol/` holds every binding rule; agent entry files hold pointers only.
- [x] Backlog and ledger directories with templates; seeded from the review.
- [x] ADRs record the cloud-first, workflow and public/auto-push decisions.
- [x] Link checker and housekeeping script run clean; CI runs the link check.
- [x] Repository on GitHub with history.

## Plan

### Repository
- [x] `git init -b main`; scan candidate files for secrets; baseline commit `e5d8c8e`
- [x] `.gitignore`: `docs/tmp/*`, `.claude/settings.local.json`

### Protocol and entry files
- [x] `docs/protocol/{README,NAVIGATION,EXECUTION,KANBAN,LEDGER,DOC_SYNC,VERIFICATION,SECRETS}.md`
- [x] `AGENTS.md` (shared contract), `CLAUDE.md`, `GEMINI.md` (pointers)
- [x] `.agents/skills/codelingo-doc-manager/SKILL.md`, linked from `.claude/skills/`

### Tracking structure
- [x] `docs/backlog/` five status directories + `_TEMPLATE.md`
- [x] `docs/ledger/` three status directories + `_TEMPLATE.md`
- [x] `docs/decisions/` README, template, ADR 0001–0003
- [x] `docs/runbooks/housekeeping.md`, `tools/docs/check_doc_links.py`, `tools/docs/housekeeping.py`

### Review and seeding
- [x] `docs/product/roadmap.md` — assessment and phased roadmap
- [x] Seed tickets in `ready/` and `open/`; findings not yet decided in `ledger/open/`

### Verification and publish
- [x] Link check and housekeeping exit 0; backend tests and typecheck still pass
- [x] CI step for the link check in `.github/workflows/ci.yml`
- [x] `gh repo create mrrayyyy/codelingo --public --source . --push`

## Implementation Log
- 2026-11-05 — Read AIOps protocol (`aiops/docs/protocol/*`), templates and
  `aiops-doc-manager` skill. Asked the owner 8 scoping questions.
- 2026-11-05 — Baseline evidence: `pytest backend/tests` → 53 passed, 1
  deprecation warning; `npm run typecheck` → exit 0.
- 2026-11-05 — Secret scan over the 62 files git would add: only placeholders in
  `.env*.example` and deliberate fake keys in `backend/tests/test_extraction.py`.
  Baseline commit `e5d8c8e`.
- 2026-11-05 — Wrote protocol, entry files, skill, templates, ADRs, tools,
  roadmap, seed tickets and ledger entries.

## Deviations
- Existing `docs/architecture.md`, `docs/cloud-deployment.vi.md` and
  `docs/verification.md` stay where they are (README links them); NAVIGATION
  maps them instead of moving them.
