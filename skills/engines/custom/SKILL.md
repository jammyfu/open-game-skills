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

## Lifecycle and resources

The engine-neutral rules live in `audio-feel`, `juice-vfx`, `asset-runtime`, `performance-budget` and `soak-stability`; this section only maps them onto a custom runtime. Document:

- the audio-output availability states (locked, device lost, background) and where cues are dropped or fall back;
- the focus/background/suspend/device-loss hooks and the catch-up limit applied on resume;
- the pools/arenas for frequently spawned effects and voices, and the release point of every engine/GPU/audio handle;
- the overlay draw order relative to HUD-critical elements.

Camera anti-clip follows `camera-anti-clip`: protect the actual camera/frustum footprint and final offsets rather than relying on a single point ray.

## Asset pack import

A validated asset pack is plain images, JSON and audio, so any runtime can consume it: read the manifest, load atlas JSON (frame rectangle, source size, trim offset, pivot, tick holds, animation lists), read Tiled `.tmj`/`.tsj` (row-major gid arrays, gid minus one as tile id, tile `type` as semantics, objects anchored at their tile bottom) and the feel/box/enemy/audio data files. Keep the pack's declared logical clock separate from render frequency, apply integer scaling and nearest filtering for pixel styles, and record the loader build and what it reproduced as import evidence.

## Accept

Record engine/runtime build identity, loop diagram, configured clock rates, phase order and pause ownership. Replay a deterministic input/contact trace at at least two render cadences where the runtime permits; logical results must match, and untested timing modes remain `not-run`.

Record the lifecycle hooks and resource release points used. A burst, teardown and background/resume cycle returns live effect, voice, timer and handle counts to the warm-up baseline; untested platforms remain `not-run`.
