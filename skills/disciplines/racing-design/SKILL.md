---
name: racing-design
description: Use when a race, time trial, pack contest, item race, route challenge, catch-up policy, ranking rule, track decision grammar, or race win/loss contract needs to be designed independently from vehicle handling.
---

# Racing design

This skill **owns race structure**: objective, ranking/progress, lap/checkpoint validity, catch-up/item policy, track decisions and finish/reset rules. `racing-feel` owns vehicle and speed response.

## Modes

| Mode | Structural focus |
|---|---|
| time-trial | time/ghost/route validity and retry policy |
| rubber-band | explicit project-authored catch-up policy for competitors |
| kart-chaos | item/disruption race structure and eligibility tables |
| boost-rail | route/rail/shortcut/chain structure; handling stays in racing-feel |
| drift-weight | race/track structure intended for grip/weight-focused handling |

These are design directions, not claims about named commercial titles or universal tuning values.

## Contract

Publish applicable data such as:

```text
race id / rules revision
start/finish and checkpoint/lap validity
ranking/progress calculation + tie rule
respawn/recovery effect on progress
ghost/opponent collision policy
catch-up/item policy, if any, with observable eligibility
shortcut/off-track validity
finish, DNF, timeout and restart policy
```

Track decision density, shortcut risk, pack spacing and catch-up strength are project data. Do not require one readable decision every few seconds or assume a hidden speed boost is necessary for any mode.

## Ownership

- `racing-feel`: acceleration, braking, grip/slip, drift, boost response, collision response and speed readability.
- `rng-seed` / loot-like table owners: deterministic random streams when race items require them.
- `game-qa`: race regression/device evidence.
- `netcode-feel`: network prediction/correction when multiplayer applies.

## Accept

Given a recorded race state, the project can explain ranking/progress, legal route, catch-up/item eligibility and finish outcome without inspecting presentation effects. Different handling columns can use the same race structure without changing hidden rules.
