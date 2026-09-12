---
name: juice-vfx
description: Flash, shake, particles, freeze-frame extras. juice_hook only. Must not change hitstop length, damage, or cancel windows. Ask dry vs punchy vs maximal.
---

# Juice and VFX

Ask the column:

| Column | How loud |
|---|---|
| dry | pose + audio only |
| punchy | short flash + camera kick |
| maximal | particles, hit spark, pause-frame extra |

## Rules

1. juice_hook fires after the hit is already decided.
2. Shake and flash die in under 200ms unless the column is maximal and the hit is a finisher.
3. A11y flash-off must still leave pose and audio tells. See a11y-controls.
4. Do not scale Engine.time to fake weight. Weight is action-feel.
5. Particle count lives under performance-budget. Cut particles before you cut boxes.

## Accept

- Turning juice off still lets a new player read a published tell
- Two identical hits produce two identical clocks with or without sparks
