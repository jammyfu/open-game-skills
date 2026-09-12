---
name: ad-break
description: >
  Optional ads as a pause, never as a combat cancel. Use when a reward
  video fires mid-combo or when skip is fake. Stacks on game-monetization
  ad-reward. Does not promise eCPM.
---

# Ad break

Ask the column.

| Column | When it may play |
|---|---|
| after-fail | continue / retry offer |
| between-runs | after a match or stage clear |
| shop-opt-in | player taps watch for N coins |
| banner-idle | menus only, never the field |

No column plays during hitstop, input buffer, or an active move.

## Clock

Ads freeze presentation. Logic pauses (menu-flow freeze-world) or the match is already over.
Reward grants go through entitlement-grant after the SDK says completed — not on impression.
Close / fail / skip-without-reward grants nothing.

## Iron rules

- Opt-in copy names the reward before the video.
- Frequency cap is published. A second fail does not stack two videos.
- Remove-ads durable-unlock silences every column.
- Do not start an ad on pointer-down of an attack job.

## Accept

A combo can finish without an ad. Watching once grants once. Premium-unlock leaves no banner on the HUD.
