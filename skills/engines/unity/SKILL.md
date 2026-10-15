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

## Lifecycle and resources

The engine-neutral rules live in `audio-feel`, `juice-vfx`, `asset-runtime`, `performance-budget` and `soak-stability`; this section only maps them onto Unity.

- audio output: WebGL builds inherit browser autoplay rules. The project's real/virtual voice limits (Audio settings) and the cue's steal policy cap retriggered voices.
- background: `OnApplicationPause` / `OnApplicationFocus` and `Application.runInBackground` define what happens to loops, timers and catch-up when focus or foreground is lost.
- release: pool spawned effects (for example `UnityEngine.Pool.ObjectPool<T>` where available) instead of `Instantiate`/`Destroy` per hit. Accessing `Renderer.material` creates a per-renderer copy that must be destroyed; use `sharedMaterial` or a `MaterialPropertyBlock` for per-hit tint. Release Addressables handles explicitly; destroying a GameObject does not release them.
- overlays: Canvas `sortingOrder` keeps flashes beneath HUD-critical elements.

## Asset pack import

For a validated asset pack, import sprites with point filtering and no compression for pixel styles, bilinear for the cartoon style, and a pixels-per-unit equal to the pack's tile size. Take pivots from the atlas JSON (actors use bottom-centre), slice by its rectangles, and use a Pixel Perfect Camera whose reference resolution is the profile's virtual resolution (for example 640x360) with the game view at 1920x1080, so the upscale is an exact integer; the cartoon style is native 1080p without pixel snapping. Switch art style by changing one style id and resolving every asset key through the pack's `styles.json` (2D sprite atlases, or GLB models with their node and clip names for `toon-3d`); levels, tile-unit hitboxes and tick tables are shared by all styles. A pack's tick tables are authored on its declared logical clock: set `Time.fixedDeltaTime` to match it or rescale every feel value, and record which. Tiled maps are data; read their layers and object properties with a loader of your choice. Engine import evidence is separate from playthrough evidence.

## Accept

Record Unity version, `Time.fixedDeltaTime`, relevant physics settings and which callback owns each logical/presentation phase. Replay the same logical trace under different render rates; verify gameplay outcomes and per-actor freeze ownership, while reporting presentation-latency differences separately.

Record the lifecycle hooks and resource release points used. A burst, teardown and background/resume cycle returns live effect, voice, timer and handle counts to the warm-up baseline; untested platforms remain `not-run`.
