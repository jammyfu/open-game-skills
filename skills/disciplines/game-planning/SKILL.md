---
name: game-planning
description: Use when defining a game's smallest playable slice, limiting feature scope or deciding whether a proposed loop has a meaningful player outcome.
---

# Game planning

Record existing genre, target device, input roles and selected modes before expansion. Keep the slice small enough to validate; do not add combat, locomotion, loot or progression merely to satisfy an action-game template.

## Slice contract

Publish:
- stable `slice_id` and `slice_revision`
- pillars and explicit scope exclusions
- target/device/input context
- core challenge or decision
- start and end conditions
- failure/retry or explicit no-failure policy
- dependent skill modes/versions
- acceptance evidence and untested remainder
- next milestone and exit criteria

The player understands the goal, completes one **core challenge or decision**, perceives its consequence, and knows what to do next. Combat is one possible loop; noncombat games are equally valid.

| Loop | Core challenge | Observable consequence |
|---|---|---|
| combat | win or survive an encounter | outcome and next opportunity |
| puzzle | solve with taught properties | changed room or new possibility |
| building/simulation | build or allocate a limited resource | visible system response |
| narrative | make an informed choice | acknowledged consequence or branch |
| rhythm/racing | finish a passage or lap | timing/line feedback and retry |

## Rules

1. Revisions change when scope, goal, acceptance or dependent modes materially change.
2. Evidence must name the exact slice/build/revision; a demo clip or debug setup cannot silently stand in for a natural clear.
3. Stabilize only the systems used by this slice before expanding content volume.
4. Preserve project facts and prior choices; ask only for consequential missing decisions.

## Acceptance

`gameplay-validation` can run the natural start-to-outcome chain against the published `slice_id`/revision and return pass/fail/blocked/not-run with evidence. Expansion follows demonstrated slice goals, not a genre checklist.
