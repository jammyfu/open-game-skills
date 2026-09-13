---
name: custom
description: Use when a proprietary or custom game loop needs open-game-skills contracts mapped onto its actual simulation, rendering, input, collision, animation, and pause architecture.
---

# Custom engine adapter

First document the runtime/engine version or build identity and the existing loop. Do not invent a 60 Hz clock merely because other engines often expose fixed-step patterns.

## Timing contract

Publish the project's actual simulation model: fixed step, variable step, multiple rates, lockstep, server-authoritative, or another explicit design. If a fixed step exists, record its configured duration/rate and catch-up/drop policy. Keep render interpolation and presentation callbacks separate from authoritative gameplay state.

Map these responsibilities conceptually rather than forcing a specific function signature:

- semantic input sampling;
- logical tick/time identity;
- actor pose/animation presentation;
- gameplay contact queries;
- collision-safe movement/knockback;
- presentation/juice events.

Per-actor hitstop freezes only the named logical/action clocks. A separate global pause may freeze broader systems when the project explicitly owns that behavior.

Camera anti-clip follows `camera-anti-clip`: protect the actual camera/frustum footprint and final offsets rather than relying on a single point ray.

## Accept

Record engine/runtime build identity, loop diagram, configured clock rates, phase order and pause ownership. Replay a deterministic input/contact trace at at least two render cadences where the runtime permits; logical results must match, and untested timing modes remain `not-run`.
