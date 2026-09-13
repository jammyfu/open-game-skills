---
name: godot
description: Use when an existing Godot project needs gameplay, physics, animation, input, hitstop, or camera contracts mapped onto its configured idle and physics processing loops.
---

# Godot adapter

Inspect the Godot version, project physics tick setting and existing node ownership before mapping gameplay clocks.

## Timing

`_process(delta)` is idle/frame processing and varies with rendered frame rate. `_physics_process(delta)` runs before physics steps at the project's configured physics tick rate (60/s is a default, not a contract). The engine may process multiple physics steps in one rendered frame when catching up.

Physics-facing character/collision work normally belongs in `_physics_process`; presentation can live in `_process`. If the project uses another deterministic logical clock, preserve it rather than forcing all gameplay into the default physics rate.

Actor-local hitstop pauses the selected action/animation/logical clock. Do not use `Engine.time_scale` for per-actor combat freeze.

## Bindings

- input: `Input` / action map into semantic actions;
- pose: `AnimationPlayer` / `AnimationTree` under local time ownership;
- hits: `Area2D/3D`, shape queries, `ShapeCast2D/3D`, or project-authored logical volumes;
- knockback: body movement solver in the owned physics/logical phase;
- camera: `SpringArm3D`/shape sweep or project solution implementing `camera-anti-clip`.

## Accept

Record Godot version and configured physics ticks per second, then document which work is `_process`, `_physics_process`, or a custom clock. Replay equivalent logical input at different render rates and verify identical logical outcomes without claiming identical presentation latency.
