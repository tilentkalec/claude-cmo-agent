# claude-cmo-agent

An AI-native marketing operating system built on Claude Code. A CMO orchestrator that fans out to channel subagents (Meta, Google, email, content, social) and runs daily on a launchd schedule to produce a Slack-posted cross-channel report.

## Why this exists

I run this against my actual ed-tech brand across 5 markets. The brand-specific data pullers, copy samples, and memory live in a private repo. This is the brand-agnostic skeleton — the orchestrator, the subagent contracts, the rules, the cron runner — extracted as a reference for other operators building agent systems on Claude Code.

## Architecture

```
                       ┌─────────────────────────────┐
                       │  launchd cron               │
                       │  Daily 09:00 → AM batch     │
                       │  Sunday 18:00 → Re-plan     │
                       └──────────────┬──────────────┘
                                      │
                                      ▼
                       ┌─────────────────────────────┐
                       │  CMO orchestrator           │
                       │  (AGENTS.md)                │
                       │  • Pulls GA4 + store data   │
                       │  • Reads rules + memory     │
                       └──────────────┬──────────────┘
                                      │ parallel spawn
        ┌───────────┬─────────┬───────┼───────┬─────────┬───────────┐
        ▼           ▼         ▼       ▼       ▼         ▼           ▼
   content-       content-  social-  meta-  google-  email     performance-
   strategist     producer  media    ads    ads               reviewer
        │           │         │       │       │         │           │
        └───────────┴─────────┴───────┴───────┴─────────┘           │
                                      │                             │
                                      ▼                             │
                               Channel briefs ─────► synthesized ◄──┘
                                                    insights file
                                                    (md + html)
                                                          │
                                                          ▼
                                                   Slack rollup
```

Six channel subagents run in parallel. The performance-reviewer synthesizes their outputs plus the day's tracker rows into a dated insights file (markdown + HTML). The CMO posts a one-message daily rollup to Slack with a `file://` link to the rendered HTML.

## The four modes

- **Report** (`/cmo-report [weekly|monthly]`) — full cross-channel performance review. Spawns all 6 subagents, writes to `outputs/`.
- **Analyze** (`/cmo-analyze "<question>"`) — targeted question. Spawns only the relevant subagents, answers inline.
- **Plan** (`/cmo-plan "<goal>"`) — strategic plan against a goal. Allocates across channels, drops a plan file.
- **Slot** (headless via cron, or "run today's batch") — daily AM execution: parallel email + meta-ads + google-ads, then performance-reviewer, then Slack rollup. Never publishes externally.

Plus **Re-plan mode** on Sundays at 18:00 — rewrites `docs/strategy/weekly-plan.md` from the week's insights and runs memory hygiene across all agents.

## Operating principles

The agent files are structured around six principles drawn from Runbear's prompting guide:

1. **Goals / Boundaries / Constraints framing** — every agent has explicit sections for what it's trying to do, what it never does without confirmation, and the materiality/sample-size rules it operates under.
2. **Restraint > autonomy** — agents return "no material change" rather than padding when nothing moved.
3. **Structured context** — rules in `.claude/rules/` are read at session start by every agent. Single source of truth.
4. **Per-agent memory with hygiene** — each agent appends terse, KPI-anchored entries to its own `notes.md`; CMO archives entries >30 days old on Sundays.
5. **Environment > wording** — the cron, the file layout, and the tracker CSVs do more than any prompt rewrite would.
6. **Channel data boundaries** — subagents own their platform; the CMO owns GA4 + store and passes context down.

## Setup

1. Clone this repo.
2. Copy `.env.example` to `.env` and fill in `SLACK_WEBHOOK_URL` (point the webhook at whichever Slack channel you want — the rules call out `#marketing-agents` but it's just a default).
3. Edit `CLAUDE.md` — fill in the Business Context section with your brand, model, budget, and goal.
4. Edit `.claude/rules/markets.md` with your markets, languages, currencies, and any per-market term/script overrides.
5. Edit `.claude/rules/brand-voice.md` with your voice attributes and per-market sample copy.
6. Edit `.claude/rules/seasonality.md` to match your business cycle (the included file uses ed-tech exam prep as a worked example).
7. Drop your own data-pull scripts (GA4, store/orders, ad platforms) into `scripts/` so the CMO and performance-reviewer can read fresh JSON from `data/`.
8. Optional: install the launchd plist for daily runs.
   ```
   # edit scripts/com.example.cmo-slot.plist — replace <REPO_ROOT> with your absolute path
   cp scripts/com.example.cmo-slot.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.example.cmo-slot.plist
   ```

## What's NOT included

- **Data-pull scripts.** GA4, Woo, Klaviyo, Meta, Google Ads pullers are brand- and stack-specific. The orchestration pattern is the value; bring your own pullers.
- **Finance subagents.** CFO / revenue / expense agents are excluded — they're locale-specific (tax, accounting tooling) and not part of CMO scope.
- **The operator's actual data, memory, weekly plans, and copy samples.** Those live in a private repo.

## License

MIT.

## Credit

Structure inspired by Runbear's [Ultimate Guide to Prompting AI Agents](https://runbear.io/). The Goals / Boundaries / Constraints framing and the "restraint > autonomy" principle come from there.
