---
name: season-track
description: Use when a timed or versioned reward track has free/paid lanes, tiers, XP/progress, catch-up, season rollover, claim state, or entitlement access that must survive retries and version changes.
---

# Season Track

This skill owns **season/track identity, tier progression and claim state**. Purchase ownership belongs to `entitlement-grant`; offer copy/pricing belongs to `game-monetization`/`iap-offers`; durable settings/save isolation belongs to their respective owners.

## Modes

| Mode | Lanes |
|---|---|
| free | no paid lane entitlement required |
| paid | track access requires an authored entitlement |
| both | shared progression with separate free/paid reward eligibility |

Reward type is project policy; do not assume cosmetics are always the default or that gameplay-affecting rewards are automatically valid/invalid here.

## Season contract

Each season/track has stable `season_id`, version, start/end policy, tier definitions and progression metric. Each reward claim has stable tier/reward identity and a claim transaction ID so retries cannot grant twice.

Paid-lane eligibility reads `entitlement-grant`; it does not create a second receipt flag. Season rollover explicitly defines carry/reset of track XP, unclaimed rewards and entitlement relationship. It must not silently reset unrelated `settings-persist`, story save or cloud data.

Catch-up/skips, premium rewards and free availability are monetization/design policy authored in `game-monetization`; this skill only implements the selected track state consistently.

## Acceptance

Test claim/retry, exact tier boundary, free-vs-paid eligibility, purchase arriving after progress, season end/rollover, save/load and duplicate callback. Stable season/reward IDs prevent duplicate or missing grants across version changes.
