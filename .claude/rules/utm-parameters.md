# UTM convention

Every outbound link from email, social, ads, or scheduled posts must use this format.

```
?utm_source={channel}&utm_medium={type}&utm_campaign={slug}&utm_content={variant}&utm_term={market}
```

## Allowed values

- **utm_source**: `klaviyo` | `meta` | `google` | `tiktok` | `instagram` | `youtube` | `linkedin` | `wp` | `manual`
- **utm_medium**: `email` | `cpc` | `cpm` | `social` | `organic` | `referral`
- **utm_campaign**: kebab-case slug, descriptive (`peak-jan-2026-creative-test`, `enrollment-sept-parents`)
- **utm_content**: variant name (`headline-a`, `video-15s`, `static-bookcover`)
- **utm_term**: market code lowercase (matches the codes in `markets.md`)

## Examples

```
https://yourbrand.com/?utm_source=klaviyo&utm_medium=email&utm_campaign=peak-feb-streak&utm_content=day3&utm_term=si
https://yourbrand.com/?utm_source=meta&utm_medium=cpc&utm_campaign=peak-mar-urgency&utm_content=video-15s&utm_term=hu
```

## Rules

- All five params required on tracked links. No optional params.
- Lowercase, no spaces, hyphens not underscores.
- Never reuse a campaign slug across phases — append phase if reused (`peak-feb-streak-v2`).
