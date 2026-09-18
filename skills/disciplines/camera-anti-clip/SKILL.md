---
name: camera-anti-clip
description: Use when a gameplay camera clips through solids, flickers near thin geometry, exposes the inside of walls, or final camera offsets can escape collision-safe space.
---

# Camera anti-clip

Choose the camera column before tuning collision:

| Column | Pivot | Occlusion policy |
|---|---|---|
| orbit-third | chest / authored target | decollide; deocclusion optional |
| over-shoulder | shoulder target | decollide hard |
| sidescroll | plane target | constrain depth and near-plane clearance |
| lock-strafe | shared framing target | preserve both actors when feasible |
| first-person | eye | near-plane clearance only |

## Collision contract

1. Solve from an authored pivot/target to the desired camera transform on the logical/render preparation step after actor pose is known.
2. Collision must protect the **camera frustum near plane**, not only the camera origin. Use a conservative sphere/capsule/probe radius derived from near-plane half extents, FOV/aspect and skin, or an equivalent multi-probe method supported by the adapter.
3. Ignore only explicitly owned player/camera helper colliders. Do not globally ignore dynamic geometry.
4. On obstruction, move to the nearest collision-safe pose immediately enough to prevent penetration; when clear, recover with a separately authored easing policy.
5. Decollision and deocclusion are separate policies. Fading foliage must not hide a solid wall or collapse a third-person camera into an unintended first-person pose.
6. Camera shake, recoil and shoulder offsets are part of the **final camera transform budget**. Apply them before the final safety validation, or clamp/re-sweep the displaced pose. An offset may never bypass collision just because it is presentation.
7. Moving geometry is sampled consistently with its rendered/logical pose. Do not parent the camera to a rolling root bone to fake collision.
8. Invasive low-angle or private-zone framing is owned by `camera-modesty`. A collision-safe pose can still fail that policy.

## Accept

Test wall-backup, thin pillars, inside corners, low ceilings, climbing over a lip, moving geometry, wide/narrow aspect ratios, minimum/maximum FOV, and maximum authored shake/recoil. The near plane never crosses a solid and clear/blocked transitions do not flicker. Record the final safe camera pose and obstruction normal; screenshots alone are not collision evidence.
