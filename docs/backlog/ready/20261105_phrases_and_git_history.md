---
type: content
owner: claude
stakes: routine
priority: P2
skill: reading
opened: 2026-11-05
---

# Learn workplace phrases, and use git history as a source

## Context
Vocabulary is deduplicated by `(lemma, part_of_speech)`, so the app teaches
single words. Workplace English runs on multi-word chunks — "walk me through",
"I'm blocked on", "ship it behind a flag", "let's take this offline". Commit
messages and PR descriptions are the richest everyday source of such prose and
are listed as remaining scope in the README ("git-log/PR extraction").

## Acceptance Criteria
- [ ] Extraction keeps frequent noun chunks and verb-particle phrases (spaCy) alongside lemmas, ranked the same way.
- [ ] A curated seed list of ~150 meeting/stand-up/code-review phrases with Vietnamese meaning, project-authored.
- [ ] ZIP/GitHub imports with `.git` history (bounded: last N commits) contribute commit-message sentences as context.
- [ ] Phrases appear in review and reading exercises; existing word behaviour unchanged.
- [ ] Extraction tests with fixtures for phrases and commit messages.

## Plan
Write when picked up. Check archive limits in `backend/app/imports.py` before reading `.git`.

## Implementation Log

## Deviations
