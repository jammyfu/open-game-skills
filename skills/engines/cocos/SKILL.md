---
name: cocos
description: Use when an existing Cocos Creator or related Cocos/minigame project needs skill contracts mapped onto its component lifecycle, scheduler, physics, animation, input, or project-owned simulation clock.
---

# Cocos adapter

Inspect the Cocos/Creator version, target runtime/minigame platform, physics backend and current scheduling ownership before binding gameplay timing.

## Timing

Component `update(dt)` and `lateUpdate(dt)` are called every frame when enabled. Scheduled callbacks use the engine scheduler but an interval alone is not proof of a deterministic fixed gameplay simulation.

If the project already owns a fixed logical loop, preserve its configured rate and call it from the appropriate lifecycle/scheduler boundary. Add an accumulator only when the game contract needs one; never assume the engine update callback itself is fixed-rate.

Per-actor hitstop freezes actor/action/animation state, not the engine's global ticker/scheduler. Minigame focus/touch lifecycle stacks with `browser-input` or the target platform adapter.

## Bindings

Map semantic input, actor-local pose/animation, physics/query volumes, movement/knockback and camera presentation through the APIs available in the installed version. Keep feel/timing rules in disciplines rather than duplicating them in components.

## Accept

Record engine version, target platform, update/scheduler/physics configuration and logical-step owner. Test variable frame cadence, pause/background/resume and per-actor hitstop; unrelated actors/systems continue according to the project contract.
