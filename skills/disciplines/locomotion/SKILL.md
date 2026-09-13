---
name: locomotion
description: Use when ground or air movement needs explicit velocity, acceleration, braking, facing, slope, grounding, or root-motion ownership independent of render interpolation.
---

# Locomotion

Choose the movement column:

| Column | Turn | Air |
|---|---|---|
| tank-turn | rotate then move | low authority |
| strafe | camera-relative | medium authority |
| twin-stick | face aim action | medium authority |
| analog-8way | snap or blend | high authority |
| root-motion-driven | authored root displacement | clip-defined, adapter-validated |
| climb-stamina | traversal state swaps movement policy | project-defined |

## Ownership

1. The logical movement step owns position/velocity state; rendering interpolates/extrapolates presentation only.
2. Acceleration, braking, max speed, air-control and turn policy are project data. Instant max speed is an authored mode, not a default.
3. Grounding uses declared collision/probe evidence on slopes, stairs, ledges and moving surfaces; never assume world `y = 0`.
4. `jump-leniency` is the single owner of coyote time, jump buffer and corner forgiveness. Locomotion exposes grounded/left-ground/landed events and consumes the resulting jump request.
5. `platform-jump` owns jump-arc tuning; `moving-platform` owns platform-relative carry/transfer; `climb-vault` and `swim-water` own their traversal-state transitions.
6. Attack turn-lock or cancel restrictions come from `action-feel`, not this skill.
7. Root motion must still pass through the project's collision/movement solver. A clip cannot teleport through blockers because it authored displacement.

## Accept

Replay the same input trace across supported render rates. Logical position/velocity and grounded transitions match within declared numeric tolerance. Test acceleration/braking, slope/stair boundaries, ledge departure, moving surfaces and root-motion collision. Forgiveness windows are logged by `jump-leniency`, not duplicated here.
