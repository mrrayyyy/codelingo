@AGENTS.md

# Claude Code adapter
- This file holds no rules. Everything binding is in [docs/protocol/](docs/protocol/README.md).
- `.agents/` is canonical. The doc-manager skill is linked into
  `.claude/skills/codelingo-doc-manager`; invoke it for any ticket, ledger, ADR
  or housekeeping action.
- `.claude/settings.local.json` is personal and git-ignored.
- If a rule costs time or blocks legitimate work, file `type: protocol-friction`
  in `docs/ledger/open/` rather than working around it silently.
