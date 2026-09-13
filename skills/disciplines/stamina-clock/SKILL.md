---
name: stamina-clock
description: Use when sprint, dodge, charge, climb or other actions consume/regenerate a stamina-like resource and need explicit transaction identity, timebase and interruption/recovery policy.
---

# Stamina clock

## Compatible modes

`none` | `shared-bar` | `per-verb`

## Resource contract

Publish resource ID, min/max, action cost policy, spend/commit boundary, regeneration/decay **timebase**, delay/conditions, interruption behavior and UI event source.

Every spend/refund/regen grant is a named **transaction** or deterministically derived event identity. Retry/re-simulation/duplicate callbacks are **idempotent** for the same logical transaction.

## Rules

1. Action owners request/reserve/commit/cancel stamina; this skill does not decide whether an attack/dodge/sprint is otherwise legal.
2. Insufficient-resource behavior is project/action data: deny start, partial/alternate action, debt, exhaustion or another declared result.
3. Regeneration timebase is explicit (gameplay tick/time, real time, state-driven event, etc.) and obeys pause/hitstop policies chosen by the project rather than an implicit clock.
4. Interruption/refund policy is explicit so an action cannot spend twice or refund after a committed irreversible boundary.
5. HUD/accessibility presentation consumes authoritative resource/change events and cannot create resource state.

## Accept

Replay start/cancel/commit, exact-cost, insufficient, duplicate callback and pause/interruption cases. Ledger/trace balances reconcile from stable transaction IDs and the declared timebase.
