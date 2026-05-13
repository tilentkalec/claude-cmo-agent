# KPI definitions — canonical

All agents reference these definitions. Never redefine inline.

## Acquisition
- **Sessions** — GA4 sessions
- **Conversions** — GA4 `purchase` events (or your primary conversion event)
- **Conversion rate** — conversions / sessions
- **CAC** — channel spend / new paid customers from that channel (attribution: GA4 last-non-direct)
- **ROAS** — revenue / spend (use 30-day rolling for ads, lifetime for organic content)

## Email (Klaviyo)
- **Open rate** — Apple-MPP-adjusted where possible; flag when not
- **Click rate** — unique clicks / delivered
- **Conversion rate** — placed orders / delivered (Klaviyo native)
- **Revenue per recipient** — attributed revenue / recipients

## Ads
- **CTR** — clicks / impressions
- **CPC** — spend / clicks
- **Frequency** — impressions / reach (Meta only; flag >2.5)

## Content / SEO
- **Impressions / clicks** — GSC
- **Avg position** — GSC, weighted by impressions
- **Organic conversions** — GA4 source/medium = `*/organic`

## Cross-channel
- **Blended CAC** — total marketing spend / total new paid customers
- **Channel mix** — % of conversions by channel × market

## Comparison windows
- Default WoW for weekly reports, MoM for monthly, YoY when seasonality applies
- Always state the comparison window explicitly in headlines

## Worked calculations

### CAC (Meta, last 7 days)
- Meta spend (Meta API): €312
- New paid customers from `meta / cpc` (GA4 last-non-direct): 14
- **CAC = 312 / 14 = €22.29**
- Headline format: "Meta CAC €22.29 (last 7d, GA4 last-non-direct attribution)"

### ROAS (Google Ads, 30-day rolling)
- Google spend (Google Ads API): €1,840
- Revenue from `google / cpc` (store, 30d): €4,968
- **ROAS = 4968 / 1840 = 2.7×**
- Headline format: "Google ROAS 2.7× (30d rolling, store revenue)"

### Email revenue per recipient (Klaviyo campaign)
- Recipients: 4,200
- Attributed revenue (Klaviyo native): €126
- **RPR = 126 / 4200 = €0.030 per recipient**
- Headline format: "Campaign RPR €0.030 (Klaviyo native attribution)"

### Blended CAC (all channels, last 30 days)
- Total marketing spend: €3,420 (Meta + Google + content + email + tool stack)
- Total new paid customers (store `payment_complete` events, all sources): 168
- **Blended CAC = 3420 / 168 = €20.36**
- Headline format: "Blended CAC €20.36 (all channels, 30d, store)"

### GSC weighted average position (top 10 KWs)
- Sum of (position × impressions) across 10 KWs = 18,420
- Sum of impressions = 4,100
- **Weighted avg position = 18420 / 4100 = 4.49**
- Always weight by impressions — a position-1 KW with 50 impressions matters less than a position-6 KW with 800.

## Source-of-truth ordering when sources disagree

For revenue attribution: **Klaviyo native** > **GA4 last-non-direct** > **store `payment_complete`**. Klaviyo's own attribution is most accurate for email; GA4 catches multi-channel paths; the store is ground truth for *total* revenue but blind to source. Always state which on revenue claims.

For ad spend: **platform native** (Meta API, Google Ads API) > GA4 inferred > store. Platform-native is canonical for spend.

For sessions: **GA4** is canonical; nothing else measures sessions.
