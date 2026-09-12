---
name: vfx-prompt
description: >
  Generate game juice sheets with GPT Image 2.5. Use for hit sparks, slash,
  speed, heal, shield, teleport, landing dust, beams, elemental auras.
  Stacks on juice-vfx and vfx-generate. The picture is not a hitbox.
---

# VFX prompt (GPT Image 2.5)

Ask the column. One sheet per request. Do not invent a new folder per spark.

## Combat contact

| Column | What the sheet shows |
|---|---|
| hit-spark | radial sparks + star flash at contact |
| slash-arc | crescent energy along a swing |
| impact-burst | shock ring + debris opposite the force |
| parry-flash | brief ring on a successful guard |
| crit-star | extra starburst on a published crit |
| guard-break | shattered plate pieces flying off |
| ground-crack | radial cracks + dust, no full floor tile |

## Motion

| Column | What the sheet shows |
|---|---|
| speed-line | motion lines / smear behind a fast body |
| afterimage | 2–4 ghost poses fading behind |
| dash-trail | ribbon along a published path |
| landing-dust | puff at feet on land |
| jump-puff | small dust at takeoff |
| water-splash | droplets + crown, no pool tile |

## Ranged / magic

| Column | What the sheet shows |
|---|---|
| muzzle-flash | short cone at a barrel |
| beam-bolt | straight energy between two points |
| charge-gather | inward wisps before a published startup |
| explode-burst | fire + smoke scaled to published damage |
| cast-circle | ground ring under a caster, loopable |
| teleport-in | assemble from particles |
| teleport-out | dissolve to particles |

## Status / support

| Column | What the sheet shows |
|---|---|
| status-aura | loopable ring: burn / ice / poison / shock |
| heal-burst | upward motes + soft plus-shapes (no UI text) |
| shield-bubble | dome or plate, break uses guard-break |
| pickup-sparkle | small loop on a world item |
| death-puff | short smoke, not a second ragdoll |

Timing still lives in juice-vfx. This file only authors the *look*.

## Image 2.5 contract

```
ASSET: game VFX sprite / flipbook / single stamp
SUBJECT: one effect, no character unless asked
DIRECTION: force vector
STYLE: lock one (pixel / anime cel / painterly / stylized 3D)
BG: transparent PNG, no checkerboard, no floor, no drop shadow unless asked
TEXT: none. no watermark, no HIT/COMBO caption
OUTPUT: square stamp or N-frame strip
```

API: `model=gpt-image-2.5-*`, `background=transparent`, png/webp.
Restate STYLE — transparency can drift the look.
Light = fewer marks. Heavy = ring + stretch. Speed-line off at walk speed.
Charge-gather is juice on startup, not a second attack-tell unless art-bible says so.

## Iron rules

- juice_hook after the logical event. A spark does not move query_hits.
- One column per image job.
- Flash-off still reads the pose (a11y-controls).
- Flipbook: edit only the moving marks in-thread.
- Status-aura loops. Contact bursts do not.
- Heal plus-shapes are marks, not HUD numbers.

## Accept

Alpha reads at stamp size. Same row reuses the same sheet. Juice-off does not change hitstun or damage.

Prompt pack: [docs/prompts-vfx-image25.md](../../../docs/prompts-vfx-image25.md) and/or [docs/vfx-image-prompts.md](../../../docs/vfx-image-prompts.md)
