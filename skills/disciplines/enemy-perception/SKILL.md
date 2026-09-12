---
name: enemy-perception
description: >
  How a body notices the player. Use when an elite always faces you like a
  punching bag, or when stealth-info exists but AI never drops chase.
  Stacks on enemy-ai and stealth-info. Does not author a kit.
---

# Enemy perception

Ask the column.

| Column | How they know |
|---|---|
| cone-sight | forward cone + line of sight |
| hear-ring | noise radius; sprint louder than walk |
| last-known | go to last seen point, then idle |
| alert-share | one spotted can ping neighbors once |

States: idle → suspect → combat → drop. Drop has a published timer. Infinite chase is a bug.

## Iron rules

- Kit (enemy-kit-balance) only runs in combat. Idle bodies do not use their scary move.
- Sight blocked by collision-layers, not by the render mesh.
- Alert-share is not omniscience. Ping once, then last-known.
- Stealth-info cone-alert is the player-facing meter. This file is the NPC side. Keep both on one clock.
- Do not spawn the player inside a cone as the first teach (level-teach safe-try).

## Accept

A debug overlay can draw cone / ring / last-known. Breaking line of sight for the drop timer returns idle. A punching-bag that always tracks the camera fails this skill.
