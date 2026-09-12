---
name: lock-on-target
description: Generic lock-on. One target, a pip, camera helps. Marker, facing, attack yaw, and camera must agree.
---

# Lock-on target

Ask: soft-lock | hard-lock | none.
Soft-lock steers the stick toward a nearby foe. Hard-lock pins camera + attack yaw to one actor until cancel.
Cycle next/prev is a button, not a mouse flick, unless kb-mouse-map is fps-look.
Lost target (dead, occluded, out of range) drops cleanly. Do not snap to a third body behind the camera.
Pip lives in hud-feedback. Camera assist must still run camera-anti-clip.

## One target

Lock pip, actor facing, attack direction, and camera look-at are the same actor. If any one disagrees, drop or retarget — do not keep a split lock.

Melee lock and bow / mouse aim are two accept passes (`kb-mouse-map`). Occlusion, death, and multi-target cycle are required scenes in `gameplay-validation`, not optional juice.

Accept: the player can name who they are locked to without the HUD. After the target dies, the next tap is a new lock or none, not a ghost.
