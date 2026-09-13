---
name: swim-water
description: Use when entering water must switch buoyancy, surface, dive, breath, movement, camera, attack, or exit rules through an explicit water-volume state.
---

# Swim and water

Choose:

| Column | Capability |
|---|---|
| no-swim | block, hazard, or authored failure response |
| surface-only | buoyant surface locomotion |
| dive | 3-axis underwater locomotion with optional breath/resource |

## Rules

1. A water volume publishes enter/exit events and surface information. Movement state changes are logical transitions, not render-height guesses.
2. Surface buoyancy, dive depth, vertical authority and exit/ledge rules are authored data. `locomotion` integrates the selected water movement policy.
3. Breath/oxygen may use its own meter or a declared shared resource. Publish warning thresholds and failure behavior; do not assume stamina is always the correct owner.
4. `camera-anti-clip` handles **solid geometry** around/under water. The water surface itself is not universally treated as a solid camera collider; above/below-water presentation is a separate camera/render policy.
5. Water attack/cancel availability is an explicit graph subset. Do not automatically reuse land cancels.
6. `fall-rules` owns fall consequences; water may modify them only through published landing/volume rules.

## Accept

Test shallow/deep entry, surface transition, dive/no-dive boundary, low breath warning, exit with blocked clearance, and leaving/re-entering the volume in one logical interval. The movement/camera state follows volume data without getting stuck, and no invisible solid water plane blocks a valid camera unless the project explicitly authors one.
