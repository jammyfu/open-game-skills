---
name: boss-design
description: Use when a boss or major encounter needs a clear exam, phase/state structure, authored risk/readability policy and recoverable transitions without copying a shipped encounter or forcing universal phase rules.
---

# Boss design

Ask the project role first: duel, puzzle-gate, hunt, raid, spectacle, hybrid, or existing.

## Contract

Publish:
- stable `boss_encounter_id` and revision
- exam/goal statement
- phase or state graph with stable state IDs
- entry/exit/fail/retry policy
- authored risk/readability policy
- arena dependencies and required taught verbs
- resource/reset rules owned by their respective systems

## Ownership

Boss design owns encounter composition and state transitions. `attack-tell` owns warning contracts, `enemy-kit-balance` owns move-kit tuning, `difficulty-design` owns difficulty policy, and camera/combat/resource skills retain their own truth.

## Rules

1. Telegraph/readability is authored from threat, pacing, player capability and accessibility needs; there is no universal damage-to-windup formula.
2. A phase may change space, goals, move combinations, resources, presentation or another authored dimension; it does not need to fit one template.
3. Required tools/verbs must have a recoverable availability path or an explicit fail/retry path.
4. Story placement, optionality and relative difficulty are project progression decisions, not boss invariants.
5. Phase transitions are idempotent and use stable transition identity so duplicate callbacks cannot advance twice.

## Acceptance

Given the same boss revision and starting state, a reviewer can identify the intended exam, legal state transitions, risk/readability policy, recovery path and which external skills own timing, targeting, resources and presentation.
