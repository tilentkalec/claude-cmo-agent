---
allowed-tools: Bash, Read, Write, Agent, Glob, Grep, WebFetch, WebSearch
description: Plan marketing strategy for a specific goal
argument-hint: "<goal>"
---

## Task

Run CMO **plan mode** per the instructions in `AGENTS.md`.

Goal: $ARGUMENTS

Steps:
1. Pull current state: GA4 + store data (run your puller scripts or reuse cached). Get recent channel perf from subagents if needed.
2. Apply the CMO decision framework: seasonality (see `.claude/rules/seasonality.md`), budget, CAC efficiency, market-weight.
3. Propose channel allocation + sequenced actions.
4. Spawn relevant channel subagents to write concrete briefs for their piece of the plan.
5. Write unified plan to `outputs/plan-<goal-slug>-YYYY-MM-DD.md`.
6. Return the plan path and a short summary.
