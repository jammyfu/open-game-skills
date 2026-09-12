---
name: performance-optimization
description: Frame time is a design constraint. Ask 30-stable vs 60-stable vs unlocked-with-floor vs handheld-dock-dual. Profile before cutting art. Never fake speed or hitstop by scaling Engine.time.
---

# Performance optimization

Ask the column:

| Column | Contract |
|---|---|
| 30-stable | 33.3ms, no stumble |
| 60-stable | 16.6ms, logic at 60 |
| unlocked-floor | present as fast as possible, logic fixed, floor 30 or 60 |
| handheld-dock-dual | two published budgets, same cartridge |

## Rules

1. Logic step is fixed. Render may skip frames. Feel lives on the logic clock.
2. Budget the frame before the asset: CPU sim, GPU opaque, GPU transparent, UI, audio, GC.
3. Cut in this order: off-screen work, overdraw, shadow casters, particle lifetime, simultaneous AI, then mesh LOD.
4. Hitch is worse than a lower cap. A 60 that falls to 12 on a burst fails 60-stable.
5. Do not shrink hitstop, input windows, or vehicle accel to hide a miss.
6. Measure on the target device. See platform-targets.

## Accept

- A 5-minute slice on the target device holds the published cap
- Combat, race boost, or boss VFX does not drop below the floor
- A loading hitch is named and owned
