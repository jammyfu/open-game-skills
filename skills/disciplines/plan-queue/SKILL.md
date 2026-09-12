---
name: plan-queue
description: Pause to queue simultaneous actions, then play. Execution still matters. Not a turn-based clock.
---

# Plan queue

Ask: freeze-queue | soft-pause | none.

Freeze-queue stops the world clock (`pause-timescale` / hard-pause) so the player assigns one next verb per body. On confirm, all verbs start the same logic tick. Soft-pause slows but does not stop perception ticks.
A queue is not an auto-win. Cones still move after play (`enemy-perception`). Infinite pause with no execution skill is a column you must publish.
Do not add a second combat clock inside the queue UI.

Accept: two bodies open a door and take a guard on the same tick. A mistimed queue is a player error, not an invisible extra cone.
