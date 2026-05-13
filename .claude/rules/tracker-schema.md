# Tracker CSV schemas

Each subagent appends to its tracker after completing work. Performance reviewer reads these nightly.

Location: `data/trackers/`

## social-tracker.csv

```
date,market,platform,post_url,format,hook_type,status,notes
2026-05-04,si,tiktok,https://...,short-15s,pattern-interrupt,posted,
```

- `platform`: `tiktok` | `instagram` | `youtube` | `linkedin`
- `format`: `short-15s` | `short-30s` | `static` | `carousel` | `long`
- `hook_type`: `pattern-interrupt` | `question` | `stat` | `story` | `controversy`
- `status`: `draft` | `scheduled` | `posted` | `killed`

## email-tracker.csv

```
date,market,campaign_id,subject,segment,sent,delivered,open_rate,ctr,conv_rate,revenue,unsubs
2026-05-04,si,01HX...,Subject example,Active 30d,1240,1218,0.42,0.067,0.018,€340,3
```

## ads-tracker.csv

```
date,channel,market,campaign,adset,spend,impressions,clicks,ctr,conv,cac,roas,status
2026-05-04,meta,hu,peak-may-urgency,parents-25-54,€48,12400,180,0.0145,4,€12,3.2,active
```

- `channel`: `meta` | `google` | `tiktok` | `youtube`
- `status`: `active` | `paused` | `killed` | `learning`

## content-tracker.csv

```
date,market,url,title,target_kw,word_count,status,gsc_impressions_7d,gsc_clicks_7d,position_avg
2026-05-04,si,/blog/...,How to study X,X glagol,1850,published,,,
```

- `status`: `draft` | `review` | `published` | `updated`
- GSC fields filled by performance-reviewer 7+ days post-publish

## Append rules

- Always append, never overwrite
- If a row updates (e.g., a draft becomes published), append a new row with new status — keep history
- Subagent name + timestamp comment line OK at top of session block
