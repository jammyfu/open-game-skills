---
name: router
description: Route open-game-skills. Ask columns first. Load one engine adapter, then the needed disciplines, then at most one studio column and one genre column.
---

# Router

1. Ask the columns in README (map, difficulty, gear, wear, combat, engine).
2. Engine unknown → `engines/custom`.
3. Combat / buffer / hitstop / cancel → `action-feel`.
4. Orbit / clip / follow → `camera-anti-clip`.
5. Foot slide → `ik-foot-locking`.
6. Map / fog / pins → `world-map`.
7. Curve / gates / scaling → `difficulty-design`.
8. Loot / craft / slots → `equipment-progression`.
9. Wear / break / hone → `durability-economy`.
10. Rooms / shrines / stages → `level-design`.
11. Verb teaching → `puzzle-design`.
12. Pillars / slice → `game-planning`.
13. Buttons / context A → `input-design`.
14. Mesh / tex / bind → `assets/*`. Spine / pixel → `2d/*`.
15. Studio names only pick columns. They do not add a second clock.

Never mix two combat presets on one actor. Never mix consume + town-repair on one item instance.
