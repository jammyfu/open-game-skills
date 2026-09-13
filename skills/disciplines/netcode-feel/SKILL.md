---
name: netcode-feel
description: Use when online play needs an explicit authority, input-delay, prediction, rollback, correction, or confirmation contract without coupling network latency to the render clock.
---

# Netcode feel

Choose the networking model before tuning feel:

| Mode | Authority / wait model |
|---|---|
| delay-based | inputs wait a published number of logical ticks |
| rollback | predict remote input, snapshot, rewind and resimulate |
| lockstep | peers advance only when required inputs for a tick are available |
| server-auth | server state is authoritative; clients predict/interpolate where allowed |

## Deterministic state boundary

Networking owns transport/authority; gameplay systems still own their state. A rollback snapshot must include every gameplay value needed to reproduce future simulation: transforms/velocities, action state and timers, health/resources, spawned logical entities, RNG stream state/counters (`rng-seed`), and any other deterministic state read by later ticks.

Presentation-only camera shake, particles and audio need stable event IDs or predicted/confirmed lifecycle rules so resimulation does not duplicate them.

## Predicted versus confirmed

A client may present a **predicted** hit or state before authority/remote input is confirmed. Rollback is allowed to invalidate a prediction the player already saw. The correction policy therefore distinguishes predicted from confirmed events instead of pretending visible predictions can never be revoked.

Publish which effects may play speculatively, which wait for confirmation, and how canceled predictions are reconciled. Confirmed durable outcomes must not be applied twice during resimulation.

## Timing

Input delay, simulation tick, render interpolation and network transport are separate quantities. Do not slow the simulation clock to hide network latency. Hitstop affects only the gameplay clocks named by its owner; transport/network time keeps progressing.

For rollback, snapshot before the earliest rewound tick, restore that state, inject corrected inputs and resimulate through the current tick. Reversing entity iteration or replaying the same packet/input trace must not change deterministic gameplay results.

## Acceptance

Replay a captured input/packet trace with artificial latency, jitter, reordering and packet loss appropriate to the selected model. For rollback, compare deterministic state hashes after rewind/resimulation, RNG state, predicted/confirmed event transitions and duplicate-effect suppression. Record maximum rollback/correction distance and user-visible correction separately from transport delay. Unrun network/device tests stay `not-run`.
