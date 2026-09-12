---
name: world-map
description: >
  Engine-neutral open-world map: landmark gravity, triangle terrain,
  fog-of-war as earned information, towers, player pins, layer stacks
  (surface/sky/depths). Use when building a map screen, Sheikah-tower
  style reveal, or navigation that should feel like BotW / TotK.
---

# World map

Outcome: the player always has one visible destination and two optional side-tracks. The map sells *information they earned*, not a carpet of icons.

Public sources: CEDEC / GDC BotW world talk — triangle rule, tower heatmaps, landmark height = importance, Nintendo's word "gravity".

## When not to use

Indoor dungeon graph → `level-design`. Puzzle verb teaching → `puzzle-design`. Camera clip → `camera-anti-clip`.

## Data you must author

```
Region { id, bounds, tower, fog: hidden|silhouette|revealed }
Landmark { id, region, height_m, silhouette, reward_type,
           gravity: tower|shrine|camp|stable|peak|quest }
Pin { owner: player|system, type: stamp|marker|quest, pos, layer }
Layer { surface | sky | depths }     # TotK; BotW uses surface only
```

## Placement rules

1. **One tall thing per region.** Height encodes importance. Tower > divine beast > stable horse-head > camp skull > cooking smoke.
2. **Triangle terrain.** A hill is a choice: climb or go around. The far side hides a reward. Rectangles are used only as a reveal gate (rock that slides off a castle).
3. **Gravity, not rails.** Towers first placed as a grid felt like homework. Re-place from playtest heatmaps: put a tower where people stall, put a shrine / camp / chest *between* towers so the walk is never empty.
4. **See it, go there.** If a peak is on the horizon, there is a legal path. No invisible walls dressed as cliffs unless stamina is the gate and the cliff is readable.
5. **Fog is a reward.** Unrevealed region: border only. Activating the regional tower fills topo. Fast travel unlocks on the tower / shrine the player touched — not on every icon.
6. **Pins are the player's plan.** Cap at ~5–8 custom pins or they become noise. System quest markers do not cover the whole map at once.

## Map screen contract

- Player glyph is a **facing chevron**, not a dot.
- Zoom stops: world → region → local. Local still does not dump every material node.
- Layers (surface/sky/depths) are tabs, never composited into one unreadable sheet.
- Night changes landmark priority: lights and stables rise, peaks fall.

## Difficulty coupling

Early stamina is the map's first gate. A tower that needs two stamina wheels is a *region key*, not a bug. Do not auto-level the climb.

## Accept

- From the spawn plateau the player can name three destinations they can see.
- Walking toward the first tower, they get sidetracked by at least one other gravity well.
- Opening the map on an unvisited region shows a border, not a spoiler list.
- A 360° spin never shows more than ~2 towers plus a handful of smaller silhouettes.
