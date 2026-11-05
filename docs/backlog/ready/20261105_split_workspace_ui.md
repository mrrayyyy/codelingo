---
type: refactor
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Split the workspace UI into per-page components

## Context
`frontend/components/workspace.tsx` holds all six pages (dashboard, vocabulary,
repositories, review, practice, settings) in one client component with 33
`useState` hooks; several lines exceed 2,000 characters (measured 2026-11-05 with
`awk 'length > 400'`). Every Phase 1–3 feature (daily session, PWA, speaking
simulator, listening) adds screens here. Splitting first makes those changes
reviewable and keeps regressions local.

No behaviour change is intended.

## Acceptance Criteria
- [ ] One component per page under `frontend/components/pages/`, plus shared pieces (import dialog, word drawer, toast).
- [ ] i18n strings out of inline `t(en, vi)` calls into a small dictionary module.
- [ ] No source line over 160 characters in `frontend/components/`.
- [ ] Playwright flow passes unchanged; screenshots of each page before/after look the same.

## Plan
### Before
- [ ] Read `frontend/node_modules/next/dist/docs/` sections on client components and routing for this Next.js version
- [ ] Capture before-screenshots of all six pages (Playwright, `docs/tmp/`)
### Split
- [ ] Extract shared state/data loading into a hook (`frontend/lib/use-workspace.ts`)
- [ ] Move each page into `frontend/components/pages/<page>.tsx`
- [ ] Move dialogs/drawers into `frontend/components/`
- [ ] Move strings into `frontend/lib/i18n.ts`
### Verify
- [ ] typecheck, build, `npm run test:e2e` against `scripts/dev.py`
- [ ] After-screenshots compared with before
- [ ] Decide whether pages become App Router routes (record in Deviations or a ledger idea)

## Implementation Log

## Deviations
