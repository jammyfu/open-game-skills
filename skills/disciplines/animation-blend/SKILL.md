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

## Accept

Record animation/gameplay state, source clips/layers/weights, displacement owner and resulting pose through transition/interruption cases. Disabling render meshes/blending does not change authoritative hits, cancels or gameplay displacement.
