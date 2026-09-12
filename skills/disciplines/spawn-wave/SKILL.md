---
name: spawn-wave
description: When new foes may appear. Ask authored-pack vs wave-budget vs director-pressure vs none. Spawns must not pop inside the camera or on the player capsule.
---

# Spawn wave

Ask the column:

| Column | Who decides the next pack |
|---|---|
| none | placed only |
| authored-pack | designer list |
| wave-budget | count + cooldown |
| director-pressure | pressure meter, still published |

## Rules

1. Spawn points are off-camera or gated. A pop-in on the pip is a bug.
2. Budget names max alive, cadence, and stop condition.
3. Rest-site heal-and-repop is a different column. Do not mix with a mid-fight director.
4. Difficulty-design may scale counts. It may not shrink dodge iframes.
5. A debug clear-ai then spawn is scripted-scene, not a natural wave.

## Accept

Player can feel a pause between packs. A pack never stands up inside their hurtbox.
