#!/bin/zsh
# Headless invocation of the CMO in slot mode.
# Triggered by launchd (com.example.cmo-slot).
#
# launchd uses the system's local time. Set the firing schedule in the
# accompanying .plist file. Defaults:
#   Daily AM batch: 09:00 every day (Mon–Sun).
#   Sunday additionally: 18:00 Re-plan mode.
# See docs/strategy/weekly-plan.md for the weekly cadence.
#
# The CMO's Boundaries (AGENTS.md) prevent spend changes / external publishes,
# so --dangerously-skip-permissions is acceptable here: the agent's own rules
# are the safety layer, not interactive prompts.

set -e

# Resolve repo root: env override > script's parent dir.
REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$REPO_ROOT"

LOG_DIR="${LOG_DIR:-/tmp}"
TS=$(date '+%Y-%m-%d %H:%M:%S %Z')
DOW=$(date +%u)   # 1=Mon ... 7=Sun
HOUR=$(date +%H)

# Pick the prompt for this firing.
# Sunday at 18:00 → Re-plan mode. Everything else (including Sun 09:00) → daily AM batch.
if [[ "$DOW" == "7" && "$HOUR" == "18" ]]; then
  PROMPT="You are the CMO. Today is Sunday 18:00 — execute Re-plan mode (see AGENTS.md). Sunday's 09:00 AM batch has already produced today's insights file; read it alongside the rest of the week. Read last 7 days of docs/strategy/insights/*.md, outputs/agent-overrides.md, and the current docs/strategy/weekly-plan.md. Conservatively rewrite docs/strategy/weekly-plan.md for the upcoming week. Run memory hygiene per .claude/rules/memory-hygiene.md. Post the standard Slack summary."
  LOG="$LOG_DIR/cmo-replan.log"
else
  PROMPT="You are the CMO. Execute today's AM batch per AGENTS.md slot mode + docs/strategy/weekly-plan.md. Runs every day including weekends. Sequence: (1) if Monday, run weekly kickoff first; (2) spawn email + meta-ads + google-ads in PARALLEL — each pulls last-7-day vs prior-7-day data with recommendations (on weekends, channel agents must compare Sat-to-prior-Sat or Sun-to-prior-Sun, not weekend-to-weekday); (3) wait for all three, then spawn performance-reviewer to synthesize into docs/strategy/insights/YYYY-MM-DD.md (and .html via scripts/insights_to_html.py); (4) post the CMO daily rollup to Slack via scripts/slack_post.py reading the insights file just written. Start by reading yesterday's insights file if present."
  LOG="$LOG_DIR/cmo-am.log"
fi

echo "=== $TS firing (DOW=$DOW) ===" >> "$LOG"

# Retry on transient errors (529 overload, 503, network blips).
# 3 attempts with exponential backoff: 30s, 120s, 300s.
ATTEMPT=0
MAX_ATTEMPTS=3
BACKOFFS=(30 120 300)
SUCCESS=0
while (( ATTEMPT < MAX_ATTEMPTS )); do
  ATTEMPT=$(( ATTEMPT + 1 ))
  echo "--- attempt $ATTEMPT/$MAX_ATTEMPTS at $(date '+%H:%M:%S') ---" >> "$LOG"
  if claude --dangerously-skip-permissions -p "$PROMPT" >> "$LOG" 2>&1; then
    SUCCESS=1
    break
  fi
  EXIT=$?
  echo "--- attempt $ATTEMPT failed (exit $EXIT) ---" >> "$LOG"
  if (( ATTEMPT < MAX_ATTEMPTS )); then
    SLEEP=${BACKOFFS[$ATTEMPT-1]}
    echo "--- sleeping ${SLEEP}s before retry ---" >> "$LOG"
    sleep "$SLEEP"
  fi
done

if (( SUCCESS == 1 )); then
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') done (after $ATTEMPT attempts) ===" >> "$LOG"
else
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') FAILED after $MAX_ATTEMPTS attempts ===" >> "$LOG"
  exit 1
fi
