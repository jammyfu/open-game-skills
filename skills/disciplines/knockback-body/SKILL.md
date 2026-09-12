---
name: knockback-body
description: The body that rides knockback-launch. Capsule stays on nav. Use for 受击位移, 击飞身体.
---

# Knockback body

Pairs with `knockback-launch`. The vector is data; the body must not tunnel.

Rules: sweep the same capsule the pawn walks with (`nav-mesh`). Hitstop ends, then the sweep (`action-feel`). Landing lag starts when the capsule finds floor (`landing-lag`). Wall contact may splat (`wall-splat`) or slide, published. Fat costumes do not change the capsule.

Accept: a launch cannot put them inside a wall. Training draws the capsule at takeoff and land.
