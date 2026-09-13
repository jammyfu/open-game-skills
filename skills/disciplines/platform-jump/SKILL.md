---
name: platform-jump
description: Use when a platformer's jump arc, rise/fall gravity, takeoff speed, air control, jump cut, or reachable-gap metrics need outcome-based tuning.
---

# Platform jump

This skill owns the **jump arc and reachability metrics**. `jump-leniency` owns coyote time, input buffering and corner forgiveness; `locomotion` owns movement integration and grounding.

Choose the movement/jump feel:

| Column | Ground feel | Air policy |
|---|---|---|
| snap-run | fast acceleration | authored air control |
| weight-run | longer accel/brake | authored air control |
| inertia-air | preserves more horizontal momentum | optional air verbs |
| gravity-flip | local up vector | same ownership rules in local frame |

Tune by outcomes such as body-height jump, time-to-apex and horizontal reach rather than copying raw constants from another game.

For a simple constant-gravity arc using positive magnitudes:

```text
gravity_up = 2 * height / apex_time^2
launch_speed = 2 * height / apex_time
```

A separate fall multiplier or curve may be authored. These equations are a starting model, not a requirement for every jump system.

## Rules

- Variable-height jump cut belongs to the arc policy; its input edge comes through `input-design`/movement state.
- Coyote/buffer configuration is referenced from `jump-leniency`, not duplicated here.
- Dash, wall-jump and double-jump are separate named verbs/capabilities; they do not silently rewrite the base arc.
- Critical level geometry should be validated against the intended no-forgiveness baseline unless the design explicitly requires a forgiveness mechanic as a taught capability.

## Accept

Measure height, apex time, horizontal reach and short-hop outcome from logical state. Verify representative gaps under the intended movement column, with forgiveness disabled and enabled separately. Changing render FPS does not change the arc; changing leniency does not secretly change gravity or takeoff speed.
