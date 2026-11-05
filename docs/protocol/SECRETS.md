# Secrets and privacy

**This repository is public** (`ray-dd1510/codelingo`, owner decision
2026-11-05). Everything committed — code, tickets, ledger entries, commit
messages — is readable by anyone, permanently, even after deletion.

## Never commit

- API keys, tokens, passwords, connection strings with credentials (`.env` is
  git-ignored; keep it that way);
- the hosted app URL together with anything that authenticates to it;
- real vocabulary, context sentences or source snippets extracted from a
  private or employer repository;
- names of internal systems, hosts, customers or colleagues from the owner's
  workplace — in tickets and ledger entries too. Describe them generically
  ("a work repository").

Secrets live in `.env` locally and in Render / GitHub Actions secret settings
when hosted. Changing hosted secrets is gated ([EXECUTION.md](EXECUTION.md)).
Never print a secret value into chat, logs or files.

## Before every commit

```sh
python3 tools/docs/scan_secrets.py                       # staged changes
git diff origin/main..HEAD | python3 tools/docs/scan_secrets.py -   # anything already committed
```

It prints matches and exits 1. Test fixtures that deliberately contain fake
secrets carry the marker `fake-secret-fixture` on the same line or the line
above so the scanner skips them; never use the marker on a real value.

If a real secret is ever pushed: rotate it first (the old value is compromised
the moment it is public), then clean history as a gated action.

## Employer code

The cloud profile sends imported repositories to GitHub Actions runners, stores
context sentences in Neon, and can send exercise text to Groq. Importing code
the owner does not own may break their employer's policy. Until the owner
decides otherwise
([ledger entry](../ledger/open/process-gap_20261105_employer_code_privacy.md)),
agents import only public repositories or the bundled sample.
