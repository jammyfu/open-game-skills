---
name: sprite-atlas
description: Use when sprite sheets need slicing, stable pivots, texture packing or engine metadata, or when an imported animation jitters, bleeds between cells or loses attachments.
---

# Sprite atlas

Own **packing and import**, not image inventory. [Sprite catalog](../sprite-catalog/SKILL.md) owns required image families; [pixel-animation](../pixel-animation/SKILL.md) owns playback and gameplay frame mapping. Keep the existing family's intent when older callers ask this skill to generate art; route generation before packing.

## Modes

| Mode | Output |
|---|---|
| grid-slice | uniform source cells and explicit empty-cell handling |
| trimmed-pack | varying trimmed regions with original geometry preserved |
| tileset | tile IDs, margin/separation and terrain metadata |
| ui-kit | regions plus nine-slice borders and widget states |

Legacy families char-cycle, portrait, projectile, prop, combat-pose, facing, companion, enemy, weapon-overlay, pickup, hud-icon, shadow, vehicle and background remain inventory requests; resolve a packing mode afterwards. VFX generation goes to [vfx-generate](../../assets/vfx-generate/SKILL.md).

## Procedure

1. Inspect real image dimensions, alpha, cell layout, facing and target loader/version. An attractive generated sheet is not necessarily an exact grid. Reject or repair malformed cells explicitly; never silently crop a weapon or foot.
2. Measure pivot/attachment positions against the untrimmed source coordinate system. Publish axis direction and pixels-per-unit. If trimmed or rotated, export the transform back to the source; disable rotation for loaders that cannot represent it.
3. Export each region's ID, `source_size`, packed rectangle, `trim_offset`, `pivot`, rotation, socket offsets and `duration_ms`. Preserve stable IDs across repacks. A zero-alpha cell may be an intentional timing frame, not removable waste.
4. Choose padding/extrusion, filtering, mipmaps, page size and compression for the actual renderer. A fixed one-pixel rule is not sufficient for all mip levels. Report alpha convention and test against light and dark backgrounds.
5. Import the metadata and replay the animation. Map artwork durations onto the authored simulation timeline; never change active frames to fit a PNG. Hitboxes and hurtboxes stay authored gameplay data.

## Output

Atlas images, frame/animation metadata, source manifest mapping, packing settings, version/rights record, measured alignment deviations and an import result. Unsupported loader features are blocked, not guessed. Generation and packing scripts must not overwrite source art without explicit permission.

## Accept

Replay idle/walk/attack with overlays for source pivot and sockets; trimming must not move them. Repack and verify saved IDs still resolve. Test empty frames, rotated imports, edges at minification and missing-region fallback. A missing attachment must not create invisible invulnerability.

## Reference

[Godot TileSet atlas properties](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html) describe a concrete loader's margins, separation and padding. Inspect the target version rather than copying its settings to every engine.
