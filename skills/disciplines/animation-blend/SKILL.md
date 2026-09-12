---
name: animation-blend
description: Pose layers on top of the logic clock. Locomotion, aim, overlay attack. Inertialization on cuts. Foot lock is separate. A blend must not invent extra hit frames.
---

# Animation blend

Ask the column:

| Column | Who owns displacement |
|---|---|
| procedural-loco | code velocity |
| root-motion | clip |
| hybrid | clip on commit, code on walk |

## Rules

1. Logic step advances the move. Blend space only paints the pose.
2. Attack overlays must not extend active frames.
3. Cuts use inertialization or a 2-6 frame fade.
4. Foot slide after a blend → ik-foot-locking.
5. Aim offsets live on spine/arms, not root yaw unless fps-look.

## Accept

- Turning off meshes still matches query_hits to the move frame
- A walk-to-attack cut does not slide a planted foot after lock
