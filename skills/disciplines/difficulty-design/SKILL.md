---
name: difficulty-design
description: Use when a project needs explicit difficulty modes, scaling rules, challenge curves or assist policies with measurable outcomes instead of hidden HP-only inflation or genre-specific defaults.
---

# Difficulty design

Difficulty is a versioned project policy, not a fixed ordering of knobs.

## Contract

Publish:
- stable `difficulty_policy_id` and revision
- named mode/scaling policy
- affected systems and excluded systems
- measurement context: build, segment, player cohort or test mode
- challenge metrics and guardrails
- transition/switch rules, including whether mid-session changes are allowed
- evidence required to accept a tuning change

Possible levers include space, information, resources, enemy composition, timing windows, numbers, assists, checkpoints or other project-defined systems. Their order and use depend on the game.

## Ownership

This skill selects and evaluates the difficulty policy. It does not directly own combat clocks, hitboxes, economy ledgers, navigation, camera or save state.

## Rules

1. Scaling must be observable in project data or documentation; no silent rule changes that cannot be reproduced.
2. Static regions, level sync, rank-based scaling, adaptive systems and fixed challenge are all valid when explicitly chosen.
3. Readability comes from the owning tell/UI/accessibility contracts. High threat does not imply one universal tell length.
4. Compare changes in a declared measurement context; do not mix different builds, modes or player populations without labeling them.
5. A change that crosses another owner's contract reruns that owner's acceptance tests.

## Acceptance

A reviewer can name the active policy/revision, what can change, what must remain stable, the measurement context and the evidence needed to show the intended challenge changed without hidden collateral rule changes.
