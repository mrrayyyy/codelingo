# 0002. Docs-as-code task and documentation workflow

- Status: accepted
- Date: 2026-11-05
- Decided by: owner with Claude

## Context
Work on CodeLingo is done by the owner with Claude Code and Gemini/Antigravity
across many sessions. Without a shared record, plans, findings and decisions live
in chat transcripts and are lost when a session ends. The owner already runs a
protocol for this in their AIOps workspace.

## Decision
Adopt a trimmed version of the AIOps protocol:

- binding rules in [docs/protocol/](../protocol/README.md); `AGENTS.md`,
  `CLAUDE.md`, `GEMINI.md` hold pointers only;
- tickets in `docs/backlog/{open,ready,in_progress,done,cancel}/`, status by
  directory;
- findings in `docs/ledger/{open,resolved,cancelled}/` with mandatory evidence and
  `next_review`;
- ADRs in `docs/decisions/`;
- one skill, `.agents/skills/codelingo-doc-manager/`, linked into
  `.claude/skills/`;
- `tools/docs/` scripts for link checking, housekeeping and secret scanning; the
  link check runs in CI.

Dropped from AIOps: Vault/Kubernetes/SSH rules, command logging, safety-gate
hooks, memory folder.

## Alternatives considered
- GitHub Issues/Projects — not readable offline by agents without API calls,
  and splits context from the code.
- Full AIOps setup with hooks — more machinery than a single-developer app needs.
- Nothing — the status quo that lost context.

## Consequences
- Every non-trivial change has a ticket with a plan and a log an interrupted
  session can resume from.
- Tickets and ledger entries are public (see ADR 0003), so they must not contain
  secrets or employer-internal details.
