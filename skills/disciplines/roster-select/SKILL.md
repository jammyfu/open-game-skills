---
name: roster-select
description: Use when one or more players choose characters/loadouts from a roster and the project needs stable selection identity, availability predicates, ready/commit behavior and presentation-independent state.
---

# Roster select

Ask the selection model: single-pick, multi-pick, draft, random, blind, unlock-grid, custom, or existing.

## Contract

Publish:
- stable `roster_id` and roster revision
- stable character/loadout IDs
- stable `selection_id` per participant/request
- availability/eligibility predicate
- selection/change/cancel/random policy
- explicit `ready/commit` boundary
- tie/conflict policy when exclusivity exists

## Ownership

This skill owns selection state and commit lifecycle. Character gameplay data, unlock/progression state, cosmetics and input bindings remain with their owners.

## Rules

1. Selection/ready callbacks are idempotent by `selection_id` and request identity.
2. Blind, random, duplicate picks, bans and exclusivity are project modes; none are tied to one genre.
3. UI highlight, portrait order or color does not become canonical selection truth.
4. Roster revision changes define compatibility/migration for saved presets or pending selections.
5. A committed selection is immutable for that start request unless an explicit unready/reopen transition occurs.

## Acceptance

Given the same roster revision, eligibility state and selection requests, the same committed roster result occurs. Duplicate ready callbacks do not start twice, and presentation changes do not alter selected IDs.
