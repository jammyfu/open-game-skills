---
name: fighting-design
description: Versus grammar on a shared clock. Footsies, air-dash, tag-assist, platform-fighter. Stacks on action-feel. Ask the column first. Do not start from a named character movelist.
---

# Fighting design

Ask the column:

| Column | Space | Combo owner |
|---|---|---|
| grounded-footsies | 2D plane, walk-in | links + special cancel |
| air-dash | air mobility is a resource | juggle routes |
| tag-assist | two bodies, one meter | tag extend |
| platform-fighter | platforms + blast line | knockback growth, not long links |

Street Fighter fills grounded-footsies. Air-dash is a column, not a franchise. Smash-likes fill platform-fighter.

## Rules

1. One shared logic clock. Hitstop freezes the two colliding ActorClocks only. See action-feel.
2. Motion parse is stepwise windows, not one fat pocket.
3. Neutral must exist. If every button is a combo starter that skips space control, the column is broken.
4. A throw / grab answers shield or block. A projectile answers walk-in. Publish the triangle.
5. Meter that skips neutral needs a visible cost and a punish window after.
6. Netcode: prefer delay + rollback over lockstep. Input delay is part of feel; hide it in buffer, do not add a second clock.
7. Character identity is a moveset shape (long poke, fast walk, meter monster), not a lore paragraph.

## Stages

Keep collision stable. Hazards are a column (off / rare / constant). Platform-fighter blast lines are the health bar; grounded columns should not use blast lines as the win.

## Accept

- A new player can block, walk, and poke in the first minute
- A 2-hit confirm is possible on the chosen combo column without a 20-hit route
- Mirror match does not require a patch to be playable
