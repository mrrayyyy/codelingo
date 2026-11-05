# Kanban (`docs/backlog/`)

The task board. Status is the **directory the file is in**; changing status
means moving the file (`git mv`), so `git log --follow` shows when each
transition happened.

```text
open/         exists, but blocked — the blocker is named in the ticket
ready/        no blocker, pickable
in_progress/  being worked now
done/         complete; the ticket is its own historical record
cancel/       abandoned, with the reason inline
```

`open/` → `ready/` → `in_progress/` → `done/`. A ticket never jumps from `open/`
to `in_progress/`: whoever clears the blocker moves it to `ready/` first, which
keeps "what is pickable now" answerable with one `ls`.

## When a ticket is needed

Open a ticket for work that changes user-visible behaviour, touches more than one
module, or will take more than about half an hour. Typos, one-line fixes and doc
corrections need only a good commit message.

## Fields

Files are named `YYYYMMDD_slug.md`. Start from
[`_TEMPLATE.md`](../backlog/_TEMPLATE.md).

- `type: feature | content | refactor | infra | docs | investigation`
- `owner: claude | user` — new tickets default to `claude`. `user` only when the
  owner said they will do it (accounts, payments, anything needing their
  browser login). Claude does not pick up or re-own a `user` ticket.
- `stakes: routine | irreversible` — irreversible: hosted schema/data changes,
  deploy configuration, secrets, anything deleting learning data. Self-upgrade
  mid-flight if the work turns out bigger.
- `priority: P1 | P2 | P3` — P1 is the current roadmap phase in
  [docs/product/roadmap.md](../product/roadmap.md).
- `skill:` optional — `speaking | listening | reading | writing | vocabulary` for
  product tickets, so progress per learning skill is visible.

## Lifecycle

1. **Becoming pickable** — the blocker clears; move to `ready/`.
2. **Starting** — move to `in_progress/`. Write `## Plan` first if missing, as a
   [detailed checklist](#the-plan-is-a-detailed-checklist).
3. **Tracking** — append to `## Implementation Log` after each meaningful step.
   A ticket in `in_progress/` with a stale log is a violation: sessions run out
   of context mid-task, and a summary saved for the end is a summary lost.
4. **Closing** — append `## Deviations`; file anything unresolved to
   `docs/ledger/open/` citing this ticket; update docs the work invalidated
   ([DOC_SYNC.md](DOC_SYNC.md)); move to `done/`.

Keep at most **two** tickets in `in_progress/` at once. Personal projects stall
from too much started work, not too little.

## The plan is a detailed checklist

Each item is one action with one checkable result, names where it happens (file,
module, service), is marked **`[gate]`** when it needs confirmation under
[EXECUTION.md](EXECUTION.md) and **`[user]`** when only the owner can do it, and
is ticked `[x]` in the same turn it is done with a pointer to the evidence
(commit, test output). New work discovered mid-ticket is added as an item, not
done silently.

## Commit at creation and at resolution

Commit a ticket the moment it is created and again when it moves to `done/` or
`cancel/` — stage that ticket's files (plus the ledger entries it graduated from
or filed) explicitly. Status is the directory, and git history is the only
record of when it changed; an uncommitted ticket has neither.

## Relationship to the ledger

The [ledger](LEDGER.md) holds things *noticed*; the backlog holds things
*decided*. A ledger item graduates when someone decides to work it, and moves to
`ledger/resolved/` the moment the ticket exists.
