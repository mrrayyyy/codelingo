---
type: feature
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Installable PWA and a 10-minute daily session

**Blocked by:** [cloud deploy](../ready/20261105_cloud_deploy_render_neon_groq.md)
(needs the hosted URL and a measured cold-start time) and
[split workspace UI](../ready/20261105_split_workspace_ui.md).

## Context
Practice is spread over separate pages; a habit needs one button. Render's free
tier spins down when idle, so the first open of the day can be slow. An
installable PWA with a cached shell shows the session immediately and a clear
"waking the server" state instead of a blank page.

## Acceptance Criteria
- [ ] Installable on iOS/Android home screen (manifest, icons, service worker for the static shell only — no learning data cached in the browser).
- [ ] "Today" screen: due reviews (cap 15) → 1 listening item → 1 speaking item → summary, about 10 minutes.
- [ ] Cold start shows progress text, not an error; retries until the API answers.
- [ ] Dashboard shows per-skill minutes and attempts for the last 7 days.

## Implementation Log

## Deviations
