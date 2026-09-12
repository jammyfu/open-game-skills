---
name: locomotion
description: Ground and air movement independent of the combat clock. Tank-turn, strafe, twin-stick, analog 8-way, root-motion, climb-stamina. Coyote and jump buffer live here.
---

# Locomotion

Ask the column:

| Column | Turn | Air |
|---|---|---|
| tank-turn | rotate then move | low |
| strafe | camera-relative | medium |
| twin-stick | face aim stick | medium |
| analog-8way | snap or blend | high |
| root-motion-driven | clip owns displacement | clip |
| climb-stamina | same as ground | shared tank |

## Rules

1. Logic step owns velocity. Render interpolates.
2. Author accel and brake. Instant max-speed is a column, not a default.
3. Stairs and slopes use a ground probe, never y = 0.
4. Coyote and jump-buffer start at 4-8 frames at 60Hz — data, not law.
5. A shared stamina tank empties into slide or fall, not a freeze.
6. Turn-lock during attacks comes from action-feel, not from this skill.

## Accept

- Releasing the stick stops inside the authored brake window
- A jump pressed a few frames early still jumps on the platformer column
- Climbing a readable slope fails into a fall, not a stuck pose
