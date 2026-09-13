---
name: enemy-fire
description: Use when an enemy ranged attack needs an authored fire-pattern profile, stable burst/shot identity, target snapshot and deterministic spread/suppression behavior without owning target selection or hit resolution.
---

# Enemy fire

Ask: `burst | suppress | accurate`.

## Ownership

`enemy-fire` owns fire-pattern scheduling. `target-priority` supplies the target decision, `attack-tell` supplies authored warning contracts when required, `projectile-hitscan` resolves shots, and `rng-seed` owns replayable random streams.

## Contract

Publish:
- stable `fire_pattern_id` + revision
- `fire_sequence_id`
- target ID / aim snapshot source
- ordered shot IDs or shot slots
- timing/recovery data from the project gameplay clock
- spread/suppression parameters and RNG stream ID when stochastic
- interruption/cancel conditions

Burst length, suppression accuracy, first-shot warning policy, crouch/cover modifiers and reload behavior are project data. Do not assume one universal pattern.

## Runtime rules

1. A shot slot commits at most once for one fire sequence.
2. Stale target snapshots follow the project's retain/reacquire/cancel policy; render order is not authority.
3. Random spread consumes the declared RNG stream so replay can reproduce shot directions.
4. Player invulnerability/filtering remains with its gameplay owner.
5. Presentation muzzle flash/tracer does not schedule or confirm the shot.

## Acceptance

Given the same pattern revision, target snapshot, gameplay-clock state and RNG stream state, the same ordered shot requests are produced. Interrupted/retried sequences cannot duplicate committed shot slots.
