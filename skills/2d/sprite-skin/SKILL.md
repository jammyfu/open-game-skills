---
name: sprite-skin
description: 2D swap of slots and skins. Ask atlas-slot vs spine-skin vs palette-swap. Hitboxes stay on the logic body. Cosmetics do not change hurtboxes.
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

1. Skin is paint. Hurtbox / hitbox live on collision-layers.
2. A paid skin is cosmetic. See game-monetization. No paid i-frames.
3. Atlas pack by draw order. Missing attachment falls back to a published default, not a crash.
4. After swap, re-check socket names (weapon, hand) against model-pipeline / character-rig contracts.
5. Pixel-animation sheets use atlas-slot, not a second skeleton.

## Accept

Swap skin in the pause menu: same hitbox, same cancel window. A missing slot shows the default arm, not a hole in the hurtbox.
