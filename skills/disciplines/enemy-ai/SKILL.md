---
name: enemy-ai
description: Use when an NPC needs explicit idle, alert, search, combat, retreat, or reset state transitions and those transitions are currently snapping, looping, or contradicting other AI systems.
---

# Enemy AI

This skill owns the **brain state machine and transition policy**. It does not own sensing geometry, target scoring, attack warnings, or move balance.

## Modes

| Mode | State emphasis |
|---|---|
| leash-guard | guard area, pursue within published leash, then recover |
| patrol-hunt | patrol → investigate/search → combat → recover |
| ambush | hidden/idle → authored reveal → combat |
| duelist | combat spacing and state commitment for one primary opponent |
| swarm | simple local states coordinated by `group-tactics` |

`enemy-perception` owns sight/hearing/last-known evidence. `aggro-table` owns AI threat scoring. `enemy-kit-balance` owns move data. `attack-tell` owns readable startup.

## Transition contract

Publish state IDs and the event/evidence that can enter or leave each state. A transition records its reason (`saw_target`, `lost_target`, `leash_exceeded`, `scripted_phase`, and so on) so debug output can explain why the brain changed state.

Use one logical decision clock. Rendering rate and animation interpolation do not create extra state transitions. When several transition conditions become true on the same tick, use an authored priority or stable rule instead of container iteration order.

Reset/recovery behavior is project data: walk home, hold position, despawn, rejoin patrol, or remain engaged are all valid when explicitly chosen. Do not assume every game must visibly walk an NPC home.

## Acceptance

Replay the same perception/target event trace at different render rates and reversed entity iteration order. Brain states and transition reasons must match. Break and reacquire perception around the configured boundary, exceed the leash if one exists, and interrupt a scripted phase. Debug output must name the current state and the reason for the latest transition; animation alone is not evidence.
