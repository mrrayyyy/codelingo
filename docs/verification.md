# Verification record

## Base MVP

- First import → extract → flashcard/FSRS API suite: 32 passing tests.
- Expanded extraction/plugin/API suite: 44 passing tests before managed deployment support.
- Next.js production build and both self-hosted Docker image builds succeeded.
- Two Chromium browser tests passed: import sample → vocabulary search → Monaco/highlights → FSRS review → reading grade → saved settings → Vietnamese switch; mobile overflow/import validation/Escape dismissal.
- Dependency audit reported zero vulnerabilities after rebuilding Monaco from ESM with the DOMPurify override.

## Managed cloud profile

- Python/API suite including cloud dispatch, callbacks, provider adapters, limits, and no-NLP web startup: 53 passing tests.
- TypeScript checking passed.
- Cloud access test passed: Basic Auth, protected data endpoints, machine-key route scoping, and public health check.
- Cloud speech/LLM adapters use mocked responses in tests; live Groq calls require the account API key and model access.
- Managed cloud deployment has not been executed: Render/Neon connections and hosted secrets are not configured. No live hosted URL is claimed. The cloud Dockerfile has not been built locally after the user's request to avoid local workloads; its build is intended to run on Render.
- Local preview processes and Compose services were stopped after the deployment preference changed. The checked-in GitHub Actions CI workflow runs future verification on hosted runners.
