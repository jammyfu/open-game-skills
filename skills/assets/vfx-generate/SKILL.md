---
name: vfx-generate
description: Use when isolated game VFX plates or flipbooks are needed for impacts, movement, status or traversal, especially when effects have been baked into actor art.
---

# VFX generate

Ask the column first. One plate, one job. Visual timing stays in `juice-vfx`; gameplay event timing stays with the move or world system.

## Combat

| Column | Plate |
|---|---|
| hit-spark | short directional sparks at contact |
| impact-burst | ring + debris opposite the force |
| slash-arc | blade ribbon + thin highlight |
| muzzle-flash | barrel bloom, 1–2 frames |
| trail-streak | projectile or dash ribbon |
| explode-burst | fire + smoke, scaled to published damage |
| parry-flash | brief ring on a successful guard |
| shield-break | shards flying off a failing barrier |
| crit-star | small star burst, not a damage number |

## Motion

| Column | Plate |
|---|---|
| speed-line | motion lines, only when fast |
| afterimage | 2–4 fading silhouettes |
| charge-gather | inward specks before a published swing |
| landing-dust | dust + short ring at foot plant |
| foot-puff | tiny puff on step or slide |

## Status / space

| Column | Plate |
|---|---|
| status-aura | loopable burn / ice / poison ring |
| heal-burst | upward motes + soft ring |
| teleport-dissolve | particles replacing a body, not a second collider |
| summon-circle | floor ring, no extra character |
| ground-crack | decal + rising dust, not a new pit collider |
| water-splash | droplets + crown, contact with a volume |
| teleport-in | particles assemble, distinct from dissolution |
| teleport-out | particles disperse from the source shape |
| beam-bolt | energy span between endpoints |
| shield-bubble | sustained barrier appearance |
| pickup-sparkle | loop on a pickup |
| death-puff | terminal puff, no extra body |

## Provider capability and output contract

1. Isolated plate or N-frame strip. Flat chroma or transparent. No scene, no logo, no text.
2. No full character unless afterimage — then silhouette only.
3. Name force direction and weight. Style lock from `art-bible`.
4. One column per job. Recolor may use a reproducible local transform; do not require another paid generation call.
5. Inspect the available tool and its supported transparency, formats and edit inputs. Do not guess model IDs or API parameters. For an edit, first locate the actual source image. No usable image means generation from a brief or a request for the missing input, never a fabricated edit.
6. A prompt is not proof of exact frame count, real alpha or loop continuity. Measure the output; hand slicing/packing to sprite-atlas. Record provider/version if known, source rights, dimensions and unverified properties.

Template:

```
Game-ready {column} VFX plate, {light|heavy},
force traveling {dir}, {style},
{N}-frame flipbook in one row,
flat #{hex} or transparent,
no character, no UI, no text, no watermark.
```

Prompts: [bundled prompt examples](../../references/vfx-image-prompts.md)

## Rules

1. juice_hook after `query_hits`. A spark is not a hurtbox.
2. Speed-line / afterimage off at walk speed. Charge-gather only during published startup.
3. Heal, aura, teleport do not change HP or i-frames by existing.
4. Ground-crack is paint unless `hazard-volume` published it.
5. Flash-off still leaves pose + audio (`a11y-controls`).

Accept: the plate composites on a dummy pose without moving sockets. Juice-off still reads the tell.

Legacy aliases from vfx-prompt are translated there; all generation and acceptance rules remain here. Validate real alpha over contrasting backgrounds, measured frame rectangles and loop closure before calling a plate game-ready.
