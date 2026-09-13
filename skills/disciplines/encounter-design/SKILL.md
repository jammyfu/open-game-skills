---
name: encounter-design
description: Use when a room, arena, hunt, ambush or non-boss challenge needs an explicit state/beat graph, entry/exit rules, composition goals and evidence without forcing one universal encounter shape.
---

# Encounter design

Ask the intended role: traversal pressure, teaching, resource test, elite challenge, ambush, arena, hunt, hybrid, or existing.

## Contract

Publish:
- stable `encounter_id` and revision
- goal and completion condition
- state/beat graph with stable beat IDs
- participant/spawn references
- entry, fail, retry, reset and exit policy
- resource assumptions and rewards only if the project uses them
- evidence needed to prove the authored goal

## Ownership

Encounter design composes existing systems. `spawn-wave` owns dynamic spawn scheduling, `enemy-kit-balance` owns kits, `difficulty-design` owns scaling policy, and loot/economy systems own grants.

## Rules

1. An encounter may test one concept or several interacting concepts; composition is authored, not universally capped at one idea.
2. HP, count, geometry, information and resource pressure are valid only when tied to the stated goal and owner contracts.
3. Rewards are optional project data; do not require a drop to compensate a spend.
4. Reset/retry transitions are idempotent and do not duplicate participants or grants.
5. Record what was actually tested; a scripted setup does not prove a natural route into the encounter.

## Acceptance

Given the same `encounter_id`, revision and starting state, a reviewer can reproduce the legal beat transitions, identify completion/failure, and distinguish encounter composition from spawn, difficulty, combat and reward ownership.
