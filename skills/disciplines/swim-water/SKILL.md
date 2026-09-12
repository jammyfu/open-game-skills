---
name: swim-water
description: The body in a volume. Ask surface-only vs dive vs no-swim. Locomotion and camera swap on enter. Breath is a meter or none.
---

# Swim and water

Ask the column:

| Column | What the body may do |
|---|---|
| no-swim | kill or block |
| surface-only | float and paddle |
| dive | 3-axis + breath |

## Rules

1. Enter and exit are moves. Instant floor-walk out of a pool is a bug.
2. Breath drain uses stamina-clock or its own meter. Publish drown vs pop-up.
3. Camera-anti-clip treats the water plane as a collider for the near plane if dive is off.
4. Attacks in water are a graph subset. Do not keep land cancel windows.
5. Fall-rules swap on water. A high dive may be safe.

## Accept

Player can name how to get out. Drowning is telegraphed before it kills.
