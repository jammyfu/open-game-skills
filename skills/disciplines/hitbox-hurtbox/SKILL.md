---
name: hitbox-hurtbox
description: Attack boxes and vulnerable boxes are data on the move, not the mesh. Ask 2d-boxes vs 3d-capsules vs projectile-volume. query_hits reads these. Use when the user talks about 判定盒, clash, or trade.
---

# Hitbox and hurtbox

Ask the column:

| Column | Shape |
|---|---|
| 2d-boxes | AABB / OBB on a plane |
| 3d-capsules | body + limb capsules |
| projectile-volume | spawned volume with lifetime |

## Rules

1. Boxes live on move frames. A pretty mesh is not a hit.
2. Active frames publish a box. Recovery has no box unless the data says so.
3. Throw / grab is a different box class, not a bigger punch.
4. Clash / trade is a column. Default: both hurtboxes can be hit the same frame.
5. query_hits runs on the logic step. Render interpolation must not widen a box.

## Accept

- Turning off meshes still lets two actors trade
- A 2-hit confirm uses the published boxes, not magnet
