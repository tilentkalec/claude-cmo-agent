# YourBrand Marketing Agents

## Business Context

<!--
Replace this section with a tight description of your business. This is the
top-of-context for every CMO and subagent run — keep it terse and high-signal.
Recommended structure:
-->

**YourBrand** is a [one-sentence description of what you sell and to whom].

- **Markets:** see `.claude/rules/markets.md` for the canonical list
- **Business model:** [subscription / one-time / marketplace / etc.]
- **Marketing budget:** [annual spend ballpark]
- **Primary goal:** [the one number you're trying to move]

## Operator

The operator running this system is the de facto CMO. Agents should treat them as
a peer operator — direct, strategic, no fluff. Skip basic marketing explanations
unless asked.

## Communication Style

- English by default (unless producing market-specific content)
- Direct, strategic, no fluff
- KPIs before description — every analysis leads with a number
- Localize content to the configured markets per `.claude/rules/markets.md`

## Connected Tools (MCP)

Configure whichever of these your operator account has connected:
- **Klaviyo** — email marketing, flows, segmentation, campaigns
- **Google Sheets** — data, reporting templates, content calendars
- **Google Drive** — shared assets, documents, briefs
- **Gmail** — outreach, notifications
- **Google Calendar** — content scheduling, campaign timelines
- **Slack** — internal comms, notifications, alerts
- **Notion** — knowledge base, SOPs, campaign briefs
- **Canva** — creative assets, ad visuals
- **YouTube** — video content, channel management
- **Zapier** — automation glue between tools
- **Supabase** — data storage, analytics backend
- **Vercel** — landing pages, web properties
- **Google Ads** — search/display campaign management

For account-scoped APIs (Klaviyo, Meta, Google Ads) where MCP can only attach to
one account at a time, prefer direct REST calls from `scripts/` so you can hit
multiple accounts in one run.

## Seasonality

See `.claude/rules/seasonality.md`. Rewrite the calendar + worked examples there
to match your business cycle — the included file is an ed-tech example.

## Project Structure

```
$REPO_ROOT/                  # set this to wherever you cloned the repo
├── CLAUDE.md                # this file — top-level context
├── AGENTS.md                # CMO orchestrator + agent-spawning logic
├── README.md
├── LICENSE
├── .env.example             # copy to .env, fill in secrets
├── .gitignore
├── .claude/
│   ├── agents/              # 7 channel subagent definitions
│   ├── rules/               # project-wide invariants (KPIs, markets, voice, ...)
│   ├── commands/            # slash commands for CMO modes
│   └── agent-memory/        # per-agent notes.md (gitignored)
├── scripts/                 # cron runner, slack poster, insights→HTML, your data pullers
├── data/                    # trackers + JSON outputs from data pullers (gitignored)
├── docs/
│   └── strategy/
│       ├── weekly-plan.md   # written by CMO Re-plan mode
│       └── insights/        # daily insights md+html from performance-reviewer
└── outputs/                 # CMO reports, plans, agent-overrides (gitignored)
```

## Agent Architecture

See `AGENTS.md` for the full orchestrator definition. Key points:
- **CMO logic is in the orchestrator** (no separate analytics skill)
- **Subagents get spawned** when tasks involve 2+ channels, are data-heavy, or span multiple markets
- **Single-channel tasks** are handled inline without spawning agents
