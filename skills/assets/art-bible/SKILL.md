---
name: art-bible
description: Use when a project lacks a stable visual-style contract across silhouettes, palettes, generated art, UI, enemies, or cosmetic skins.
---

# Art bible

Ask the column:

| Column | Lock |
|---|---|
| silhouette-family | one body read at a glance |
| palette-lock | published colors, no surprise neon |
| generated-draft | generated art stays draft until type-appropriate validation passes |

## Rules

1. Enemies of the same job share a silhouette family so attack-tell still reads.
2. UI fonts and combat text follow game-localization, not the key-art typeface if it goes tofu.
3. Generated textures get a compress pass then a pose/collision check (model-pipeline rule 9).
4. Skins in sprite-skin stay inside the palette-lock.
5. Do not paste a franchise style guide. Columns only.

## Accept

A new elite is readable as "elite" in graybox. A generated asset stays draft until the validation appropriate to its type is complete; generated meshes use model-pipeline cleanup/retopo when required.
