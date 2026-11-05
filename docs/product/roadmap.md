# Product assessment and roadmap

Owner goals (confirmed 2026-11-05): a **personal** tool for learning workplace
English, used daily without running anything locally. Skill focus: **speaking**
(meetings, stand-ups), **listening**, **reading/vocabulary**. Priorities for the
next 1–2 months: daily cloud use, workplace English practice, content quality.

## Assessment (2026-11-05)

Evidence: `pytest backend/tests` → 53 passed; `npm run typecheck` → clean;
code read at `codelingo e5d8c8e`.

### Strengths
- **Careful engineering foundations.** Bounded archive handling, secret filtering,
  source never executed, answer keys kept server-side, idempotent and
  stale-protected FSRS reviews, explicit "unavailable" instead of invented data.
- **A real plugin contract** (TypeScript and Python) with five working practice
  plugins — new exercise types slot in without touching the core.
- **Clever free cloud design**: GitHub Actions as an on-demand NLP worker keeps
  both the laptop and the hosted app light.
- **Tests and CI** including a browser flow on hosted runners.

### Gaps that matter for the owner's goals

| # | Gap | Evidence | Effect on daily learning |
| :--- | :--- | :--- | :--- |
| 1 | **Never deployed** | [verification.md](../verification.md): "Managed cloud deployment has not been executed" | The app has never met its only user. Everything else is speculative until it is used daily. |
| 2 | **Almost no meanings, none in Vietnamese** | `lexicon.py`: 33 definitions; `vocab_items` has no Vietnamese field | Most flashcards show "definition unavailable" — the core review loop is weak for a Vietnamese learner. |
| 3 | **Learns words, not workplace phrases** | Dedup key is `(lemma, POS)`; extraction ranks single terms | Meetings run on chunks ("walk me through", "I'm blocked on", "let's take this offline"), not lemmas from identifiers. |
| 4 | **Speaking and listening are thin** | Only dictation and read-aloud; read-aloud scores transcript agreement | The two top-priority skills have no conversational practice. |
| 5 | **UI is one dense component** | `workspace.tsx`: 33 `useState`, lines up to 2,332 chars | Every new practice screen means editing the same file; slows all feature work and invites regressions. |
| 6 | **No schema migrations** | README: "uses SQLAlchemy `create_all`" | The first schema change after real data exists in Neon risks losing review history. |
| 7 | **Three job modes, two deployment profiles** | `config.py` `job_mode`; Compose + Render | Maintenance cost for a single user ([ledger](../ledger/open/idea_20261105_simplify_job_modes.md)). |
| 8 | **Employer code in a public cloud pipeline** | Cloud profile sends imports to Actions/Neon/Groq | Policy risk if work repositories are imported ([ledger](../ledger/open/process-gap_20261105_employer_code_privacy.md)). |
| 9 | **Free-tier idle spin-down** | Render free web services spin down when idle (re-verify at deploy) | A cold start before a 3-minute review kills the habit; needs an installable shell and a graceful loading state. |

### Opinion
The code is ahead of the product. The highest-leverage move is not another
feature but **getting it live and used every day**, then fixing what daily use
exposes: meanings in Vietnamese first, then phrase-level content, then
conversational speaking and listening built on the existing plugin contract. Keep
the scope personal — multi-user, OAuth and plugin isolation from the original v1
list should stay out until the owner wants to share it.

## Roadmap

Status of each ticket is the directory it is in under `docs/backlog/`.

### Phase 0 — Foundations (week 1) · P1
| Ticket | Why now |
| :--- | :--- |
| [Alembic migrations](../backlog/ready/20261105_alembic_migrations.md) | Must exist before real data lands in Neon |
| [Split the workspace UI](../backlog/ready/20261105_split_workspace_ui.md) | Every later feature touches the UI |

### Phase 1 — Live and daily (weeks 1–2) · P1
| Ticket | Why now |
| :--- | :--- |
| [Deploy to Render + Neon + Groq](../backlog/ready/20261105_cloud_deploy_render_neon_groq.md) | Gap 1 |
| [Installable PWA and a 10-minute daily session](../backlog/open/20261105_pwa_daily_session.md) | Gap 9; turns features into a habit |

### Phase 2 — Content quality (weeks 2–4) · P1–P2
| Ticket | Why now |
| :--- | :--- |
| [Vietnamese meanings and better CEFR](../backlog/ready/20261105_vietnamese_gloss_and_cefr.md) | Gap 2 |
| [Workplace phrases and git history as sources](../backlog/ready/20261105_phrases_and_git_history.md) | Gap 3 |

### Phase 3 — Speaking and listening (weeks 4–8) · P2
| Ticket | Why now |
| :--- | :--- |
| [Stand-up speaking simulator](../backlog/open/20261105_standup_speaking_simulator.md) | Gap 4, top skill |
| [Meeting listening practice](../backlog/open/20261105_meeting_listening_practice.md) | Gap 4 |

### Later (not scheduled)
Interview practice, writing variants (Slack/email tone), progress analytics per
skill, phoneme-level pronunciation, multi-user/OAuth. File ideas to the ledger as
`type: idea`; promote them when a phase finishes.

## How to measure progress
Per skill, weekly: minutes practised, attempts, mean score, and FSRS retention
(share of reviews rated Good/Easy). Add these to the dashboard as part of the
daily-session ticket; until then, a ticket's acceptance criteria are the measure.
