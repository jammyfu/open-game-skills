---
name: juice-vfx
description: Use when authoritative gameplay events need flashes, particles, trails, hit sparks, screen/camera accents or other runtime VFX presentation that must not own damage, hitboxes, timing or simulation.
---

# Juice and VFX

This skill owns runtime **presentation** effects. Asset generation belongs to `vfx-generate`; gameplay state remains authoritative in its domain owner.

## Compatible modes

| Mode | Presentation density |
|---|---|
| dry | minimal/no optional VFX |
| punchy | selected short accents |
| maximal | richer authored layers within performance/accessibility budgets |

## Event contract

Each effect binds to an authoritative event/state ID and declares spawn anchor, lifetime/end condition, stacking/retrigger policy, ownership/cleanup, performance class and accessibility fallback/reduction behavior.

## Rules

1. Spawn VFX only after/while the authoritative logical state says the event exists; particles/screenshake never create hits or damage.
2. Lifetime, opacity, shake and particle counts are authored project values, not universal millisecond constants.
3. Reduced-flash/motion settings preserve required information through pose/UI/audio/other supported channels rather than silently changing gameplay.
4. Camera offsets route through the camera safety/collision contract (`camera-anti-clip`) when they change the final camera transform.
5. Performance degradation removes/scales optional presentation according to `performance-budget`; it never removes gameplay collision/data.
6. Cancellation, rollback/re-simulation, retry and scene teardown use stable event/effect identity to avoid duplicate or stale effects.
7. Entity-bound effects (projectile bodies, beams, auras, weapon glows) end on every authoritative removal path: impact, block, mutual cancel, expiry, owner reset and scene/round teardown. As a fallback, each presentation update reconciles live effect IDs against the authoritative entity set and retires orphans. Orphans are logged, because each one means an end event is missing.
8. Full-screen accents in the same beat (flash, impact/negative frame, focus or speed lines, vignette) declare a sequence or priority so one does not mask another. They render beneath HUD-critical state unless the project explicitly allows covering it.
9. Size, anchor and direction come from event and actor data: contact point, actor scale and attacker-to-defender direction. Review them in frame captures for occlusion of critical reads such as the defender's face/pose or the HUD.
10. Trails and smears sample skeletal sockets after the current pose update and end with the action instance's authored window. Reduced settings remove them without removing required information.

## Runtime cost and cleanup

1. Each effect class declares an instance cap and a degradation order under `performance-budget`: optional layers lose count/size first, and required information survives. Bursts such as rapid hits or projectile spam stay within the cap through an explicit steal/skip policy.
2. Reuse geometry, materials, textures and particle buffers through pools, instancing or shared assets. Do not create and destroy engine/GPU resources per hit on the hot path. Generated resources (canvas textures, procedural meshes) are cached with an owner instead of rebuilt per spawn.
3. Every instance ends by returning to its pool or releasing its handles through `asset-runtime`. This includes timers, listeners, overlay UI nodes and temporary global state such as screen filters, post-process toggles or time scale, which must be restored. Scene/round teardown clears active instances and pending timers.

## Accept

Replay identical logical traces with VFX on/off/reduced and under re-simulation/retry where relevant. Gameplay state is identical; effect instances have explainable event IDs, cleanup and fallback behavior.

Review composition from captures taken at fixed offsets after a named event. Freeze-on-event debug hooks are acceptable evidence when labeled as such. A reduced run shows zero instances of the reduced optional classes. A mutual-cancel or expiry trace leaves no live entity-bound effect. A burst trace stays within the declared caps and frame budget. After teardown, live effect/resource counts return to the warm-up baseline.
