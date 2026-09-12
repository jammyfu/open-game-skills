---
name: vfx-generate
description: Generate isolated game VFX plates for GPT Image 2.5. Hit sparks, slashes, speed lines, muzzle, trails. Paint only. Never a second hitbox.
---

# VFX generate

Ask the column first. One plate, one job.

| Column | What the plate shows |
|---|---|
| hit-spark | short directional sparks at contact |
| impact-burst | ring + debris opposite the force |
| slash-arc | blade ribbon + thin highlight |
| speed-line | motion lines / afterimage, only when fast |
| muzzle-flash | gun bloom at the barrel, 1–2 frames |
| trail-streak | projectile or dash ribbon |
| explode-burst | fire + smoke, scaled to published damage |
| status-aura | loopable element ring (burn, ice, poison) |

Timing still lives in `juice-vfx`. This file only authors the picture. Cosmetics do not change hurtboxes (`game-monetization`).

## Image 2.5 contract

Name the artefact, not a screenshot:

1. Isolated VFX plate or N-frame flipbook grid.
2. Flat chroma or transparent field. No scene, no logo, no watermark.
3. No full character unless the column is speed-line afterimage — then a silhouette only.
4. Force direction and weight (light / heavy) in the prompt.
5. Style lock from `art-bible`. Do not mix oil paint and pixel on one sheet.
6. Neutral anchor first if you also generate characters — never bake sparks into the walk sheet.

Template:

```
Game-ready {column} VFX plate, {light|heavy} weight,
force traveling {dir}, {art-bible style},
{N}-frame flipbook in one row, even spacing,
flat #{hex} background or transparent,
no character, no UI, no text, no watermark.
```

Light hits resolve visually in 0.3–0.5s (few sparks). Heavy hits add a ring and more stretch. Speed-line is off at walk speed.

## Accept

A generated plate composites over a dummy pose without moving the hurtbox. Two identical hits can reuse the same plate. Juice-off still reads the tell (`juice-vfx`, `a11y-controls`).
