# Memory hygiene

Per-agent `notes.md` files in `.claude/agent-memory/<agent>/` accumulate every session. Without pruning they decay into stale context that contradicts current state — the well-known "retaining obsolete contextual information" anti-pattern.

This file defines how each agent and the CMO maintain memory health.

## Per-agent rules (apply on every session-end write)

1. **Soft cap: 200 lines.** Before appending, count lines in your `notes.md`. If it would exceed 200 after the new entry, do not delete — flag in your output: `memory at <N> lines — CMO will roll on Sunday`.
2. **Terse, KPI-anchored entries.** Every entry leads with a number or a name, not narrative. ✅ "Email OR 38% Apr 14 — subject 'X' winner, port to other markets" / ❌ "Today we noticed that emails are doing well."
3. **Date every entry.** First token of every entry: `YYYY-MM-DD —`.
4. **Append-only within a session.** Never edit prior entries. If a past entry turned out to be wrong, append a new entry referencing it: `YYYY-MM-DD — correction to YYYY-MM-DD entry: <X> was actually <Y> because <Z>.`
5. **No file paths to ephemeral outputs.** Reference KPIs and decisions, not "see outputs/foo-2026-04-21.md" — those files rot.

## CMO Sunday roll (part of Re-plan mode)

After rewriting `weekly-plan.md` on Sunday at 18:00, the CMO performs memory hygiene across all agents:

1. For each `.claude/agent-memory/<agent>/notes.md` over 200 lines:
   - Move all entries dated >30 days ago to `.claude/agent-memory/<agent>/notes-archive-YYYY-Q<N>.md` (quarterly file, append).
   - The remaining `notes.md` keeps last-30-days entries plus a header line: `<!-- archived through YYYY-MM-DD; see notes-archive-YYYY-Q<N>.md -->`.
2. For the CMO's own `notes.md`: same rule, plus compress decisions older than 30 days into a 5-line summary at the top of that quarter's archive file: *"Q<N>: top 3 wins, top 3 misses, 2 sentences on phase posture."*
3. Entries that contradict current `agent-overrides.md` or current rules: do not archive — append a `<!-- contradicts override on YYYY-MM-DD -->` comment and leave in `notes.md` so the next session sees it (otherwise the agent re-makes the corrected mistake).

## What never gets archived

- The operator's explicit instructions ("operator said X on YYYY-MM-DD") — these stay in `notes.md` indefinitely.
- Anomalies that turned out to be tracking artifacts (so the agent doesn't re-flag them).
- Cross-channel correlations confirmed across 3+ weeks (these become near-rules; consider promoting to `.claude/rules/` instead).

## Anti-patterns

- ❌ Wholesale deletion: never `> notes.md`. Always archive.
- ❌ Editing past entries to "clean them up." History is the point.
- ❌ Letting `notes.md` cross 500 lines. If you see this, the Sunday roll is failing — flag to the operator.
- ❌ Importing old entries from archive back into `notes.md` because they "still feel relevant." If they're relevant, they'll re-emerge from current data.
