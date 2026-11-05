---
type: infra
owner: claude
stakes: irreversible
priority: P1
opened: 2026-11-05
---

# Deploy the cloud profile (Render + Neon + GitHub Actions + Groq)

## Context
The cloud profile ([ADR 0001](../../decisions/0001-cloud-first-free-tier.md),
[guide](../../cloud-deployment.vi.md)) has never been deployed. The owner wants
to use CodeLingo daily without running anything locally. Account creation and
secret entry need the owner's browser; Claude prepares, verifies and documents.

Should follow the Alembic ticket so the first hosted schema is migration-managed.

## Acceptance Criteria
- [ ] The hosted app loads behind Basic Auth on a phone and a laptop.
- [ ] Sample import completes through GitHub Actions; vocabulary and review work.
- [ ] Review history survives a Render restart (data in Neon).
- [ ] Groq TTS/STT/LLM either work or show a clear "not configured" state.
- [ ] `docs/verification.md` records the dated evidence; free-tier facts in the guide are re-verified and dated.

## Plan
### Prepare (Claude, local)
- [ ] Re-verify free-tier facts in `docs/cloud-deployment.vi.md` against current Render, Neon, GitHub, Groq docs; date them
- [ ] Confirm Groq model names in `.env.cloud.example` still exist; update if not
- [ ] Build `Dockerfile.cloud` in CI (add a job) instead of locally
### Accounts and secrets (owner)
- [ ] `[user]` Create the Neon project; keep the connection string private
- [ ] `[user]` Create a fine-grained GitHub token limited to `mrrayyyy/codelingo`, Actions: write
- [ ] `[user]` Create the Render service from `render.yaml`; enter secrets in the Render dashboard
- [ ] `[user]` Add `CODELINGO_URL` and `CODELINGO_API_KEY` as GitHub Actions secrets
- [ ] `[user]` Optional: Groq API key in Render
### Verify (Claude, with the owner)
- [ ] `[gate]` First deploy; check `/api/health`
- [ ] Sample import end-to-end; review a card; restart; review persists
- [ ] Measure cold-start time after idle; record it for the PWA ticket
- [ ] Doc sync: verification.md, cloud guide; move `20261105_pwa_daily_session` to `ready/`

## Blast Radius
- Creates hosted accounts and secrets; a leaked `API_KEY`, `WORKSPACE_PASSWORD`
  or GitHub token exposes the owner's learning data or lets someone trigger
  Actions runs. Recovery: rotate in Render/GitHub, redeploy.
- After this, **a push to `main` is a deploy** (Render auto-deploy). A broken
  commit takes the app down until fixed; recovery is a revert commit.
- Neon holds the only copy of review history. Schema changes after this point
  are `irreversible` tickets with a backup step (`pg_dump`) first.
- Repositories imported here pass through public-repo Actions runners; logs print
  only counts, but import only public or own code (SECRETS.md).

## Implementation Log

## Deviations
