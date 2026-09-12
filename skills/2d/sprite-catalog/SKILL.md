---
name: sprite-catalog
description: >
  Full inventory of game images to generate. Use when the user wants
  sprites, tiles, UI, icons, portraits, or props listed or generated.
  One sheet per job. Stacks on pixel-animation, sprite-skin, vfx-generate,
  art-bible. Pictures are not hitboxes.
---

# Sprite catalog

Ask the family first, then the row. Full list: [docs/SPRITE-CATALOG.md](../../../docs/SPRITE-CATALOG.md).

| Family | Typical sheets |
|---|---|
| actor-cycle | idle / walk / run / jump / fall / land / dash / climb / swim / sit |
| actor-combat | attack-light / attack-heavy / hurt / death / block / parry / dodge / throw |
| actor-face | portrait / talk-blink / viseme / turnaround |
| enemy-cycle | same cycles as actor, plus spawn / enrage / downed |
| projectile | bullet / arrow / magic-bolt / thrown / beam-head |
| vfx | route to vfx-generate / vfx-prompt |
| tileset | ground / wall / cliff / water / ladder / door / hazard |
| prop | chest / crate / torch / vegetation / furniture / vehicle |
| item-icon | weapon / armor / consumable / key / currency |
| ui-hud | heart / meter / button / frame / cursor / prompt / numbers |
| map-icon | pin / poi / player-arrow / fog-mask |
| avatar-part | hair / eyes / mouth / brow / outfit — route to avatar-create |
| shadow | blob / contact / jump-shrink |

## Image 2.5 contract

Same seven slots as vfx-prompt: isolated subject, one style lock, transparent or chroma, no extra text, even cell grid for flipbooks.
Actor sheets face one published direction per strip. 4-dir or 8-dir is extra strips, not one crowded collage.
Neutral bind pose / idle first. Combat sheets do not bake sparks into the body (vfx is a separate plate).

## Iron rules

- One family + one row per generate job.
- Pixel size is published (16 / 32 / 48 / 64). Do not mix sizes on one atlas.
- Hurtboxes stay hitbox-hurtbox data. The sprite can be larger than the box.
- Wardrobe is sprite-skin slots, not a second skeleton.
- Do not scrape copyrighted sprite rips into the repo.

## Accept

A slice JSON or even grid can cut the sheet. Idle loops. Attack frames match the move-row count, not the other way around.
