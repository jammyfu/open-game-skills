---
name: sprite-catalog
description: Use when a project needs to inventory required sprites, tiles, UI, icons, portraits, props, animation states, or facings before generation or atlas packing.
---

# Sprite catalog

Ask the family first, then the row. Full list: [bundled image families](../../references/sprite-image-catalog.md).

| Family | Typical sheets |
|---|---|
| actor-cycle | idle / walk / run / jump / fall / land / dash / climb / swim / sit |
| actor-combat | attack-light / attack-heavy / hurt / death / block / parry / dodge / throw |
| actor-face | portrait / talk-blink / viseme / turnaround |
| enemy-cycle | same cycles as actor, plus spawn / enrage / downed |
| projectile | bullet / arrow / magic-bolt / thrown / beam-head |
| vfx | route to vfx-generate |
| tileset | ground / wall / cliff / water / ladder / door / hazard |
| prop | chest / crate / torch / vegetation / furniture / vehicle |
| item-icon | weapon / armor / consumable / key / currency |
| ui-hud | heart / meter / button / frame / cursor / prompt / numbers |
| map-icon | pin / poi / player-arrow / fog-mask |
| avatar-part | hair / eyes / mouth / brow / outfit — route to avatar-create |
| shadow | blob / contact / jump-shrink |

## Generation handoff

Record the generation brief: isolated subject, one style lock, transparent or chroma, no extra text, even cell grid for flipbooks.
Actor sheets face one published direction per strip. 4-dir or 8-dir is extra strips, not one crowded collage.
Neutral bind pose / idle first. Combat sheets do not bake sparks into the body (vfx is a separate plate).

## Iron rules

- One family + one row per generate job.
- Logical cell size is published for each atlas family. Common pixel-art sizes such as 16/32/48/64 are examples, not a universal whitelist; do not mix incompatible cell metrics in one atlas.
- Hurtboxes stay hitbox-hurtbox data. The sprite can be larger than the box.
- Wardrobe is sprite-skin slots, not a second skeleton.
- Do not scrape copyrighted sprite rips into the repo.

## Accept

The asset manifest covers every required state, facing, slot and fallback. It is a production plan, not proof that images have been generated or imported.

## Output and ownership

Write an asset manifest with stable ID, family, required states/facings, logical cell size, style source, rights/provenance, priority, fallback and status (missing/draft/approved/imported). Distinguish optional art from blockers.

This skill owns **what to produce**, not atlas packing. Send approved plates and the manifest to [sprite-atlas](../sprite-atlas/SKILL.md) for slicing, pivots and import metadata. A requested atlas family remains supported, but generating an image alone is not a packed-atlas deliverable.
