---
type: feature
owner: claude
stakes: routine
priority: P2
skill: listening
opened: 2026-11-05
---

# Meeting listening practice

**Blocked by:** [cloud deploy](../ready/20261105_cloud_deploy_render_neon_groq.md)
(TTS and LLM providers) and [split workspace UI](../ready/20261105_split_workspace_ui.md).

## Context
Listening is a priority skill; today only single-sentence dictation exists. Short
generated meeting dialogues (two or three speakers, 45–90 seconds) built around
the owner's due vocabulary and phrases train following real discussions.

## Acceptance Criteria
- [ ] Plugin `listening.meeting`: LLM writes a short dialogue around 3–5 target items (strict JSON, labelled AI-generated); TTS renders it with distinct voices where the provider allows.
- [ ] Exercises: 3 comprehension questions (gist, detail, intent) and one gap-fill on a target phrase.
- [ ] Playback speed 0.8× / 1× and transcript revealed only after answering.
- [ ] Generated audio cached per exercise with a size cap, or regenerated on demand — decide and record.
- [ ] Tests with fake adapters; grading deterministic.

## Implementation Log

## Deviations
