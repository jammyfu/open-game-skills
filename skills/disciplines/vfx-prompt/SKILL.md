---
name: vfx-prompt
description: >
  Generate game juice sheets with GPT Image 2.5. Use when the user wants
  hit sparks, slash arcs, speed lines, muzzle flash, or dash trails as
  images. Stacks on juice-vfx. The picture is not a hitbox.
---

# VFX prompt (GPT Image 2.5)

Ask the column. One sheet per request. Do not invent a new folder per spark.

| Column | What the sheet shows |
|---|---|
| hit-spark | radial sparks + star flash at contact |
| slash-arc | crescent energy along a swing |
| impact-burst | shock ring + debris opposite the force |
| speed-line | motion lines / smear behind a fast body |
| afterimage | 2–4 ghost poses fading behind |
| muzzle-flash | short cone + sparks at a barrel |
| dash-trail | ribbon or streak along a published path |
| parry-flash | brief white/color ring on a successful guard |

Timing still lives in juice-vfx. This file only authors the *look*.

## Image 2.5 contract

Every prompt answers the same seven slots:

```
ASSET: game VFX sprite / flipbook / single stamp
SUBJECT: one effect, no character unless asked
DIRECTION: force vector (left→right slash, impact to camera, etc.)
STYLE: lock one (pixel / anime cel / painterly / stylized 3D)
BG: transparent PNG, no checkerboard, no floor, no drop shadow unless asked
TEXT: none. no watermark, no caption, no logo
OUTPUT: square stamp or N-frame strip, isolated silhouette
```

API when available: `model=gpt-image-2.5-*`, `background=transparent`, `png` or `webp`.
Transparency can shift style — restating STYLE in the prompt is required.

Light hit = fewer, slower marks. Heavy / finisher = more, longer streaks.
Direction opposes the incoming force (swing right → sparks fly left).

## Iron rules

- juice_hook after the logical hit. A pretty spark does not move query_hits.
- One column per image job. A slash-arc sheet is not also a muzzle sheet.
- Flash-off (a11y-controls) must still read the pose. Do not make the spark the only tell.
- Flipbook: generate a base frame, then edit only the moving marks. Lock the rest.
- Do not put UI words (“HIT”, “COMBO”) on the sprite unless the user asked for a sticker.

## Accept

The file has alpha. The silhouette reads at stamp size. Two hits of the same row can reuse the same sheet. Turning the sprite off does not change hitstun or damage.

Prompt pack: [docs/prompts-vfx-image25.md](../../../docs/prompts-vfx-image25.md)
