# 0001. Cloud-first on free managed services

- Status: accepted
- Date: 2026-10-27 (recorded 2026-11-05)
- Decided by: owner

## Context
The MVP was designed as a self-hosted Docker Compose stack (PostgreSQL, Redis,
ARQ worker, local Piper/Whisper/Ollama). The owner does not want heavy workloads
or local models on their personal computer, and wants to use the app daily
without running anything.

## Decision
The preferred deployment is the cloud profile described in
[cloud-deployment.vi.md](../cloud-deployment.vi.md):

- Render (free web service) runs the Next.js app and FastAPI in one container
  (`Dockerfile.cloud`);
- Neon stores learning data;
- GitHub Actions runs tree-sitter + spaCy extraction on demand (`extract.yml`,
  `JOB_MODE=github_actions`), receiving only a job ID and calling back;
- Groq provides optional TTS, STT and LLM.

The Compose profile and the `inline` job mode remain for development and tests.
All profiles share the schema, plugin contracts, extractor and FSRS logic.

## Alternatives considered
- Compose on a VPS — costs money and needs maintenance.
- Render's free PostgreSQL — expires, unsuitable for long-lived learning data.
- Vercel for the whole app — function payload limits break ZIP upload.

## Consequences
- Imports are slower (runner start-up) but cost nothing and keep the laptop idle.
- Free-tier behaviour (idle spin-down, quotas) shapes the UX; see the roadmap.
- Three job modes (`inline`, `arq`, `github_actions`) must be kept working; see
  [the ledger entry on simplifying them](../ledger/open/idea_20261105_simplify_job_modes.md).
- As of 2026-11-05 the cloud profile has **not** been deployed
  ([verification.md](../verification.md)).
