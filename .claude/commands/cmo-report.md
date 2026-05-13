---
allowed-tools: Bash, Read, Write, Agent, Glob, Grep
description: Run a cross-channel CMO performance report
argument-hint: [weekly|monthly]
---

## Task

Run CMO **report mode** per the instructions in `AGENTS.md`.

Argument: $ARGUMENTS (defaults to "weekly" if empty)

Steps:
1. Map argument to days: `weekly` → 7, `monthly` → 30. If empty, use 7.
2. Check `data/ga4_all_markets.json` and `data/store_all_markets.json`. If both exist and their `pulled_at` timestamp covers the requested date range (or was pulled within the current session), reuse them. Otherwise run your GA4 and store puller scripts (brand-specific — not included in this repo; bring your own to `scripts/`).
3. Read the resulting JSON files from `data/`.
4. Spawn all 6 channel subagents in parallel via the Agent tool using their `subagent_type`. Each brief must include date range, markets (all configured), and any cross-channel context you see in the GA4/store data.
5. Synthesize into the report structure defined in `AGENTS.md` (Report mode).
6. Write to `outputs/cmo-report-YYYY-MM-DD.md`.
7. Return the report path and a short summary to the user.
