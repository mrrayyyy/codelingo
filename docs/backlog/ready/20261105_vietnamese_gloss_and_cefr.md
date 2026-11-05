---
type: content
owner: claude
stakes: routine
priority: P1
skill: vocabulary
opened: 2026-11-05
---

# Vietnamese meanings, examples and better CEFR estimates

## Context
The bundled lexicon has 33 definitions (`backend/app/lexicon.py`, counted
2026-11-05) and `vocab_items` has no Vietnamese field, so most flashcards show
"definition unavailable". For a Vietnamese learner the review loop needs a short
Vietnamese meaning, an English definition and a plain example. Unknown CEFR
defaults to B2.

Constraint from [VERIFICATION.md](../../protocol/VERIFICATION.md): generated
content is labelled as AI-generated and never presented as dictionary fact.

## Acceptance Criteria
- [ ] Schema (via Alembic): `meaning_vi`, `definition_en`, `example`, `content_source` (`lexicon | dictionary | ai`), `content_checked` per vocab item.
- [ ] Enrichment on demand and in batches through the configured LLM adapter, with a strict JSON schema; the word and its retained context only — never whole files.
- [ ] UI labels AI content and lets the owner edit/approve it (`content_checked`).
- [ ] CEFR estimate uses `wordfreq` Zipf bands for words outside the reviewed lexicon; marked estimated.
- [ ] Offline/no-LLM mode unchanged: shows "unavailable", no invented text.
- [ ] Tests with a fake LLM adapter covering valid, invalid and unavailable responses.

## Plan
Write when picked up. Depends on the Alembic ticket for the schema change.

## Implementation Log

## Deviations
