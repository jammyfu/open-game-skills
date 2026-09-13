---
name: collision-layers
description: Use when gameplay, projectiles, actors, world geometry, hazards, cameras, IK or sensors need explicit collision/query categories and a reviewable interaction matrix.
---

# Collision layers

This skill owns **stable collision/query category IDs and their interaction matrix**. It does not own hit resolution (`hitbox-hurtbox`), world navigation/body motion, camera collision response or IK contact solving.

## Matrix

Publish stable semantic categories and allowed interaction/query pairs, for example project-specific equivalents of:

```text
pawn-body
world-solid
attack-volume
hurt-volume
grab-volume
projectile-volume
hazard/sensor
camera-query
ik-ground-query
```

Names and count are project data. Rendering/costume/material layers are not automatically gameplay collision layers.

## Rules

1. `hitbox-hurtbox` owns attack/hurt/grab meaning and stable hit identity; this skill only allows/blocks candidate layer pairs.
2. World/pawn blocking and movement response stay with the movement/physics owner; `hazard-volume` owns hazard semantics.
3. Projectile friendly-fire/team policy is explicit project data rather than an assumed universal default.
4. `camera-anti-clip` and `ik-foot-locking` use dedicated query masks/categories so presentation probes do not accidentally trigger gameplay contacts.
5. Layer IDs/masks remain stable across asset/costume swaps; catalog reorder or visual skin changes do not silently alter collision behavior.

## Accept

Export/draw the interaction matrix and replay representative allowed/blocked pairs. Changing render assets leaves layer IDs/pairs unchanged, and every gameplay contact still resolves through its domain owner rather than the mask alone.
