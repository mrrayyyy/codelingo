---
type: feature | content | refactor | infra | docs | investigation
owner: claude | user
stakes: routine | irreversible
priority: P1 | P2 | P3
skill: speaking | listening | reading | writing | vocabulary   # optional, product tickets only
opened: YYYY-MM-DD
---

# Ticket title

## Context
What exists today, what this changes it to, and why it matters to daily
learning. The only section required to open a ticket.

## Acceptance Criteria
- [ ] Rough at creation; refined when picked up. Prefer criteria a test or a
      screenshot can check.

## Plan
Written by whoever picks this up, before work starts. A detailed checklist,
grouped under short headings, one action per item, ticked as done
([KANBAN.md](../protocol/KANBAN.md#the-plan-is-a-detailed-checklist)):

### Group
- [ ] One concrete action, where it happens, and its checkable result
- [ ] `[gate]` A hosted or irreversible action: stops for confirmation
- [ ] `[user]` Something only the owner can do (account signup, browser login)

## Blast Radius
REQUIRED when `stakes: irreversible`: what is unrecoverable, what else this
touches, what a bad outcome looks like, and how to recover.

## Implementation Log
Appended after each meaningful step — a timeline an interrupted session can
resume from.

## Deviations
Appended when closing: judgment calls beyond the original scope, and why.
Anything unresolved gets a `docs/ledger/open/` entry citing this ticket.
