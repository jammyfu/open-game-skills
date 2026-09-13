# Game sprite / image catalog

Use with [`sprite-atlas`](../2d/sprite-atlas/SKILL.md). For VFX plates see [vfx-image-prompts](vfx-image-prompts.md). Swap `{style}` from `art-bible`.

## A. Character body sheets

| Plate | Frames (start) | Notes |
|---|---|---|
| idle | 4–8 loop | blink optional on a second row |
| walk | 6–8 | contact frames even |
| run | 6–8 | afterimage is vfx, not this sheet |
| start-run / skid | 2–4 | optional |
| jump-ascent | 2–3 | |
| jump-apex | 1–2 | |
| fall | 2–3 | |
| land | 2–3 | dust is vfx |
| crouch / crawl | 2 + 4 | |
| climb | 4–6 | ladder or wall |
| swim-surface / dive | 4 + 4 | |
| dash / roll | 4 | i-frames are data |
| sit / sleep / talk-body | 2 | |
| 4-dir or 8-dir | same cycles | east = flip if the style allows |

## B. Combat poses

| Plate | Frames | Notes |
|---|---|---|
| attack-light / heavy | 4–8 | startup / active / recover cells named |
| air-attack | 3–6 | |
| charge / hold | 2–4 | loop then release |
| hurt / knockback | 2–4 | |
| death | 4–8 | |
| block / parry | 2–3 | flash is vfx |
| grab / throw | 3–6 | |
| revive / get-up | 3 | |

## C. Other actors

| Plate | Notes |
|---|---|
| enemy kit | idle, walk, tell, attack, hurt, death |
| elite / boss | plus phase-swap pose |
| npc | idle + talk + walk |
| mount / vehicle | body + wheel or gait |
| civilian / crowd | idle only is legal |

## D. Gear and shots

| Plate | Notes |
|---|---|
| weapon-overlay | hand socket alignment |
| shield-overlay | |
| projectile | 1–4 frames + impact is vfx |
| dropped-weapon | world pickup pose |
| ammo casing | optional juice |

## E. World tiles and props

| Plate | Notes |
|---|---|
| terrain tileset | grass, dirt, stone, sand, snow, wood |
| wall / cliff / cave | autotile if the engine needs it |
| platform / slope / ladder | metrics from platform-jump |
| water / lava / ice | hazard-volume tell |
| door / chest / lever / torch | interact-prompt |
| breakable crate / pot | 2–3 break frames |
| foliage / tree / grass sway | 2–4 loop |
| building facade | |

## F. Pickups and icons

| Plate | Notes |
|---|---|
| coin / gem / heart / mana | 4-frame spin |
| key / card / quest item | |
| consumable | potion, food |
| equipment icon | inventory slot art |
| status icon | burn, freeze, poison, buff |
| skill icon | tree and hotbar |
| map pin / minimap token | |

## G. UI kit

| Plate | States |
|---|---|
| button | normal, hover, pressed, disabled |
| panel / window / speech box | 9-slice corners |
| cursor / reticle | idle, click, invalid |
| slider / checkbox / tab | |
| hp / mp / stamina bar | empty, fill, damage-delay |
| item slot / empty slot | |
| pause / game-over / title plate | no stolen fonts from a shipped game |

## H. Faces and meta

| Plate | Notes |
|---|---|
| portrait bust | talk blink + 3 emotions |
| turnaround sheet | front side back |
| expression grid | avatar-create |
| shadow blob | separate layer |
| silhouette / lock-icon | |
| logo / key-art | store page, not in-combat |
| background / parallax | sky, mid, fog |

## Provider-neutral generation brief

```
Game-ready {family} sprite sheet, {N} frames in one row, even {W}x{H} cells,
same foot pivot, {style}, flat #00FF00 background,
no VFX baked in, no UI text, no watermark.
```

Do not generate hitboxes. Do not copy a shipped sheet.

Generated output is a draft until cell geometry, alpha, alignment and import are measured. Select an available provider and verify its actual capabilities; these prompts are not API parameter documentation.
