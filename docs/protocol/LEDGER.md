# The Ledger (`docs/ledger/`)

Everything noticed that needs future attention but is not yet decided work. One
file per item, status by directory: `open/`, `resolved/`, `cancelled/`. Start
from [`_TEMPLATE.md`](../ledger/_TEMPLATE.md); name files
`<type>_YYYYMMDD_<slug>.md`.

Without it, findings live in a chat transcript and die with it.

## Types

`bug`, `tech-debt`, `drift` (docs no longer match the code or the hosted
service), `process-gap`, `protocol-friction`, `idea` (a product idea worth
keeping but not yet scheduled).

## Filing triggers

File **in the turn the thing is noticed**, not at the end of the session:

- **A doc no longer matches the code or the hosted service** → `drift`. Fix the
  doc where cheap; file the entry either way so the drift is recorded.
- **Something that passed turned out wrong** → file it, including why the green
  result was misleading.
- **A shortcut, workaround or leftover is created** → `tech-debt`, at the moment
  it is created.
- **A rule here cost time or blocked legitimate work** → `protocol-friction`.
- **A product idea comes up while doing something else** → `idea`, rather than
  starting it.

## Evidence is mandatory

Every entry records how the thing was established: the command, the output, the
date, the file and line. An entry without evidence cannot be re-checked and will
be believed anyway.

Qualify references: a commit is `codelingo <sha>`, a CI run is its full URL, an
issue or PR is `mrrayyyy/codelingo#12`.

## Anti-staleness

`next_review` is required on every open item (default: two weeks out).
[docs/runbooks/housekeeping.md](../runbooks/housekeeping.md) surfaces overdue
items; it never resolves, re-dates or deletes on its own — the owner decides.

## Resolving

Move the file to `resolved/` (or `cancelled/`) with `git mv`, set `status`, and
add a short section saying what resolved it (commit, ticket) or why it was
dropped. Run `python3 tools/docs/check_doc_links.py --fix-moves` after any move.
