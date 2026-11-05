# Gemini / Antigravity — entry point

This file holds **no rules**. Read [AGENTS.md](AGENTS.md) — the shared contract —
and then [docs/protocol/](docs/protocol/README.md), where every binding rule
lives, so every agent follows the same ones.

Before any ticket, ledger, ADR or housekeeping action, read
[.agents/skills/codelingo-doc-manager/SKILL.md](.agents/skills/codelingo-doc-manager/SKILL.md)
in full and follow it.

Minimum before doing anything:

- [NAVIGATION.md](docs/protocol/NAVIGATION.md) — where every fact lives.
- [EXECUTION.md](docs/protocol/EXECUTION.md) — what is autonomous, what is gated,
  commit and push policy.
- [SECRETS.md](docs/protocol/SECRETS.md) — this repository is public.
- [KANBAN.md](docs/protocol/KANBAN.md) and [LEDGER.md](docs/protocol/LEDGER.md) —
  file findings in the turn you notice them.

If a rule costs time or blocks legitimate work, file `type: protocol-friction`
in `docs/ledger/open/` rather than working around it silently.
