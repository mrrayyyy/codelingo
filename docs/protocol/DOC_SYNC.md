# Documentation Sync

Work that changes behaviour changes the docs describing that behaviour, in the
same ticket — not in a follow-up that never comes.

1. A change to an API route, the data model, an environment variable, the
   extraction policy, a plugin, or how the app is run or deployed updates the
   matching doc **in the same ticket**.
2. Do not move a ticket to `done/` without checking that the docs it touched
   still describe the code. This check is part of closing, alongside
   `## Deviations`.
3. Debt, shortcuts and known gaps introduced by the work go to
   `docs/ledger/open/` before closing.
4. A decision future work should not re-litigate becomes an ADR in
   `docs/decisions/`.

## Which doc

| Change | Update |
| :--- | :--- |
| New or changed API route, table, column, plugin contract | [docs/architecture.md](../architecture.md) (ERD, contract sections) |
| New environment variable or setting | `.env.example` / `.env.cloud.example`, and [README.md](../../README.md) or [docs/cloud-deployment.vi.md](../cloud-deployment.vi.md) |
| How to run, build, deploy | [README.md](../../README.md), [docs/cloud-deployment.vi.md](../cloud-deployment.vi.md), or a runbook |
| User-visible feature shipped | "What is implemented" in [README.md](../../README.md); roadmap status in [docs/product/roadmap.md](../product/roadmap.md) |
| Why we chose this | `docs/decisions/` |
| What happened during the work | the ticket's `## Implementation Log` |

A document with phase headings, completion ticks or dates in its structure is a
work record, not a runbook. It belongs in a ticket.
