---
name: racing-feel
description: Use when a vehicle, hovercraft, runner, kart, rail mover, or race actor needs authored acceleration, braking, steering, grip/slip, drift, boost, surface, collision, recovery, audio/camera speed feedback, or handling assists.
---

# Racing feel

This skill **owns vehicle and speed response**. [racing-design](../racing-design/SKILL.md) owns ranking, track validity, catch-up/item eligibility and race outcome.

## Modes

| Mode | Handling focus |
|---|---|
| drift-kart | authored drift/charge/release and accessible steering response |
| boost-rail | path/rail commitment plus authored boost response |
| grip-weight | slip/grip/brake/weight-transfer model selected by the project |
| combat-arena | vehicle handling while separate combat owners provide weapon rules |

A hybrid is valid when the project names which handling pieces are combined and which owner supplies each value.

## Simulation contract

Use the project's authoritative gameplay/physics clock discovered by the engine adapter; **do not impose a universal tick rate**. Publish where input sampling, handling integration, surface/boost modifiers, collision response and race-state consumption occur.

Handling data includes applicable acceleration/deceleration curves, speed limits, steering response, grip/slip, brake behavior, drift/boost state, surface response and recovery. Camera/audio/haptic effects communicate speed but do not fabricate logical velocity.

## Rules

1. Boost has an authored state/lifetime when used; it is not required to follow one universal startup/hold/falloff shape.
2. Drift/slip failure and recovery are project data; do not mandate a spin, scrape or specific burst mechanic.
3. Collision uses the project's gameplay collision proxy/physics contract, not render geometry by accident.
4. Assists are explicit project settings or handling variants. They do not silently change because of race position unless `racing-design` publishes that policy.
5. Catch-up, item pressure, ghost rules, ranking and respawn progress are consumed from `racing-design`, not re-authored here.
6. Speed readability may combine camera, audio, environment, UI and haptics according to accessibility/settings; no one channel is universally mandatory.

## Accept

Replay the same handling input/configuration under the supported simulation/render conditions and record logical speed/steer/boost/collision state. The player-facing cues reflect that state, while race rank/catch-up decisions remain attributable to `racing-design`.
