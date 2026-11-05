---
type: feature
owner: claude
stakes: routine
priority: P2
skill: speaking
opened: 2026-11-05
---

# Stand-up and meeting speaking simulator

**Blocked by:** [cloud deploy](../ready/20261105_cloud_deploy_render_neon_groq.md)
(needs a working Groq STT/LLM/TTS configuration) and
[split workspace UI](../ready/20261105_split_workspace_ui.md).

## Context
Speaking in meetings is the owner's top skill goal. Today the app has read-aloud
only, scored by transcript agreement. A short, turn-based role-play uses the
existing adapters: the app (as a scrum master or reviewer) asks a question by
TTS; the owner answers by voice; STT transcribes; the LLM returns feedback and a
more natural version, which the owner then shadows.

## Acceptance Criteria
- [ ] New plugin `speaking.standup` on the existing contract (`backend/app/contracts.py`, `shared/plugins.ts`).
- [ ] Scenarios: daily stand-up, explaining a blocker, asking for clarification, giving a status update in a review. Prompts use the owner's own vocabulary and phrases.
- [ ] 3–5 turns per session; each turn returns: transcript, 1–3 corrections, a natural rewrite, useful phrases — strict JSON, labelled as AI feedback.
- [ ] Shadowing step: TTS plays the rewrite; owner repeats; transcript agreement shown (labelled, not a pronunciation score).
- [ ] Audio is not stored; only transcripts and feedback persist.
- [ ] Tests with fake STT/LLM/TTS adapters.

## Implementation Log

## Deviations
