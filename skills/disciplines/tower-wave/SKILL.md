---
name: tower-wave
description: Use when a tower/defense-style mode needs lane or wave schedule identity, deterministic progression and clear ownership between mode goals, spawning, paths and participant kits.
---

# Tower wave

Ask the schedule style: lane-path, budget-wave, endless-ramp, authored-sequence, hybrid, or existing.

## Contract

Publish:
- stable `wave_schedule_id` and `schedule_revision`
- ordered wave/phase IDs or generation policy
- lane/path references and path revision
- start, advance, completion and reset conditions
- allowed scaling profile
- RNG stream reference if schedule generation is stochastic
- evidence for the tested schedule revision

## Ownership

`tower-wave` owns mode-level wave progression and lane objectives. `spawn-wave` owns individual dynamic entry scheduling and spawn visibility policy. Navigation/path owners define legal movement paths; participant kits and perception remain in their own skills.

## Rules

1. Wave structure may use counts, budgets, timers, objectives, triggers or other authored conditions; no single count/interval shape is universal.
2. The same schedule revision plus deterministic inputs resolves the same phase/wave identities.
3. Path/lane revision changes are explicit and cannot silently reinterpret a saved or replayed schedule.
4. Scaling changes use a versioned profile rather than mutating another system's timing/controls.
5. Retry/reset is idempotent and cannot duplicate already committed schedule transitions.

## Acceptance

A reviewer can identify the `wave_schedule_id`, revision, current phase/wave, lane/path revision, spawn owner and completion rule. Replaying deterministic inputs reproduces the same schedule decisions without requiring the presentation layer to be the oracle.
