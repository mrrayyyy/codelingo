---
name: codelingo-doc-manager
description: Create, move and close CodeLingo backlog tickets, file and resolve ledger entries, write ADRs, keep docs in sync with code, run housekeeping, and commit/push documentation changes according to docs/protocol/. Use when starting or finishing non-trivial work, noticing a bug/debt/drift/idea, recording a decision, or when asked about project status ("what's next", "what's in progress").
---

# CodeLingo Documentation Manager

The procedures for the protocol in [docs/protocol/](../../../docs/protocol/README.md).
The protocol wins if this file and it disagree — and that disagreement is a
`protocol-friction` ledger entry.

## 1. Where things go

| Kind of fact | Destination | Pattern |
| :--- | :--- | :--- |
| Decided work | `docs/backlog/<status>/` | `YYYYMMDD_<slug>.md` from `docs/backlog/_TEMPLATE.md` |
| Noticed, not decided | `docs/ledger/open/` | `<type>_YYYYMMDD_<slug>.md` from `docs/ledger/_TEMPLATE.md` |
| Why we chose this | `docs/decisions/` | `NNNN-<slug>.md` from `0000-template.md`; add to the index in its README |
| What exists | `docs/architecture.md`, `README.md`, `docs/cloud-deployment.vi.md` | update in place |
| Product direction | `docs/product/roadmap.md` | update phase status when tickets close |
| Repeatable procedure | `docs/runbooks/<procedure>.md` | no dates, no phases |
| Scratch | `docs/tmp/<YYYYMMDD>_<task>/` | git-ignored |

Statuses: backlog `open → ready → in_progress → done` (or `cancel`); ledger
`open → resolved | cancelled`. Status is the directory.

## 2. SOP A — Start work

1. `ls docs/backlog/in_progress docs/backlog/ready`. Resume an in-progress
   ticket before starting another; keep at most two in progress.
2. No ticket for non-trivial work? Create one from the template (`owner: claude`
   unless the owner said otherwise), commit it:
   `git add docs/backlog/ready/<file> && git commit -m "docs(backlog): open <slug>"`.
3. Move it: `git mv docs/backlog/ready/<file> docs/backlog/in_progress/<file>`.
4. Write `## Plan` as a detailed checklist; mark `[gate]` and `[user]` items.
   `stakes: irreversible` → write `## Blast Radius` before any execution.
5. Commit: `docs(backlog): start <slug>`.

## 3. SOP B — During work

- After each meaningful step: tick the plan item with evidence, append a dated
  line to `## Implementation Log`, commit the ticket together with the code it
  describes.
- Noticed something out of scope? File it to the ledger now (SOP D) and carry on.
- Discovered new required work? Add a plan item; do not do it silently.

## 4. SOP C — Finish work

1. Run the checks the change touches (EXECUTION.md § Pre-push checks).
2. Doc sync: update every doc the change invalidated (DOC_SYNC.md table).
   Shipped a user-visible feature → README "What is implemented" and roadmap.
3. Write `## Deviations` (or "None").
4. File residual debt to `docs/ledger/open/`, `source:` this ticket.
5. `git mv docs/backlog/in_progress/<file> docs/backlog/done/<file>`.
6. `python3 tools/docs/check_doc_links.py --fix-moves`.
7. If a blocked `open/` ticket was waiting on this one, move it to `ready/`.
8. Commit `docs(backlog): close <slug>` and push (SOP F).

## 5. SOP D — Ledger

File in the turn it is noticed:

```markdown
---
type: bug | tech-debt | drift | process-gap | protocol-friction | idea
status: open
discovered: YYYY-MM-DD
next_review: YYYY-MM-DD   # default +14 days
source: <ticket | file:line | CI run URL | conversation>
severity: blocker | high | normal | low
owner: claude | user | either
---
# One-line summary
## Context & Evidence
(command, output, date)
## Recommended Action
```

Graduate: create the ticket, then `git mv` the entry to `docs/ledger/resolved/`,
set `status: resolved`, add `## Resolution` linking the ticket. Cancel the same
way into `cancelled/` with the reason.

## 6. SOP E — ADR

Write one when a decision is non-obvious or debated and should not be
re-litigated. Next free number, status `proposed` until the owner agrees, then
`accepted`. Add a row to `docs/decisions/README.md`.

## 7. SOP F — Commit and push

```sh
git add <explicit paths>                       # never -A / .
python3 tools/docs/scan_secrets.py             # must print "No secrets found"
python3 tools/docs/check_doc_links.py          # docs touched
.venv/bin/python -m pytest backend/tests -q    # backend touched
npm --prefix frontend run typecheck            # frontend touched
git commit -m "<type>(<scope>): <what and why>"
git log --oneline origin/main..HEAD            # know what rides along
git push origin main
```

Commit messages end with the attribution lines the session requires. Gated even
though push is autonomous: force push, history rewrite, repo settings/secrets,
hosted service config, hosted schema/data changes (EXECUTION.md).

## 8. SOP G — Status questions and housekeeping

- "What's next?" → list `in_progress/` and `ready/` with `priority` and `skill`,
  recommend one in line with the current roadmap phase.
- "Housekeeping" → `python3 tools/docs/housekeeping.py`, report grouped, let the
  owner decide each item. Never auto-resolve or re-date.

## 9. Public-repo hygiene

Tickets, ledger entries and commit messages are public. No secrets, hosted URLs
with credentials, employer system names, colleague names, or vocabulary/snippets
from private repositories. Describe them generically.
