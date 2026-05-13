# Slack notification protocol

Default channel: **#marketing-agents** (configurable via the `SLACK_WEBHOOK_URL` env var — point the webhook at whatever channel you want).

## When agents post

| Trigger | Who | What |
|---|---|---|
| Slot started | CMO | "Starting <slot>: <tasks>" |
| Slot completed | CMO | "Done <slot>. <bullet summary>. Output: <link>" |
| Subagent finished | each subagent | "<headline metric> + 1-line action" |
| Subagent blocked | each subagent | "Blocked on <reason>. Need: <ask>" |
| Anomaly detected | any | "<market> <metric> <delta> — investigating" |
| Nightly insights ready | performance-reviewer | top-3 insights + link |

## Format

- One message per event. No threads unless replying to a specific message.
- Always identify yourself with `--agent "<Agent Name>"` (e.g., "CMO", "Meta Ads", "Email").
- Lead with the KPI/result, never the process.
- Link to file outputs with full path (use absolute `file://` URIs for browser-openable HTML).

## Posting

Use the direct webhook script — **not** the Slack MCP (unregistered for headless runs; prefer direct REST):

```bash
python3 scripts/slack_post.py --agent "<Name>" --message "<text>"
# or for multi-line / formatted messages:
python3 scripts/slack_post.py --agent "<Name>" --stdin <<'EOF'
... message body ...
EOF
```

The script:
- Loads `SLACK_WEBHOOK_URL` from `.env` and posts to whichever channel the webhook is wired to.
- Auto-prefixes the message with `*[<Name>]*` so the source is visible.
- Returns exit 0 on success, exit 1 on failure (after logging to `data/slack_failed_messages.log`).

Examples (the `*[X]*` prefix is added automatically — don't double-prefix):
```
*[CMO]* Starting Mon 09:00 slot — content-strategist refreshing keywords
*[Email]* Open rate 38.2% (+4pp WoW). Action: scale winning subject line to other markets.
```

On webhook failure, the script appends to `data/slack_failed_messages.log` and exits non-zero. Agents must not block on Slack — log and continue.

## What NOT to post

- Routine "starting work" without tasks
- Long log dumps (link to file instead)
- Per-API-call status (only aggregate result)
