---
name: camera-anti-clip
description: >
  Engine-neutral camera collision. Sphere sweep from pivot to desired pose.
  Pick a rig column first. Use when the camera enters walls, sits on a thin
  ray hit, or collapses into the spine.
---

# Camera anti-clip

Ask the rig column first.

| Column | Rig | Collision |
|---|---|---|
| orbit-third | yaw/pitch arm | always sweep |
| over-shoulder | arm + socket offset | offset rotates with the arm |
| sidescroll | plane, depth locked | clamp to room bounds |
| lock-strafe | orbit while locked | lock is overlay, not a rail |
| first-person | eye socket | capsule vs world |

Two jobs: **decollision** (body not inside a wall, default on) vs **deocclusion** (keep subject visible, optional). Leaves and fences often fade. Do not yank to first-person.

## Per frame (after the subject moves)

```
desired = pivot + orbit(yaw,pitch)*(0,0,-arm) + socket
sweep sphere pivot → desired
radius >= max(near_clip, 0.15..0.25)
mask = World, ignore = Player
if hit: desired = hit.point + hit.normal * radius
damp: collide ~0.05s, release ~0.25s
look at pivot
```

## Iron rules

- No single ray parked on the hit point.
- Camera layer != player layer.
- Do not parent the camera to a rolling animation root.
- Shake is an offset applied AFTER the sweep.
- Pitch is clamped.

## Accept

Corner + 360 spin: no interior faces, no one-frame wall flash, release eases out.
