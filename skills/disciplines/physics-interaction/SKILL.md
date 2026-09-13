---
name: physics-interaction
description: Use when pushing, carrying, throwing, stacking or constrained objects tunnel, jitter, double-move, lose ownership or fail to restore after release or load.
---

# Physics interaction

## Scope

Own physical interaction state and motion authority, not the material reaction table, damage rules or vehicle handling. [Collision layers](../collision-layers/SKILL.md) owns filtering; [chemistry-verbs](../chemistry-verbs/SKILL.md) owns property reactions. Inspect units, body types, physics version and stepping ownership before tuning.

## Modes

| Mode | Motion owner |
|---|---|
| dynamic-push | physics solver responds to authored contact/forces |
| kinematic-carry | controller moves a swept collision body while held |
| constraint-grab | physics constraint follows an authored target |

## Procedure

1. Define free/grab-pending/held/releasing states, allowed transitions, owner and stable body ID. Resolve competing grabs through the authoritative simulation. One system writes body motion per phase; parenting only the mesh is not a physical carry implementation.
2. Respect the engine's physics step. Distinguish sustained force from a one-shot impulse; avoid applying an impulse once per render frame. Publish mass/size ranges, collision proxies, damping, solver/substep and sleep/wake settings as tested project parameters, not universal constants.
3. For kinematic carry, sweep the held body's volume and respect blocked motion. For constraint grab, bound force/torque, error and break distance. Define player-contact filtering and restore it on release, failure, death, disconnect and scene exit. Do not disable all world collisions to stop jitter.
4. On release, switch motion authority exactly once. Define world-space launch velocity and whether it replaces or augments existing velocity. Inherit motion from a moving/rotating carrier's contact point when intended; do not add carrier velocity twice. Validate release placement before reenabling collisions.
5. Use the backend's supported continuous collision or sweeps for fast/thin interactions and test its limitations. Do not promise CCD solves every overlap or high-mass-ratio stack. Log contact/penetration/constraint error and isolate geometry, stepping and ownership causes before tuning.
6. Save stable transforms, velocities, body modes and constraint identities through the persistence owner. Rebuild referenced bodies before joints; handle missing anchors safely. A shared seed is not proof of cross-backend deterministic physics.

## Outputs

Adapt the [interaction contract](assets/contract.example.json): body/mode table, authority transitions, release/filter policies, supported mass/speed envelope, interruption recovery and contact traces. Keep gameplay damage in its existing owner.

## Acceptance

Push a box onto a switch, carry it through a narrow doorway, throw at a thin wall, release from a moving platform, and restore a stack/constraint after load. Test interrupted holds and two grab requests. Compare against project tolerances and record the backend/device. [Cases](assets/evals.json) remain not-run without actual physics integration evidence.

## References

[Godot RigidBody3D](https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html) describes physics-owned motion and cautions about frequent transform writes. [Box2D simulation](https://box2d.org/documentation/md_simulation.html) documents fixed stepping, body types, forces and impulses for its 2D backend; do not transfer its API verbatim to a 3D engine.
