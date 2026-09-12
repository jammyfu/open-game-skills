---
name: lock-on-target
description: Generic lock-on. One target, a pip, camera helps. Use for action and souls-like. Not a painted floor.
---

# Lock-on target

Ask: soft-lock | hard-lock | none.
Soft-lock steers the stick toward a nearby foe. Hard-lock pins camera + attack yaw to one actor until cancel.
Cycle next/prev is a button, not a mouse flick, unless kb-mouse-map is fps-look.
Lost target (dead, occluded, out of range) drops cleanly. Do not snap to a third body behind the camera.
Pip lives in hud-feedback. Camera assist must still run camera-anti-clip.

Accept: the player can name who they are locked to without the HUD.
