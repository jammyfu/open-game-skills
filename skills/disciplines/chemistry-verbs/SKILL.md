---
name: chemistry-verbs
description: Use when verbs, materials or environmental properties combine into systemic reactions and the project needs a versioned reaction table with deterministic ownership and replayable outcomes.
---

# Chemistry verbs

Ask the simulation model: authored-reactions, property-table, systemic-sim, hybrid, or existing.

## Contract

Publish:
- stable `reaction_table_id` and revision
- stable property/material/verb IDs
- stable `reaction_id` for each authored or resolved reaction
- predicates, priority/tie rules and resulting state changes
- source event identity and idempotency policy
- RNG stream reference for stochastic outcomes

## Ownership

This skill owns reaction resolution from declared properties. Rendering, damage, navigation, inventory, puzzle and weather systems own their own resulting state; chemistry emits versioned reaction events rather than mutating unrelated systems ad hoc.

## Rules

1. New verbs/properties are added when they serve the project; there is no required multiplication count or maximum table size.
2. Multiple matching reactions resolve by explicit priority/tie policy, never container/render order.
3. The same source event/reaction identity cannot apply its consequence twice.
4. Puzzle teaching/solution policy remains in `puzzle-design`; the reaction table stays valid outside a specific puzzle unless scoped otherwise.

## Acceptance

Given the same table revision, source state and deterministic inputs, the same `reaction_id` and canonical outcome events are produced. Presentation changes do not alter the reaction result.
