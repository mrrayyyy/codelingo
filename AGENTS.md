# CodeLingo — Agent Contract

CodeLingo is the owner's personal tool for learning workplace English from source
code. This file is the shared entry point for every agent (Claude Code,
Gemini/Antigravity). It holds routing and pointers only; binding rules live in
[docs/protocol/](docs/protocol/README.md).

## Start of session
1. Read [docs/protocol/README.md](docs/protocol/README.md), then NAVIGATION,
   EXECUTION and SECRETS. **This repository is public.**
2. See where work stands: `ls docs/backlog/in_progress docs/backlog/ready`.
   Resume an `in_progress` ticket from its `## Implementation Log` before
   starting anything new.
3. For any documentation, ticket or ledger action, read
   [the doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md) in full.
4. Check relevant [ADRs](docs/decisions/README.md) before proposing a change to
   deployment, data model, privacy or the protocol.

## While working
- Non-trivial work happens on a ticket ([KANBAN.md](docs/protocol/KANBAN.md));
  findings are filed to the ledger in the turn they are noticed
  ([LEDGER.md](docs/protocol/LEDGER.md)).
- Commit after each meaningful step and push to `origin main` after the pre-push
  checks pass ([EXECUTION.md](docs/protocol/EXECUTION.md)). Hosted-service,
  secret, schema and history-rewriting actions are gated.
- Behaviour changes update their docs in the same ticket
  ([DOC_SYNC.md](docs/protocol/DOC_SYNC.md)).
- Never present an estimate as a measurement of the learner's English
  ([VERIFICATION.md](docs/protocol/VERIFICATION.md)).

## Communication
Talk to the owner in Vietnamese. Code, comments, commit messages and docs are
English. Use clickable file links and Markdown tables.

## Routing

| Task | Read first |
| :--- | :--- |
| Backend API, data model, plugins | [docs/architecture.md](docs/architecture.md), `backend/app/` |
| Frontend (Next.js) | `frontend/AGENTS.md` — this Next.js differs from training data; read `frontend/node_modules/next/dist/docs/` |
| Extraction quality, vocabulary content | [docs/architecture.md](docs/architecture.md) §4, `backend/app/extraction.py`, `backend/app/lexicon.py` |
| Cloud deployment | [docs/cloud-deployment.vi.md](docs/cloud-deployment.vi.md), [ADR 0001](docs/decisions/0001-cloud-first-free-tier.md) |
| Product direction, priorities | [docs/product/roadmap.md](docs/product/roadmap.md) |
| Tickets, ledger, ADRs, housekeeping | [doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md) |

## Finish
Run the checks the change touches, inspect the diff, tick the ticket's plan,
update its log, commit, push. Report the result, the checks run and their output,
and any limitation — in Vietnamese, with file links.
