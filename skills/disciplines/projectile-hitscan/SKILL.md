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
- exactly one terminal event per `projectile_id`, with a reason (impact, blocked, mutual cancel, expiry, out-of-bounds, owner/round reset)

Hitscan resolves its query at the authoritative fire confirm. A projectile advances using the project simulation and resolves contacts by projectile/event identity. A beam defines an authored occupancy/sample policy and applies each target/sample identity at most once as specified.

Do not use a universal number of self-ignore frames. Self/friendly filtering comes from explicit source identity, layer/team rules, spawn geometry policy, or other project data.

## Runtime rules

1. One `shot_id` cannot commit the same impact twice.
2. Presentation tracers, muzzle flashes and impact particles never author damage or collision.
3. Network prediction/correction delegates to `netcode-feel`; this skill preserves shot/projectile identity across reconciliation.
4. Random spread is provided by its handling/RNG owner and is recorded as part of the authoritative shot request.
5. A stale collision/filter revision is rejected or reconciled explicitly.
6. Projectile-vs-projectile cancellation is an explicit resolution policy. It states which classes cancel, how it orders against actor contacts in the same step, and that a consumed projectile cannot also commit an actor impact in that step. Both projectiles publish terminal events.
7. Per-owner projectile limits release on the terminal event, so a cancelled projectile frees its slot exactly once. Presentation (`juice-vfx`, `audio-feel`) ends entity-bound effects from the same terminal events.

## Acceptance

The same authoritative shot request and collision state produce the same canonical ordered impact results. Changing only tracer length, camera shake, reticle or other presentation cannot alter hit/no-hit truth.

Replay a mutual-cancel trace. Each projectile publishes one terminal event, none remains live, no actor impact is committed, and both owners can fire again under their limits.
