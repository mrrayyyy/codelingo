# Protocol

The working contract for anyone — the owner or an agent (Claude Code,
Gemini/Antigravity) — working in this repository. Rules live here rather than in
an agent entry file, so every agent follows the same ones and a rule changes in
one place.

**Agent entry files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) hold no rules of
their own beyond pointers and routing.** A rule that exists in only one agent's
file is a bug: move it here.

Adapted on 2026-11-05 from the owner's AIOps workspace protocol, trimmed for a
single-developer application repository (no infrastructure, Vault or cluster
rules).

| Protocol | Covers |
| :--- | :--- |
| [NAVIGATION.md](NAVIGATION.md) | where every kind of fact lives — read before guessing |
| [EXECUTION.md](EXECUTION.md) | autonomous vs gated actions, commit and push policy, blast radius |
| [KANBAN.md](KANBAN.md) | how work is tracked — `docs/backlog/`, status by directory |
| [LEDGER.md](LEDGER.md) | how findings are captured — `docs/ledger/`, filed in the turn |
| [DOC_SYNC.md](DOC_SYNC.md) | work that changes behaviour changes the docs, same ticket |
| [VERIFICATION.md](VERIFICATION.md) | don't guess; facts carry dates; a green result is not a verified fix |
| [SECRETS.md](SECRETS.md) | this repository is public — what may never enter it |

Enforcement of the dated and stale parts is
[docs/runbooks/housekeeping.md](../runbooks/housekeeping.md), run on request.

## Reading order

New session: **NAVIGATION** → **EXECUTION** → **SECRETS**, then **KANBAN** before
starting non-trivial work.

## Language

Code, comments, commit messages and these docs are English (they double as
reading practice). Conversation with the owner is Vietnamese. Keep technical
terms intact in both.

## Changing a protocol

Do not rewrite a rule unilaterally. File `type: protocol-friction` in
`docs/ledger/open/`, citing the task where the rule cost time or blocked
legitimate work, and let the owner decide. Each rule names the failure it exists
to prevent, so it can be argued with against evidence.
