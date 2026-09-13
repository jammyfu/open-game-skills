---
name: first-session-value
description: Use when the first playable session must demonstrate real product value before or around an offer, signup or wall, while keeping onboarding evidence distinct from monetization policy.
---

# First session value

This skill decides when the player experiences the promised value. `game-monetization` owns offer/paywall design.

## Contract

Publish:
- stable `session_variant_id` and revision
- audience/cohort and entry source
- promised core challenge or decision
- minimum playable/demo outcome
- optional question/setup steps and why each changes the experience
- handoff point to `game-monetization` or another product flow
- evidence and untested remainder

## Rules

1. Promise only capabilities available in the tested build or label preview/mock content explicitly.
2. The first value beat may be combat, puzzle, creation, simulation, narrative, rhythm, racing or another project loop; do not force a fight or reward.
3. Questions belong before the value beat only when their answers materially alter the experience, content or offer.
4. An offer, signup or wall is separate policy. Its presence does not prove or invalidate the gameplay slice by itself.
5. Returning/new-player state uses stable identity and must not depend on a debug slot or mutable display text.

## Acceptance

A reviewer can identify the `session_variant_id`, what value was promised, the core challenge or decision actually experienced, which setup steps mattered, where monetization/product flow begins, and what evidence supports the first-session claim.
