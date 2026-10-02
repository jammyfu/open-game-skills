---
name: animation-blend
description: Use when rendered character poses need weighted locomotion, aim, attack, additive or transition blending while gameplay state, hit timing and displacement ownership remain explicit.
---

# Animation blend

This skill owns **presentation pose composition**, not gameplay state or hit timing. `animation-graph` selects/coordinates animation states/layers; movement owners define displacement policy.

## Compatible displacement columns

| Column | Gameplay displacement owner |
|---|---|
| procedural-loco | locomotion/physics code |
| root-motion | authored root motion consumed by the gameplay movement solver |
| hybrid | published state-dependent ownership with one displacement application |

## Rules

1. Weighted blends/additives/interpolation paint a rendered pose from authoritative animation/gameplay state; they do not extend active hit frames or cancel windows.
2. Blend duration/easing/inertialisation are authored in time/state units appropriate to the runtime, not a universal 2–6 frame fade.
3. Root-motion extraction/application has one explicit gameplay owner. Visual blending must not double-apply root displacement.
4. Aim/look overlays declare mask/weight/reference space and do not silently rotate gameplay facing/collision unless the owning gameplay contract requests it.
5. Foot contact repair delegates to `ik-foot-locking`; blend output remains a source pose rather than a second locomotion solver.

## Corrective layers

Procedural corrections applied after the source pose are presentation layers with the same ownership limits. Examples are limb/body interpenetration avoidance, reach or look IK, and prop alignment. They must also be temporally stable:

1. The correction is a continuous function of pose and time. Avoid hard thresholds, snapping to bins or cells, picking whichever sample is deepest, and hard on/off zones. Blend across regions and weight competing samples smoothly.
2. Correct through a degree of freedom that can actually remove the contact. For a contact on the upper segment, rotate the chain about its parent joint rather than pushing an end effector that barely moves that segment. Iterate with bounded gain and no overshoot; a case that does not converge must not alternate between frames.
3. Contact onset is soft enough that brushing contact causes no velocity kink. The allowed residual overlap is an authored tolerance, validated against the project's clipping check.
4. For deterministic clips, corrections may be cached and filtered over time per actor and clip. Invalidate the cache on rig, body or clip changes.
5. Before tuning, attribute jitter by measuring rendered joints with the corrective layer on and off. Fix step thresholds in the source motion separately.

## Accept

Record animation/gameplay state, source clips/layers/weights, displacement owner and resulting pose through transition/interruption cases. Disabling render meshes/blending does not change authoritative hits, cancels or gameplay displacement.

For corrective layers, sample joint positions at the presentation rate. Count consecutive-frame acceleration reversals, or another authored jitter metric, with corrections on and off, alongside the penetration check. Neither metric may regress.
