---
name: camera-anti-clip
description: Keep the camera out of world geometry. Sphere sweep from pivot to desired pose. Use for third-person clip, wall suck-in, orbit collision. Ask the camera column first. Never start from SpringArm3D or Cinemachine.
---

# Camera anti-clip

Ask the column:

| Column | Pivot | Occlusion |
|---|---|---|
| orbit-third | chest | decollide; fade optional |
| over-shoulder | shoulder | decollide hard |
| sidescroll | plane lock | push on depth only |
| lock-strafe | lock point | keep both actors framed |
| first-person | eye | near-plane only |

## Rules

1. Sweep a sphere, not a single ray. Radius >= nearClip + skin.
2. Hit this frame: pull in immediately. Clear: ease out (fast-in, slow-out).
3. Ignore the player collider and the camera body.
4. Decollision is default. Deocclusion (see through foliage) must not collapse to first-person.
5. Solve after actor pose, before render. Do not parent to a rolling root bone.
6. Shake and kick are offsets applied after the sweep.

## Accept

- Back into a wall: lens never crosses the solid
- Thin pillar: no per-frame flicker
- Climb over a lip: camera sees the ledge, not the interior
