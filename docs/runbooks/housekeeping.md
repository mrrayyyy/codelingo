# Housekeeping

A repeatable audit of the ledger and the backlog. **Run when asked**, or at the
start of a session that has not touched the repo for a week.

```sh
python3 tools/docs/housekeeping.py              # exit 1 when something needs a decision
python3 tools/docs/housekeeping.py --stale-days 5
```

It reports, grouped:

1. **Ledger past `next_review`, or missing it.** The field is the only thing
   between the ledger and a pile nobody reads.
2. **Backlog gone quiet** — `in_progress/` tickets untouched for more than the
   stale window, with an empty `## Implementation Log`, never committed, or more
   than two in progress at once; `open/` tickets that name no blocker.
3. **Closed tickets with deviations** no ledger entry cites — check whether any
   deviation left something unresolved.
4. **Open protocol friction** — needs a decision, not a new date.
5. **Unreferenced protocol docs** — a rule nothing links to is a rule nothing
   follows.
6. **Dead relative links** (via `tools/docs/check_doc_links.py`).

## What to do with the output

The script never resolves, re-dates or deletes anything. Report the findings to
the owner as a grouped list and let them decide per item: work it (graduate to a
ticket), re-date it with a reason, or cancel it with a reason. Do not write a
report file — a report nobody asked for becomes another stale document.

## After moving any ticket or ledger entry

```sh
python3 tools/docs/check_doc_links.py --fix-moves
```

Moving a file silently breaks every relative link into it; markdown gives no
error.
