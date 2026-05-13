# Markets — localization invariants

> **This file is an example multi-market setup. Replace the table and per-market rules below with your own markets.** The structure — a single canonical source for market codes, languages, currencies, and per-market term/script overrides — is what every subagent reads at session start.

Always plural, always all markets configured here unless the brief specifies a subset.

| Code | Country | Language | Currency | Category term (use exactly) | Notes |
|---|---|---|---|---|---|
| SI | Slovenia | Slovenian | EUR | matura | Primary market. Domain needs `www.` prefix. |
| HU | Hungary | Hungarian | HUF | **érettségi** | Never write "matura" for HU. |
| PL | Poland | Polish | PLN | matura | Domain is `edumatura.pl` (not `ematura.pl`). |
| BG | Bulgaria | Bulgarian | BGN | матура | Cyrillic in copy. |
| GR | Greece | Greek | EUR | πανελλήνιες | Domain is `epanellinies.gr`. |

## Operational rules

- Default to all configured markets in any analysis, brief, or content plan.
- When data fails for a market, write **"data unavailable for <market>"** — never narrate around the gap.
- LTV varies by market; pull from `data/ltv_by_market.json` if available (do not hardcode).
- Per-market language/script/term overrides are hard fails if violated in localized copy.
