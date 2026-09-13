---
name: set-piece-action
description: Use when an authored action sequence changes camera, control scope, movement constraints or staging and must hand control back deterministically without creating a second gameplay ruleset.
---

# Set-piece action

Ask the control model: full-control, constrained-control, rail, observation, hybrid, or existing.

## Contract

Publish:
- stable `set_piece_id` and revision
- entry/exit conditions
- control/handoff policy
- active gameplay owners during each state
- camera/presentation mode references
- retry/skip policy where applicable
- stable transition IDs and evidence

## Ownership

The set piece composes existing gameplay and presentation systems. It may narrow or transfer control according to project policy, but it does not redefine targeting, timing, traversal, collision or input semantics.

## Rules

1. Player input may be full, partial, contextual or absent for authored intervals; that is project data, not a universal requirement.
2. Control transitions consume fresh semantic input edges and do not replay held actions across handoff unless explicitly authored.
3. Presentation visibility does not define runtime legality; simulation behavior remains with its owning systems and the project's readability rules.
4. Duplicate transition callbacks are idempotent and cannot enter/exit the piece twice.
5. Skip/retry preserves legal game state and names any setup overrides used for testing.

## Acceptance

Given the same `set_piece_id`, revision and entry state, the same control owners and legal handoff transitions occur. A reviewer can tell when gameplay authority changes and whether the piece returned to the intended state without stale input or duplicated transitions.
