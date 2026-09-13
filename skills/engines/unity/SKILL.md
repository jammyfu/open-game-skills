---
name: unity
description: Use when an existing Unity project needs open-game-skills timing, pose, collision, hitstop, input, or camera contracts mapped onto its actual PlayerLoop and physics settings.
---

# Unity adapter

Inspect the project's Unity version, `Time` settings, physics backend and existing update ownership before binding gameplay clocks.

## Timing

`Update` is frame-driven. `FixedUpdate` follows the configured fixed timestep and `Time.fixedDeltaTime`; a rendered frame may observe zero, one or multiple fixed updates. Do not equate either callback with a universal 60 Hz game clock.

If the project already owns a deterministic gameplay accumulator, preserve it. Physics-facing work may run in `FixedUpdate`; presentation/interpolation may run in `Update`/`LateUpdate`. Keep the discipline's logical phase order explicit across those boundaries.

Per-actor hitstop pauses the selected actor/action clock, Animator or authored simulation state. Do not use global `Time.timeScale` as a substitute for per-actor combat freeze; a separately designed global pause may still own it.

## Bindings

- input: existing Input System/legacy input adapter into semantic actions;
- pose: Animator/manual pose under actor-local time ownership;
- hits: layer-filtered authored gameplay volumes on the logical step;
- knockback: project movement/physics solver, not render transform teleport;
- camera: project Cinemachine/cast solution implementing `camera-anti-clip` rules.

## Accept

Record Unity version, `Time.fixedDeltaTime`, relevant physics settings and which callback owns each logical/presentation phase. Replay the same logical trace under different render rates; verify gameplay outcomes and per-actor freeze ownership, while reporting presentation-latency differences separately.
