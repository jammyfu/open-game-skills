---
name: target-priority
description: >
  Which body is the current mark when many are valid. Use when lock-on
  flips every frame, when friendly fire is a surprise, or when the camera
  mark and the attack mark disagree. Stacks on lock-on-target.
---

# Target priority

Ask the column.

| Column | Who wins |
|---|---|
| nearest-in-cone | closest inside the aim cone |
| stick-until-dead | keep mark until death, occlusion timeout, or player tap |
| threat-first | attacking bodies beat idle bodies |
| manual-cycle | player tap cycles; no auto flip |

Lock-on-target owns the camera and facing. This file owns the set and the pick.

## Iron rules

- Filter with collision-layers first. Allies are not in the set unless the row says so.
- Occlusion / death drops the mark. Do not keep a corpse as the fire target.
- Soft-lock may slide. Hard-lock uses stick-until-dead. Do not mix on one actor.
- Hitscan / projectile query_hits uses this pick, not the sprite that looks closest.
- Switching marks does not reset hitstun or cancel windows.

## Accept

A debug label names the current mark and the column. Two valid enemies do not flip every tick. Shooting while looking at A cannot damage B behind the camera.
