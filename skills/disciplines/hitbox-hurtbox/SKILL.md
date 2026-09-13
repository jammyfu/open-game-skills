---
name: hitbox-hurtbox
description: Use when attack, vulnerability, grab, projectile, clash, trade, multi-hit, or duplicate-hit collision volumes need a deterministic gameplay contract.
---

# Hitbox and hurtbox

Choose the representation required by the game:

| Column | Shape |
|---|---|
| 2d-boxes | AABB / OBB on a gameplay plane |
| 3d-capsules | body/limb capsules or other declared primitives |
| projectile-volume | spawned gameplay volume with lifetime |

## Ownership and identity

Hitboxes and hurtboxes are gameplay data, not render meshes. Active move ticks publish attack volumes; vulnerable state publishes hurt volumes independently.

Each attack activation has a stable `attack_instance_id`. A multi-hit move additionally publishes a `hit_index` or equivalent schedule. Duplicate-hit prevention is keyed by attack instance, hit index and target according to the move policy; it is not inferred from overlap duration.

Grab/throw, strike, projectile and clash volumes are distinct interaction classes. Eligibility rules decide which classes can affect the target.

## Same-tick resolution

`query_hits` reads a logic-tick snapshot. Collect candidates before mutating reaction state so entity/container iteration order cannot erase a legitimate trade. Then resolve candidates through the project's explicit priority/trade/clash policy.

Render interpolation may move pictures between ticks; it must not widen gameplay volumes or create extra contacts.

## Accept

Disable render meshes and replay a same-tick trade with entity iteration reversed: the logical result is unchanged. Hold one hitbox overlapping a target for several ticks and verify the published single-hit or multi-hit schedule exactly. Draw attack/hurt/grab volumes and log attack instance IDs for debugging; visuals alone do not prove resolution behavior.
