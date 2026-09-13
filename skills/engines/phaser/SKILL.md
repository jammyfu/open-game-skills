---
name: phaser
description: Use when an existing Phaser project needs skill contracts mapped onto its TimeStep/Scene update loop, input, Arcade or Matter physics, animation, camera, and project-specific logical timing.
---

# Phaser adapter

Inspect the installed Phaser version, game-loop/physics configuration and existing Scene architecture first; Phaser 3/4 APIs and defaults are not interchangeable assumptions.

## Timing

Phaser Core `TimeStep` is driven by browser frame events (typically requestAnimationFrame) and feeds the Game/Scene update loop. `Scene.update` is therefore frame-driven unless the project deliberately layers a fixed logical accumulator or uses a configured physics step for a bounded subsystem.

Do not claim a universal 60 Hz logical step. Preserve the project's configured simulation owner/rate and feed presentation from it. Browser focus/visibility can pause the heartbeat; recovery must clear/reconcile held input through `browser-input` rather than simulating an enormous catch-up delta.

## Bindings

- input: keyboard/gamepad/pointers → semantic actions;
- pose: sprite animations/Spine under actor-local time ownership;
- hits: Arcade/Matter queries or authored logical hit volumes, never render-list membership;
- knockback: owned body/logical movement phase;
- juice: cameras/particles after logical resolution.

Per-actor hitstop is not `scene.physics.pause()` and does not stop `game.loop`.

## Accept

Record Phaser version, TimeStep/physics configuration, logical-step owner and visibility recovery policy. Test low/high frame rates and tab-hide/resume; logical contacts must not duplicate or disappear because Scene update cadence changed.
