# Brand voice

> **Replace the per-market examples below with your own brand-voice samples.** The structure (core voice, forbidden patterns, per-market notes, tone-by-phase, examples) is the load-bearing part — keep it. Fill in the localized examples with copy that reflects your actual brand.

## Core voice

Define 3–5 voice attributes. Examples (rewrite for your brand):

- **Calm authority** — we know the domain, we don't panic-sell
- **Audience-switched register** — peer-tone for end users, advisor-tone for decision-makers (parents/buyers/etc.); switch by audience segment, not market
- **Concrete, never abstract** — cite numbers and outcomes; don't hand-wave
- **Evidence over hype** — don't promise miracles

## Forbidden patterns

- Generic filler ("unlock your potential", "transform your future", "game-changer")
- Excessive emoji (one per message max, only where natural)
- Fake urgency ("Last chance!" when it isn't)
- Comparing to competitors by name in copy

## Per-market notes

List per-market register, formality, script (Latin/Cyrillic/etc.), and any term overrides. Reference `.claude/rules/markets.md` for the canonical market table.

Example structure:

- **{{market_a}}**: [formality rule, e.g. informal "you" with end users]
- **{{market_b}}**: [term override, e.g. always use term X — never term Y]
- **{{market_c}}**: [script rule, e.g. Cyrillic body, brand stays Latin]

## Tone by phase

Map tone to the seasonality phases in `.claude/rules/seasonality.md`. Example:

- **Peak**: urgency without panic
- **Enrollment**: possibility — "start strong, finish confident"
- **Low**: brand-only — "we'll be here when you need us"

## Examples

Provide concrete ✅ and ❌ samples per market, per register. Replace the placeholders below with real copy.

### {{market}} (end users, peer tone)
- ✅ `[student peer-tone example for {{market}}]`
- ❌ `[forbidden filler example — show what wrong looks like]`
- ❌ `[wrong-register example — formal where casual is correct]`

### {{market}} (decision-maker / parent, advisor tone)
- ✅ `[advisor-tone example for {{market}}]`
- ❌ `[fake urgency or emotional manipulation example]`

### Cross-cutting failures (any market)
- ❌ `[excessive emoji + fake urgency example]`
- ❌ `[named-competitor comparison example]`
- ❌ `[generic filler word example]`
