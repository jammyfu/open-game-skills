---
name: moving-platform
description: >
  Riders inherit platform velocity. Use when a character slides off a
  lift, or when a jump from a mover ignores its speed. Stacks on
  platform-jump and locomotion.
---

# Moving platform

Ask the column.

| Column | Rider keeps |
|---|---|
| stick-carry | full platform delta while grounded |
| loose-carry | partial; player can walk off |
| one-shot-lift | elevator, no walk |
| crush-safe | publish crush or no-crush |

## Clock

Move platforms on the logic tick before riders sample ground.
A jump from a mover adds the platform velocity to v0 unless the column is one-shot-lift.
Coyote still counts if the platform slides out from under the feet.

## Iron rules

- Do not parent the mesh only. Carry is velocity, not a visual attach that desyncs collision.
- Crush: either a published kill volume or the platform yields. Silent squash is a bug.
- Camera-anti-clip treats the mover as moving geometry.
- Enemies on movers use nav-mesh that updates or a leash on the platform id.

## Accept

Stand still on a lift and you arrive. Jump with the lift and you keep the extra speed. A closing door either kills with a tell or stops on the body.
