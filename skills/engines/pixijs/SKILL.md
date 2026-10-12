---
name: pixijs
description: Use when an existing PixiJS game needs skill contracts mapped onto its Ticker, scene graph, input, animation, collision graph, or a project-owned logical simulation loop.
---

# PixiJS adapter

Inspect the PixiJS version and whether the application uses a shared, private, manual, or custom Ticker before changing timing ownership.

## Timing

PixiJS `Ticker` callbacks are frame-driven and normally run once per animation frame. `deltaTime`/`deltaMS`, min/max FPS controls and clamping do not by themselves create deterministic fixed-step gameplay.

If the project already has a logical accumulator, preserve its configured rate. Add a fixed accumulator only when the game's discipline contract requires it; do not declare 60 Hz as an engine requirement. Rendering and interpolation may remain on Ticker cadence.

Hitstop freezes only the selected actor/action/animation clock. Never use `ticker.stop()` as per-actor hitstop because it pauses unrelated listeners/rendering.

## Lifecycle and resources

The engine-neutral rules live in `audio-feel`, `juice-vfx`, `asset-runtime`, `performance-budget` and `soak-stability`; this section only maps them onto PixiJS.

- audio output: browser autoplay rules apply to whichever audio library the project uses; unlock from a user gesture.
- background: the `Ticker` follows animation frames, which hidden tabs throttle. Clamp catch-up after visibility returns.
- release: `destroy()` options decide whether textures go with a display object. A consumer must not destroy a texture that another consumer still uses. Pool frequently spawned sprites/effects instead of creating them per hit, and use the installed version's particle container for large counts.
- overlays: container order and `zIndex` (with sorting enabled on the parent) keep flashes beneath HUD-critical elements.

Display objects are presentation. Gameplay collision uses an explicit AABB/SAT/custom graph or physics integration, not the scene graph itself.

## Accept

Record PixiJS version, shared/private ticker choice, configured logical loop (if any) and collision owner. Test variable frame cadence, stop/start/visibility recovery and per-actor hitstop without freezing unrelated actors; distinguish logical determinism from display latency.

Record the lifecycle hooks and resource release points used. A burst, teardown and background/resume cycle returns live effect, voice, timer and handle counts to the warm-up baseline; untested platforms remain `not-run`.
