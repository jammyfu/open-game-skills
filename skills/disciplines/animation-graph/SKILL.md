---
name: animation-graph
description: >
  Who owns play_pose. Use when two clips fight, when root motion double-moves
  the body, or when hitstop freezes the render ticker. Stacks on action-feel.
  Does not replace play_pose.
---

# Animation graph

Ask the column.

| Column | Owner |
|---|---|
| loco-base | locomotion clip on track 0; root motion is displacement |
| overlay-attack | attack on track 1; root motion off unless the move row says on |
| hit-react | react clip may interrupt overlay; never starts a new attack |
| cinematic | cutscene owns pose until handoff |

One owner per actor per tick. A request without owner is ignored.

## Interrupt

```
request → owner check → (hitstop scales THIS skeleton only) → play_pose
```

Cancel windows live in action-feel. The graph does not invent a second clock.
Hitstop sets that skeleton `timeScale` to 0. Never freeze the world ticker (see pause-timescale if present).

## Iron rules

- Root motion and locomotion velocity do not both move the capsule on the same tick.
- Overlay cannot outlive the move row that spawned it.
- Death / knockdown: wakeup-oki owns the next request, not the last attack clip.
- 2D: spine-skeletal tracks 0/1/2 map to loco / overlay / face. Same owner rule.
- IK foot lock is presentation after the pose. It is not an owner.

## Accept

A debug line can name the owner and the clip. Two clips never write the same bone channel in one tick. Root motion off still lets the move complete on the logic clock.
