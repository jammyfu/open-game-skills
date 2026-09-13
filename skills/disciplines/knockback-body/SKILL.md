---
name: knockback-body
description: Use when a character or enemy must physically traverse knockback or launch motion without tunneling, embedding in walls, or losing deterministic floor/wall response.
---

# Knockback body

Pairs with `knockback-launch`: launch owns the intended trajectory parameters; this skill owns collision-safe body motion.

Use the gameplay collision proxy published for the actor. If knockback uses a different proxy from locomotion, declare why and test the transition; do not silently switch shapes because a costume is larger.

## Collision response

Sweep/continuous-test the displacement required by the target physics system rather than teleporting through geometry. Publish wall response as one of:

| Response | Result |
|---|---|
| stop | consume blocked component and stop/settle |
| slide | project remaining motion along the contact surface |
| splat-state | enter an authored wall reaction when speed/angle/state thresholds match |

`splat-state` is a reaction state, not a reference to a nonexistent skill. Its stun/recovery timing is owned by `hitstun-recover`.

Floor contact publishes the landing event consumed by `landing-lag`. Slopes, moving surfaces and corners need the same collision evidence as flat floor.

## Accept

Sweep representative launches into thin walls, corners, slopes and floor at the maximum supported displacement. The body never ends embedded or on the wrong side of geometry; wall response and landing tick are reproducible. Draw the collision proxy and contact normal at takeoff, impacts and landing.
