---
name: threejs
description: Use when an existing Three.js or React Three Fiber game needs skill contracts mapped onto its render loop, animation mixers, logical simulation, collision data, input, or camera system.
---

# Three.js / R3F adapter

Inspect the installed Three.js/R3F package versions and the project's existing loop before deciding where simulation lives.

## Timing

`requestAnimationFrame` and R3F `useFrame` are frame-driven callbacks, not fixed gameplay ticks. `AnimationMixer.update(deltaTime)` advances animation by the supplied elapsed time and is commonly called from the render loop; it is presentation/animation timing unless the project explicitly makes it authoritative.

If the game already has a fixed logical accumulator, preserve its configured rate. If deterministic gameplay requires one and none exists, introduce an explicit accumulator as a project decision rather than hardcoding 60 Hz. `useFrame` may feed elapsed time into that accumulator, but render cadence never becomes the logical tick by implication.

## Bindings

- input: browser/device adapter into semantic actions;
- pose: `AnimationMixer.update(delta)` for presentation or logical pose snapshots where required;
- hits: authored Box3/sphere/capsule/custom gameplay volumes, not render mesh visibility;
- knockback: logical movement/collision owner;
- camera: collision-aware sweep/volume test implementing `camera-anti-clip`, not a single point ray.

Per-actor hitstop freezes that actor's logical/animation clock; do not stop the whole render loop.

## Lifecycle and resources

The engine-neutral rules live in `audio-feel`, `juice-vfx`, `asset-runtime`, `performance-budget` and `soak-stability`; this section only maps them onto Three.js in a browser.

- audio output: a Web Audio context starts suspended until a user gesture, so call `resume()` from one. Decode or synthesise buffers outside the presenting frame.
- background: hidden documents throttle or stop `requestAnimationFrame`. Clamp the logical accumulator's catch-up after resume, and do not take frame-time evidence from a hidden page.
- release: removing an `Object3D` does not dispose its geometry, material or texture. Share or pool them, and call `dispose()` through the lease owner when the last consumer releases them. Many small particles fit an `InstancedMesh` or a pooled buffer better than one mesh/material each.
- overlays: DOM/CSS layers (screen flashes, CSS filters on the canvas, overlay canvases) need explicit stacking against HUD elements. Clear their timers and restore filters on teardown.

## Accept

Record package versions, render-loop owner, configured logical tick (if any) and interpolation policy. Replay the same logical trace at multiple render rates; verify logical states/contact IDs match and report render/presentation latency separately.

Record the lifecycle hooks and resource release points used. A burst, teardown and background/resume cycle returns live effect, voice, timer and handle counts to the warm-up baseline; untested platforms remain `not-run`.
