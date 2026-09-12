---
name: vfx-generate
description: Isolated game VFX plates for GPT Image 2.5. Combat, motion, status, traversal. Paint only. Never a second hitbox.
---

# VFX generate

Ask the column first. One plate, one job. Timing stays in `juice-vfx`.

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

## Image 2.5 contract

1. Isolated plate or N-frame strip. Flat chroma or transparent. No scene, no logo, no text.
2. No full character unless afterimage — then silhouette only.
3. Name force direction and weight. Style lock from `art-bible`.
4. One column per call. Recolor is a new call.

Template:

```
Game-ready {column} VFX plate, {light|heavy},
force traveling {dir}, {style},
{N}-frame flipbook in one row,
flat #{hex} or transparent,
no character, no UI, no text, no watermark.
```

Prompts: [docs/vfx-image-prompts.md](../../../docs/vfx-image-prompts.md)

## Rules

1. juice_hook after `query_hits`. A spark is not a hurtbox.
2. Speed-line / afterimage off at walk speed. Charge-gather only during published startup.
3. Heal, aura, teleport do not change HP or i-frames by existing.
4. Ground-crack is paint unless `hazard-volume` published it.
5. Flash-off still leaves pose + audio (`a11y-controls`).

Accept: the plate composites on a dummy pose without moving sockets. Juice-off still reads the tell.
