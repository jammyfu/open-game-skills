---
name: sprite-skin
description: Use when a 2D character needs cosmetic atlas-slot, skeletal-skin, or palette swaps while gameplay collision, timing, and stats must remain unchanged.
---

# Sprite skin

Ask the column:

| Column | What swaps |
|---|---|
| atlas-slot | one region in a sprite sheet |
| spine-skin | Spine skin / slot attachment |
| palette-swap | colors only |

Use with [spine-skeletal](../spine-skeletal/SKILL.md). Do not load a missing `spine-2d` path.

## Rules

1. Skin is paint. Hitbox/hurtbox geometry is owned by `hitbox-hurtbox`; collision filters/layers are owned by `collision-layers`.
2. A paid skin is cosmetic. See game-monetization. No paid i-frames.
3. Atlas pack by draw order. Missing attachment falls back to a published default, not a crash.
4. After swap, re-check socket names (weapon, hand) against model-pipeline / character-rig contracts.
5. Pixel-animation sheets use atlas-slot, not a second skeleton.

## Accept

Swap skin in the pause menu: same hitbox, same cancel window. A missing slot shows the default arm, not a hole in the hurtbox.
