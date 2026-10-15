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

## Lifecycle and resources

The engine-neutral rules live in `audio-feel`, `juice-vfx`, `asset-runtime`, `performance-budget` and `soak-stability`; this section only maps them onto Phaser.

- audio output: on web the sound manager reports `locked` until a user gesture unlocks it (listen for its unlock event). Cues requested while locked follow the fallback.
- background: the game emits `hidden`/`visible` events. Pause/resume loops there and clear held input through `browser-input`.
- release: pool frequently spawned objects with a `Group` (`get()` and `killAndHide()`) rather than creating and destroying per hit. `destroy()` game objects, particle emitters and timers that the scene owns on shutdown.
- overlays: depth or a dedicated UI scene keeps flashes and overlays ordered against HUD-critical elements.

## Asset pack import

For a validated asset pack, load atlases as hash atlases (the pack's TexturePacker-style JSON also lists animations per frame name) or as Aseprite exports when their frame tags are wanted; frame durations in those files are preview hints, the pack's tick tables remain the authority. Pixel styles need pixel-art rendering and `width`/`height` equal to the profile's virtual resolution with an integer `zoom` (for example 640x360 at zoom 3 is exactly 1920x1080; never a fractional zoom); the cartoon style is native 1080p without `pixelArt`. Switch art style by changing one style id and resolving each asset key through the pack's `styles.json`; the level maps, tile-unit hitboxes and tick tables are shared by all styles, and a `toon-3d` style needs a separate 3D renderer rather than Phaser sprites. Load Tiled maps with `tilemapTiledJSON`; tilesets may be external, so inline or convert them first. Inspect the installed Phaser version before choosing loader calls, and record import evidence separately from gameplay evidence.

## Accept

Record Phaser version, TimeStep/physics configuration, logical-step owner and visibility recovery policy. Test low/high frame rates and tab-hide/resume; logical contacts must not duplicate or disappear because Scene update cadence changed.

Record the lifecycle hooks and resource release points used. A burst, teardown and background/resume cycle returns live effect, voice, timer and handle counts to the warm-up baseline; untested platforms remain `not-run`.
