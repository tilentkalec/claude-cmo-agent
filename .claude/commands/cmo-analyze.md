---
allowed-tools: Bash, Read, Write, Agent, Glob, Grep, WebFetch, WebSearch
description: Ask the CMO a targeted cross-channel question
argument-hint: "<question>"
---

## Task

Run CMO **analyze mode** per the instructions in `AGENTS.md`.

Question: $ARGUMENTS

Steps:
1. Interpret the question. Decide which subagents are relevant — not always all 6.
2. Pull only the GA4/store slices needed for context (via your puller scripts in `scripts/`, or reuse cached data in `data/` if fresh).
3. Brief the selected subagents with the specific question + relevant context via the Agent tool.
4. Synthesize a focused inline answer. Do not write to a file unless the user asks.
