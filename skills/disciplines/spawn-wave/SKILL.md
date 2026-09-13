---
name: spawn-wave
description: Use when dynamic participants enter an encounter from authored points, budgets or director pressure and the project needs stable wave identity, scheduling, visibility policy and replayable stop conditions.
---

# Spawn wave

Ask the scheduling mode: placed-only, authored-pack, wave-budget, director-pressure, hybrid, or existing.

## Contract

Publish:
- stable `wave_id` and `wave_revision`
- spawn-point/source IDs
- participant pool/table revision
- cadence/budget/stop conditions
- `spawn_visibility_policy`
- deterministic ordering/tie rules where multiple points are legal
- replay seed/stream reference when randomness is used
- completion/reset semantics

## Ownership

This skill owns when and where a scheduled participant enters. Encounter goals stay in `encounter-design`; difficulty may choose an allowed budget profile; RNG state stays in `rng-seed`; participant behavior stays with its own systems.

## Rules

1. Visibility and proximity policy is project data: off-camera, gated, telegraphed, diegetic, visible arrival or another authored mode can all be valid.
2. A point rejected by occupancy/collision/streaming checks is skipped or retried deterministically; never fall through to an arbitrary list order.
3. Duplicate schedule callbacks for the same request/wave identity cannot create duplicate entries.
4. Budget/cadence changes produce a new revision and preserve enough evidence to reproduce the tested sequence.
5. Debug/scripted population changes are labeled as setup evidence, not natural encounter flow.

## Acceptance

Given the same `wave_id`, revision, start state and RNG stream, the same legal scheduling decisions occur. The project can change pacing or visibility policy without silently changing participant identity, completion rules or another system's timing contract.
