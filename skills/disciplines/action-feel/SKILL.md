---
name: action-feel
description: >
  Engine-neutral combat clock: per-actor hitstop, stepwise input parse,
  directed cancel graph, commitment. Pick a column first. Use when attacks
  feel floaty, cancels fire illegally, or hitstop freezes the whole world.
---

# Action feel

Ask the column before writing code. Studio names are examples, not rules.

| Column | Buffer | Cancel | Hitstop | Turn |
|---|---|---|---|---|
| short-special | 3-5f attacks | on-hit into specials only | 8/12/16 | snap on startup |
| long-cancel | 8-12f | on-hit + jump/gun style | rhythm, not weight | optional inertia carry |
| commit-whitelist | short, anti-misinput | named follow-ups only | 12-20 = weight | turn-lag during active |
| coyote-platformer | jump buffer + coyote | attack does not cancel jump unless data says so | tiny or none | air control % |

Do not mix short-special cancels with commit-whitelist great-swings.

## Six primitives (engine adapters implement these)

```
poll_input()
now_logical_frame()          # default 60 Hz, not render fps
play_pose(actor, move, frame)
query_hits()
apply_knockback(actor, vec)  # frame AFTER hitstop hits 0
juice_hook(event)            # flash/shake live elsewhere
```

## Clock

Each actor has `clock`, `hitstop`, `move`, `pending_cancel`.

```
each logical frame:
  sample into InputRing
  if hitstop > 0:
      hitstop -= 1
      try_match_cancels()    # matching stays legal while frozen
      do not advance pose
  else:
      advance move / loco
      resolve hits
      consume pending if legal
```

Hitstop freezes **the two colliding clocks only**. World, other actors, and input keep running. No global timeScale.

## Charge (when a move has it)

Publish the whole chain: start → full → hold-cost → release → cancel.
Hitstun, weapon-swap, and lost focus must restore a *legal* state (idle or published recover), not a stuck charge. Pose, hit box, and SFX share the same logical frame.

## Iron rules

- Press → move frame 0 ≤ 2 logical frames.
- Cancels are a directed graph + window, never "attacks can cancel attacks".
- Walk/camera look do not enter the special-move buffer unless the column says so.
- Weight = commitment + hitstop + camera kick. Slowing the clip is not weight.
- Motion inputs are stepwise windows, not one 15-frame bag.

## Accept

A vs B frozen, C still walks. Illegal cancel never starts. Commit column cannot 180° during active frames. After hitstun or alt-tab, the next tap starts a real move.
