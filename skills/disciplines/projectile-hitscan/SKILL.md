---
name: projectile-hitscan
description: >
  Ranged hit as a move row. Use when only melee boxes exist, when a bullet
  hits the shooter, or when a tracer leads the logic ray. Stacks on
  hitbox-hurtbox and collision-layers. Not aim-assist.
---

# Projectile / hitscan

Ask the column. One column per weapon row.

| Column | Logic hit |
|---|---|
| hitscan | ray this tick; tracer is juice after |
| projectile | body with speed; hit on overlap this tick or later |
| beam | occupancy each tick while held |

Authority is the sim that owns `query_hits`. Cosmetic tracers do not deal damage.

## Move row fields

```
column
speed (0 = hitscan)
max range / life
pierce count
who-layer (collision-layers)
self-ignore frames after spawn
```

Hitscan still spends the same startup / recover as a melee row (action-feel).
Spread and recoil belong to aim-assist / fps-feel if present; they do not move the hurtbox.

## Iron rules

- Firer is ignored for N frames or by layer. A shotgun must not kill the shooter.
- Hitscan damage is applied on the logic tick of the fire confirm, not when the tracer sprite arrives.
- Projectile teleport-for-catchup is netcode-feel, not this file. Do not secretly hitscan a projectile to hide lag.
- Friendly filter is collision-layers / target-priority, not a hidden 0-damage.
- Juice (muzzle, tracer, impact) after the logical hit. See juice-vfx.

## Accept

A debug ray or ghost body matches the damage event. Changing only the tracer length does not change who dies.
