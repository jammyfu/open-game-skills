---
name: knockback-launch
description: Use when hits need authored pushback, launch arcs, gravity, airborne stun, or juggle trajectories after the applicable hitstop policy resolves.
---

# Knockback launch

This skill owns intended launch parameters, not body collision response.

Choose:

| Mode | Output |
|---|---|
| ground-push | planar initial velocity/impulse plus decay or stop rule |
| launch-arc | initial velocity/impulse, gravity and airborne state |
| custom-trajectory | explicitly authored curve/solver when the project requires it |

Publish whether launch begins immediately or after participant hitstop reaches the required state. Store vector/impulse, gravity, air-stun and any air-control rule in gameplay data, not animation clip length.

`knockback-body` owns wall/floor sweeps and stop/slide/splat response. `hitstun-recover` owns action lock/recovery. `combo-design` owns juggle-route budgets. Player and enemy may share a formula, but symmetry is a project choice rather than a universal rule.

## Accept

For each representative launch, log initial state, launch tick, velocity/impulse, gravity and expected contact window; replay it at different render rates. The measured arc is stable, and changing animation duration does not change physics. Collision penetration is validated separately by `knockback-body`.
