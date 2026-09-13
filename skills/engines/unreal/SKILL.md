---
name: unreal
description: Use when an existing Unreal Engine project needs skill contracts mapped onto its actual Actor tick groups, physics/substep policy, animation, collision, input, and camera architecture.
---

# Unreal adapter

Inspect the Unreal Engine version, project tick configuration, physics settings and existing gameplay framework before choosing an update owner.

## Timing

`AActor::Tick` / Actor Tick is called per frame when enabled; it is not inherently a fixed simulation step. Tick groups order frame work. Physics may use substepping or async/fixed-step settings configured by the project, and a frame can involve multiple physics substeps/callbacks.

Do not call ordinary Actor Tick “the fixed tick.” If deterministic gameplay needs a fixed logical clock, bind to the project's existing fixed simulation/substep mechanism or add an explicit accumulator with a published rate and ownership boundary.

Per-actor hitstop uses actor/action/animation-local state (for example montage play-rate or authored clock). Global slomo/time dilation is not a substitute for per-actor hitstop, though a separate global-pause design may intentionally use global time controls.

## Bindings

- input: Enhanced Input or project input layer into semantic actions;
- pose: montage/animation state controlled by actor-local logical state;
- hits: authored collision/query volumes with stable logical IDs;
- knockback: CharacterMovement/physics/custom movement according to project ownership;
- camera: SpringArm/sweep or project camera implementing `camera-anti-clip`.

## Accept

Record engine version, enabled Tick groups, physics/substep settings and the callback/mechanism that owns gameplay logic. Test low/high render rates and substepping cases; duplicate physics callbacks must not duplicate gameplay contacts or presentation events.
