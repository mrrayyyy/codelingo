# 0003. Public repository; agents commit and push automatically

- Status: accepted
- Date: 2026-11-05
- Decided by: owner

## Context
The project had no git history. The cloud profile needs the code on GitHub (the
extraction workflow must live on the default branch). The owner chose a public
repository and wants agents to commit and push without asking.

## Decision
- The repository is `mrrayyyy/codelingo`, public, default branch `main`.
- Agents commit after each meaningful step and push to `origin main` once the
  pre-push checks in [EXECUTION.md](../protocol/EXECUTION.md#pre-push-checks)
  pass.
- Still gated: force pushes and history rewrites, repository settings and
  secrets, hosted service configuration, hosted schema/data changes.

## Alternatives considered
- Private repository — GitHub Actions minutes are capped on private repos; the
  owner preferred public.
- Commit automatically, push on request (the AIOps rule) — safer, but the owner
  wanted less friction for a personal project.

## Consequences
- Every ticket, ledger entry and commit message is world-readable:
  [SECRETS.md](../protocol/SECRETS.md) applies to docs as much as code.
- Once Render auto-deploys from `main`, a push is a deploy. The pre-push checks
  and CI are the only gate for routine changes; schema changes stay gated.
- Mistakes are visible immediately, and so is progress.
