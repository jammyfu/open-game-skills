---
name: character-rig
description: Generic character skeleton contract so locomotion IK and weapon sockets work across engines.
---

# Character rig

Minimum humanoid: pelvis, spine×2, neck, head, clavicle, upperArm, lowerArm, hand, thigh, shin, foot, **toe**.
Foot lock targets the toe, not the heel. Missing toe = do not load `ik-foot-locking`.
Forward axis is consistent. Bind in a rest pose, not a random key.
Sockets: weapon_r/l, bow, camera_pivot, hit_flash.
Export with the same facing the engine adapter expects. No silent 180° fixes in code.
