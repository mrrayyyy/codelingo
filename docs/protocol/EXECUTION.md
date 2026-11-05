# Execution

How work is carried out in this repository and against the hosted services
(Render, Neon, GitHub, Groq).

## Four steps

1. **Investigate** — read code and docs, run tests, reproduce. Autonomous.
2. **Root-cause** — name the exact mechanism before changing code.
3. **Change and verify locally** — edit, then run the
   [pre-push checks](#pre-push-checks). A change is not done because it compiles;
   see [VERIFICATION.md](VERIFICATION.md).
4. **Commit and push** — per the policy below.

## Autonomous vs gated

**Autonomous** (no confirmation): reading, local edits, running tests and builds,
local dev servers, creating or moving tickets and ledger entries, **commits on
`main`, and pushes to `origin main` that pass the pre-push checks**
([ADR 0003](../decisions/0003-public-repo-auto-commit-push.md), owner, 2026-11-05).

**Gated** — stop, state *action, target, effect, recovery*, and wait for an
explicit yes:

- `git push --force`, history rewrites, deleting branches or tags;
- changing GitHub repository settings, visibility, secrets or Actions variables;
- creating, changing or deleting Render services, environment variables or Neon
  projects/branches;
- any schema migration or data deletion against the hosted database;
- deleting local learning data (`.data/`, `docker compose down -v`);
- adding a paid service or anything that could incur a charge;
- importing a repository the owner does not own (see [SECRETS.md](SECRETS.md)).

Approval covers the action asked about, not the next one like it.

## Commit and push policy

- **Commit after every meaningful step**, in the same turn, without being asked:
  a ticket opened or moved, a ledger entry filed, a doc updated, a code change
  that passes its checks. Many small commits beat one large one.
- **Stage paths explicitly** — never `git add -A` / `git add .` once history
  exists. Another session's work in the tree is not yours to commit.
- **One subject per commit**, Conventional Commit style
  (`feat(practice): …`, `fix(api): …`, `docs(backlog): …`, `chore: …`).
- **Push to `origin main` after the pre-push checks pass.** Before pushing, check
  `git log origin/main..HEAD` so you know what rides along.
- Once Render auto-deploys from `main`, **a push is a deploy**. A commit carrying
  a schema change, a data migration or a settings change is `stakes:
  irreversible` and is gated even though pushing is otherwise autonomous.

Why: AIOps lost days of design work that existed only in an uncommitted working
tree. In a public repository the same rule also makes every change reviewable on
GitHub.

### Pre-push checks

Run what the change touches; all of them when unsure:

```sh
.venv/bin/python -m pytest backend/tests -q      # backend
npm --prefix frontend run typecheck              # frontend types
python3 tools/docs/check_doc_links.py            # docs links
python3 tools/docs/scan_secrets.py               # nothing secret staged
```

Browser tests and the production build run in CI on every push. A red CI run on
`main` is fixed before new feature work.

## Blast radius is written, not discussed

For `stakes: irreversible` tickets, the consequences go in the ticket's
`## Blast Radius` **before** execution: what is unrecoverable, what else the
change touches, what a bad outcome looks like. Confirmation alone is not
enough — it never forced anyone to work out the consequences first.

## Do not re-own a decision

When the owner has decided something, do not defer or reshape part of it on your
own judgment and record that in a commit message. Say so and let them choose.
