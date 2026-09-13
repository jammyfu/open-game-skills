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

Display objects are presentation. Gameplay collision uses an explicit AABB/SAT/custom graph or physics integration, not the scene graph itself.

## Accept

Record PixiJS version, shared/private ticker choice, configured logical loop (if any) and collision owner. Test variable frame cadence, stop/start/visibility recovery and per-actor hitstop without freezing unrelated actors; distinguish logical determinism from display latency.
