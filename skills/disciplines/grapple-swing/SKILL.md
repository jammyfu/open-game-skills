---
name: grapple-swing
description: Use when an actor attaches to a point or body for pulling, swinging or traversal and the project needs stable latch identity, motion ownership, release semantics and collision-safe recovery.
---

# Grapple and swing

Ask the mode: latch-pull, pendulum, tow-object, tether, no-grapple, or existing.

## Contract

Publish:
- stable `grapple_session_id` and revision
- stable `latch_id` / target identity
- latch eligibility predicate and query owner
- explicit `motion owner` during attached states
- rope/constraint parameters owned by physics/project data
- `release request` identity and release velocity policy
- collision/fall/recovery behavior

## Ownership

This skill owns grapple state transitions and attachment intent. Aim/target query, physics constraints, character locomotion, camera collision and fall rules stay with their owners.

## Rules

1. Latch selection is deterministic for a declared candidate revision and cannot depend on render order.
2. While attached, exactly one system owns actor transform/velocity authority; character movement and rigid-body constraints do not fight each other.
3. Duplicate latch/release callbacks are idempotent by session/request identity.
4. Tagged-only, free-surface, assisted or authored targets are project modes, not universal defaults.
5. Release may land on navigation, dynamic geometry, water or another valid project surface; if not, the owning fall/recovery policy applies.

## Acceptance

Given the same `grapple_session_id`, latch candidate state and release request, the same target and state transitions occur. A reviewer can identify motion authority, release velocity source and which external owner resolves collision/recovery.
