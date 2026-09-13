---
name: new-game-plus
description: Use when an eligible game state may start another cycle with project-defined carry, reset, scaling and entry conditions that must remain auditable across saves and revisions.
---

# New game plus

Ask the cycle policy: carry-most, selective-carry, flags-only, remix, custom, or existing.

## Contract

Publish:
- stable `cycle_id` and cycle revision
- explicit `entry predicate`
- versioned `carry_manifest` of kept/reset/transformed state IDs
- destination save/profile policy
- difficulty/content profile references
- migration/backward-compatibility behavior
- evidence required to start the cycle

## Ownership

This skill owns cycle transition and carry mapping. `save-systems`/`save-integrity` own persistence safety, `difficulty-design` owns difficulty policy, and individual progression/economy systems own their canonical state.

## Rules

1. Eligibility is an authored project-state predicate; no single completion gate is universal.
2. Cycle creation is an idempotent transaction keyed by request/cycle identity.
3. Carry/reset uses stable state IDs and schema revisions, never UI order or translated labels.
4. Temporary test state is carried only when the selected policy explicitly includes it.
5. A changed carry manifest or ruleset increments revision and must not silently reinterpret an existing cycle.

## Acceptance

A reviewer can identify the `cycle_id`, revision, entry predicate, carry manifest and destination profile. Replaying the same committed transition cannot duplicate or silently drop carried state.
