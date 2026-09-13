---
name: projectile-hitscan
description: Use when ranged attacks need authoritative hitscan, projectile, or beam query identity, stable shot/projectile events, collision filtering and replayable hit evidence independent from tracers, reticles or aim assistance.
---

# Projectile / hitscan

Ask: `hitscan | projectile | beam`.

## Ownership

This skill owns ranged query/impact resolution. `aim-assist` and `fps-feel` may supply handled aim intent; `collision-layers` supplies filtering; `action-feel` supplies action timing; `juice-vfx` renders muzzle/tracer/impact presentation.

## Contract

For every fire request publish:
- stable `shot_id`
- source actor / weapon / action IDs
- fire-confirm logical frame or project time identity
- authoritative origin/direction or projectile initial state
- collision/filter revision
- optional `projectile_id`
- ordered hit/impact event IDs

Hitscan resolves its query at the authoritative fire confirm. A projectile advances using the project simulation and resolves contacts by projectile/event identity. A beam defines an authored occupancy/sample policy and applies each target/sample identity at most once as specified.

Do not use a universal number of self-ignore frames. Self/friendly filtering comes from explicit source identity, layer/team rules, spawn geometry policy, or other project data.

## Runtime rules

1. One `shot_id` cannot commit the same impact twice.
2. Presentation tracers, muzzle flashes and impact particles never author damage or collision.
3. Network prediction/correction delegates to `netcode-feel`; this skill preserves shot/projectile identity across reconciliation.
4. Random spread is provided by its handling/RNG owner and is recorded as part of the authoritative shot request.
5. A stale collision/filter revision is rejected or reconciled explicitly.

## Acceptance

The same authoritative shot request and collision state produce the same canonical ordered impact results. Changing only tracer length, camera shake, reticle or other presentation cannot alter hit/no-hit truth.
