---
name: collision-layers
description: Who hits whom. Layers, not one blob. Use for 碰撞层, 弹道穿过队友.
---

# Collision layers

Ask first: which pairs may touch — pawn-world, hit-hurt, projectile-hurt, pawn-pawn?

Rules: hit vs hurt is `hitbox-hurtbox`. World vs pawn is `nav-mesh` / `hazard-volume`. Friendly projectiles do not hit allies unless the column is friendly-fire. Camera and foot IK use their own masks (`camera-anti-clip`, `ik-foot-locking`).

Accept: a training overlay can color the layers. A costume never adds a layer.
