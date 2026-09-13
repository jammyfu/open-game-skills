---
name: survival-needs
description: Use when hunger, thirst, fatigue, temperature, shelter or similar needs affect play and the project needs explicit meters, timebase, thresholds and delegated consequences.
---

# Survival needs

Ask which needs exist and whether they are cosmetic, advisory, gating, attritional, fail-state, hybrid, or existing.

## Contract

Publish:
- stable `needs_policy_id` and revision
- meter/state IDs and ranges
- declared timebase and pause/suspend policy
- threshold/effect policy for each state
- source/sink transaction identity where resources are consumed
- persistence behavior and UI/accessibility signals

## Ownership

This skill owns need-state progression and threshold events. `rest-site`, inventory/economy, health/damage, weather and durability remain separate owners and consume those events through explicit mappings.

## Rules

1. Depletion consequences are project data: warning, debuff, gating, resource conversion, fail state or no consequence are all valid when declared.
2. Need progression does not silently use render time or a different combat clock.
3. Pause, hitstop, sleep, fast-forward and suspend behavior are explicit per policy.
4. Duplicate consumption/tick events with the same identity do not double-apply.
5. UI meter presentation is not the canonical meter value.

## Acceptance

A reviewer can identify the needs policy/revision, timebase, threshold/effect mapping, persistence and source transactions. Replaying the same canonical ticks/events produces the same need-state transitions independent of HUD rendering.
