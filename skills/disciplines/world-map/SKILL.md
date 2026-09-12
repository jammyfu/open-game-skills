---
name: world-map
description: Engine-neutral map information design — what the player sees in the world vs on the pause map, how fog is earned, who is allowed to drop pins. Use for open-world navigation, region reveal, landmark gravity, Metroidvania maps, hub-and-spoke, or Souls-style blank maps.
---

# World Map

The map sells *earned information*, not a carpet of icons.
Ask the preset before placing a single marker.

## First question

Which information policy?

| Preset | World view | Pause map starts as | Pins |
|---|---|---|---|
| open-air | See it, walk there | Region border only | Player stamps; no auto quest trail |
| metroidvania | Room you are in | Graph grows as rooms load | Ability-gates, not GPS |
| hub-spoke | Roads from a town | Unlocked by visiting | Quest pins only in the active hub |
| blank-chart | Landmarks only if tall | Almost empty | Player-drawn notes |
| radar-hud | Fog of war + minimap | Full sheet after recon | System pings hostiles |

Do not mix "see it go there" with a golden path of quest arrows.

## Four information layers (all presets)

1. **Geometry** — always on. Silhouettes, height, light, smoke.
2. **Chart** — pause-map topography. Earned (tower, room visit, recon).
3. **Icons** — only what the player discovered or pinned.
4. **Travel** — fast-travel nodes the player has stood on.

If an icon appears before the player has a reason to know it, delete the icon.

## Universal placement rules

1. Height encodes importance. The tallest readable thing in a region is the region's sentence.
2. A landform is a choice (go over / go around / go through). The far side may hide a reward.
3. Between two major nodes, put one smaller gravity well so the walk is not empty. Re-place from playtest heatmaps, not a grid.
4. The player glyph faces a direction. A dot with no facing is a bug.
5. Cap player pins (~5–8). When everything is pinned, nothing is a plan.
6. Night / weather may reorder which landmarks pull. Do not invent new icons for that — change lights.

## Accept

From a spawn or a vista the player can name two destinations without opening the map. An unvisited region on the pause map is a border, not a spoiler list. Opening the map is optional for the next 60 seconds of travel.

Indoor graphs → `level-design`. Combat clock → `action-feel`. Camera clip → `camera-anti-clip`.
