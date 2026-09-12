---
name: fps-feel
description: >
  First-person gun feel. Use when ads, recoil, view kick, or weapon swap
  is missing, or when a fighter clock is copied onto a gun. Not lock-on.
  Not projectile-hitscan. Stacks on aim-assist and kb-mouse-map / fps-look.
---

# FPS feel

Ask the column.

| Column | What it owns |
|---|---|
| hip-fire | wide cone, short ready |
| ads | narrower cone, published raise time, slower move |
| recoil-pattern | view kick + recover on the logic tick |
| swap-holster | weapon change as a move row with recover |

Hitscan vs projectile lives in projectile-hitscan. This file is the body and camera of the gunner.

## Iron rules

- Recoil is a published pattern. It is not random each shot unless rng-seed says so and is replayable.
- View kick is juice after the fire confirm. It does not secretly move the hitscan origin after query_hits.
- ADS raise / drop has startup and recover. Cancel windows stay in action-feel if the gun can cancel.
- Do not put grounded-footsies on a rifle actor. One combat clock.
- Reload is a move row. Inventory ammo count is inventory-economy.

## Accept

Hip and ADS are two readable states. A clip of recoil recover matches the pattern table. Swapping weapons cannot fire the old gun on the same tick.
