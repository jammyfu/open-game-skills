---
name: platform-jump
description: >
  Coyote, jump buffer, variable height, corner slip. Use when a jump feels
  floaty, late, or unfair. Stacks on locomotion and action-feel
  coyote-platformer. Do not copy a franchise stage.
---

# Platform jump

Ask the column.

| Column | Accel | Forgiveness |
|---|---|---|
| snap-run | almost instant | coyote + buffer |
| weight-run | long accel / stop | coyote only |
| inertia-air | keep air momentum | dash edges extra |
| gravity-flip | local up vector | same timers |

Tune by **outcome**: height in body-heights, time-to-apex in seconds. Not by a raw gravity you copied.

## Feel knobs (starting points, not law)

| Knob | Typical start |
|---|---|
| height | 2.5–4 body heights |
| time to apex | 0.28–0.40 s |
| fall gravity | 1.5–2.0× rise |
| coyote | 5–8 frames @ 60 |
| jump buffer | 6–10 frames |
| jump cut | release multiplies upward vel by ~0.4–0.5 |

```
gravity_up  = 2 * height / apex^2
v0          = 2 * height / apex
gravity_down = gravity_up * fall_mul
```

Levels must be beatable **without** coyote. Coyote is a late-press save, not a hidden extra tile.

## Clock

Coyote and buffer live on the same logic tick as action-feel. They are not render-time slop.
Corner correction is a small horizontal nudge when a jump clips a lip. It is not a magnet through a wall.

## Iron rules

- Variable height is cut-upward-velocity on release, not "release to jump".
- Buffer consumes on the first grounded frame, then clears.
- Spikes / pits that require coyote as the only legal jump are a level-design bug.
- Dash / wall-jump are named extra verbs. They do not silently rewrite jump height.

## Accept

A player who presses one frame late still jumps. A player who taps gets a short hop. A spectator can tell intended jumps from coyote saves in training-mode.
