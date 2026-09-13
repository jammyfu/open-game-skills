---
name: weapon-swap
description: Use when equipped weapon/tool identity can change during play and swap start/commit/cancel, sockets, action interruption, ammo/resources and presentation handoff need an explicit state contract.
---

# Weapon swap

## Compatible modes

`instant-holster` | `commit-swap` | `no-swap`

Timing values are project data; “instant-holster” is a behavior direction, not a universal frame count.

## Swap contract

Publish source **weapon ID**, target weapon ID, requested/committed equipped state, start/commit/end/cancel boundaries, legal action/cancel conditions, **interruption** behavior, socket/attachment requirement, ammo/resource ownership and fallback if the target asset/socket is unavailable.

## Rules

1. Whether swap is represented as a move/state/instant transaction is project/action data. `action-feel`/input state owners decide interaction with attacks/blocks/charges.
2. Held/charge/block state transfer or cancellation is explicit per action/weapon; do not assume all held state dies.
3. Gameplay hitboxes/projectiles use the committed weapon/action state and their own active windows, not the presentation moment a model becomes visible.
4. `model-pipeline`/`character-rig` owns **socket** compatibility. Missing required asset/socket follows declared fallback/error and cannot silently float.
5. HUD, animation and audio consume swap state/events and may present with latency/blending; they do not have to “swap on the same logic frame” to be correct.
6. Duplicate swap requests and interruption races settle deterministically to one equipped weapon/state.

## Accept

Test swap/cancel/interruption/focus loss/asset failure and duplicate requests from each allowed source state. Log committed weapon ID, state boundary and socket/resource outcome; no stuck action or double equip occurs.
