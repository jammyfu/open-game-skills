---
name: death-carry
description: Use when a death/defeat transition must define what state is kept, transformed, dropped or reset and where recovery resumes without conflating presentation, checkpointing or run rules.
---

# Death carry

Ask the policy: keep-all, partial-carry, recoverable-drop, run-reset, custom, or existing.

## Contract

Publish:
- stable `death_policy_id` and revision
- stable `death_event_id`
- carry/reset/drop manifest by stable state ID
- respawn/checkpoint source
- `drop/recovery record` identity when recovery exists
- commit boundary and retry behavior

## Ownership

`death-carry` owns state transformation caused by the death event. `save-checkpoint` selects recovery anchors, `roguelike-run` owns run lifecycle, inventory/economy owns item/currency transactions, and presentation owns audio/VFX.

## Rules

1. Each `death_event_id` settles exactly once; retries/resume cannot duplicate drops, grants or resets.
2. Carry/reset policy is versioned project data, not tied to one genre.
3. Recovery records persist or expire according to explicit policy and never depend on display labels or render objects.
4. A death transition cannot mark unrelated quest/boss/run completion unless that owner emitted the corresponding event.
5. Save commit failures leave an inspectable pending/retry state rather than half-applying the carry manifest.

## Acceptance

Given one death event, policy revision and starting state, the same carry/reset/drop result is committed exactly once and the reviewer can identify the recovery anchor, recovery record and any pending persistence work.
