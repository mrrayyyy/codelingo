# Verification

## Do not guess

- Do not guess library APIs or configuration fields. Read the installed version's
  docs or source (`frontend/node_modules/next/dist/docs/`, `.venv/lib/...`),
  `--help`, or the error text. Next.js here is newer than most training data.
- Do not guess hosted-service facts (free-tier limits, model names, pricing).
  Check the provider's current docs and record the date.
- When behaviour is uncertain, test it rather than reasoning about it.

## Facts carry a date

A claim someone would act on — a free-tier limit, a model name, a quota, whether
the hosted app is deployed — records when it was last checked, e.g. *"verified
2026-11-05"*. A fact you wrote yourself is not evidence; it needs a date like
anyone else's.

## Learning claims are labelled

This app grades a person's English. Never present an estimate as a
measurement:

- transcript agreement is not pronunciation scoring;
- an LLM's feedback is labelled as an AI estimate;
- an unknown definition is shown as unavailable, never invented;
- estimated CEFR levels are marked as estimated.

A feature that blurs these is a `bug`, even if it looks better.

## Verifying a fix

A change is not verified because a later run was green. Ask what else could
produce that green: was the test exercising the changed path, did the fixture
already contain the answer, is the check a proxy (a 200 status, a non-empty
list) for the thing that matters? Prefer the direct test, and state plainly what
a result does *not* establish.

For UI changes, a typecheck is not verification: run the app or the Playwright
flow and look at the screen that changed.
