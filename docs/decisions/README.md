# Decisions (ADRs)

The record of *why* — decisions behind the current shape of CodeLingo, kept apart
from [architecture.md](../architecture.md), which records *what exists*.

Consult the relevant ADRs before proposing a change to deployment, data model,
privacy boundaries, or the working protocol. The goal is to never re-litigate a
settled decision and never silently contradict one.

## When to write one

When a decision is non-obvious, was debated, or would surprise a new reader —
"why GitHub Actions does NLP instead of a worker", "why the repo is public".
Routine changes belong in a ticket and a commit message.

## Format

One file per decision, `NNNN-short-title.md`, numbered sequentially. Copy
[0000-template.md](0000-template.md).

## Status values

- `proposed` — under consideration
- `accepted` — decided and reflected in the code
- `superseded by NNNN` — replaced; keep the old file

## Index

| ADR | Status | Decision |
| :--- | :--- | :--- |
| [0001](0001-cloud-first-free-tier.md) | accepted | Cloud-first on free managed services; self-hosted profile kept for development |
| [0002](0002-docs-as-code-workflow.md) | accepted | Docs-as-code task and documentation workflow adapted from AIOps |
| [0003](0003-public-repo-auto-commit-push.md) | accepted | Public repository; agents commit and push to `main` automatically |
