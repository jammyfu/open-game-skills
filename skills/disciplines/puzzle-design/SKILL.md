---
name: puzzle-design
description: Use when a puzzle needs explicit legal verbs, properties, solution policy, reset behavior and evidence without assuming one room, one answer or one teaching sequence.
---

# Puzzle design

Ask the intended structure: authored-one, multi-solution, systemic-toy, sequence, hybrid, or existing.

## Contract

Publish:
- stable `puzzle_id` and revision
- legal verb/property set and their owners
- legal solution policy
- state variables and stable state IDs where needed
- fail/reset/leave policy
- hint policy and accessibility alternatives
- evidence for intended and allowed alternate solutions

## Rules

1. A puzzle may teach, test, combine or remix properties; the number of rooms or new combinations is project-authored.
2. An allowed improvised solution remains valid when it satisfies the published property/state rules.
3. Failure/reset behavior must avoid unrecoverable state unless that is an explicit project rule.
4. Hinting may range from none to explicit solution guidance; evaluate it against the project's learning/accessibility goal rather than declaring every direct hint a design failure.
5. Chemistry, physics, inventory, gates and narrative state stay owned by their respective skills.

## Acceptance

Given a `puzzle_id`, revision and start state, a reviewer can identify legal verbs/properties, accepted solution policy, reset path, hint policy and which outcomes are valid. Different presentation or room layout does not silently change the puzzle's rules.
