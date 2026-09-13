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

## Accept

Replay identical logical traces with VFX on/off/reduced and under re-simulation/retry where relevant. Gameplay state is identical; effect instances have explainable event IDs, cleanup and fallback behavior.
