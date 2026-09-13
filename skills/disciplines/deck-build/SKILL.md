---
name: deck-build
description: Use when cards or card-like actions move through a deck/hand/discard/exhaust system and the project needs stable card identity, zone transactions, draw/shuffle rules and replayable RNG ownership.
---

# Deck build

Ask the deck model: fixed, constructed, draft, run-builder, rotating-pool, hybrid, or existing.

## Contract

Publish:
- stable `deck_ruleset_id` and revision
- stable `card_id` plus card-definition revision
- legal deck constraints
- canonical zone IDs and move rules
- draw/shuffle/mulligan policy
- cost/resource owner references
- `rng-seed` stream reference for stochastic ordering
- persistence/reset behavior

## Ownership

This skill owns deck composition rules and card movement between canonical zones. Card effects route to their gameplay owners; resources route to their own meter/economy skill; RNG algorithm/state stays in `rng-seed`.

## Rules

1. Each zone transition has transaction/request identity so duplicate callbacks cannot draw, discard or exhaust the same card twice.
2. Shuffle/draw order is reproducible from declared stream state when determinism is required.
3. Starter viability, encounter order and required content are project policies, not deck-system invariants.
4. Card display order/animation is not canonical zone order unless explicitly authored.
5. Ruleset changes increment revision and define migration for persisted decks/runs.

## Acceptance

Given the same ruleset revision, canonical zones and RNG stream state, the same draw/shuffle/move results occur. A reviewer can distinguish deck ownership from card effects, resource costs and presentation.
