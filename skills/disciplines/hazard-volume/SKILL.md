---
name: hazard-volume
description: Use when lava, spikes, wind, pits, poison clouds, or other spatial gameplay hazards need authored volumes, stable overlap identity, tick/kill/push policy, and evidence independent from decorative meshes.
---

# Hazard volume

Ask: `tick-damage | instant-kill | push-field`.

## Ownership

The hazard owns its gameplay volume and effect policy. Decorative art is not the oracle. Hit filtering remains compatible with `hitbox-hurtbox` / `collision-layers`; recovery or fall policy may delegate to `fall-rules`.

## Contract

Publish:
- stable `hazard_id`
- authoritative volume shape/transform
- effect mode and project gameplay-clock policy
- target filters / immunity policy
- enter/stay/exit event identity
- cue/reference IDs used by presentation

For periodic effects, define the tick schedule from the project's gameplay clock and guarantee at-most-once application for one hazard/target/tick identity. Re-entering, pause/resume, streaming and rollback must not duplicate an already committed effect.

For instant-kill or forced recovery, the project defines the cue and recovery contract; this skill does not require one universal telegraph style.

## Acceptance

The same overlap event resolves once, independent of frame rate or decorative mesh overlap. The hazard's visible presentation may extend beyond the gameplay volume, but evidence can show the authoritative boundary, effect identity and target state that produced each application.
