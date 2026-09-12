---
name: ik-foot-locking
description: Lock toes on contact so feet do not slide. Two-bone leg IK plus a contact state machine and inertialization. Use for walk/run on terrain. Do not rebuild the whole skeleton.
---

# IK foot locking

Source shape: Daniel Holden, Inverse Kinematics and Foot Locking. Engine-neutral.

## Rules

1. IK is a pose fix, not a locomotion owner. Locomotion writes the root; this skill edits the leg after.
2. Lock the toe, not the heel.
3. Soft-clamp extension. Never pull the pelvis to reach a target.
4. Contact = toe world speed below a threshold (start at 0.1-0.5 m/s) AND height sanity AND a 3-5 frame majority vote.
5. Unlock with the same vote so one noisy frame cannot pop the foot.
6. Blend with inertialization: keep the old offset, then decay toward the new solve. Do not lerp two world targets.
7. Ground height comes from a probe, never y = 0.

## Accept

- During a locked contact, toe travel < 1 cm
- Slope and stairs keep contact without skating
- Unlock into a stride does not rubber-band the ankle
