---
name: loot-roll
description: Use when enemy, chest, quest, world, or encounter rewards come from deterministic or random drop tables and rolls are duplicated, opaque, unreplayable, or disconnected from pity and item ownership.
---

# Loot Roll

This skill owns **drop-table identity, roll inputs and reward selection**. `rng-seed` owns deterministic random streams, `pity-table` owns bad-luck counters/floors, and item/currency owners commit the selected reward.

## Modes

| Mode | Selection |
|---|---|
| guaranteed-kit | authored guaranteed entries |
| chance-affix | random/weighted entries or modifiers |
| shared-pool | multiple sources reference a shared versioned pool |
| none | source grants no rolled loot |

## Roll contract

Every table/pool has a stable ID and version. A roll records source/reward event ID, pool version, eligible entries, relevant context and the `rng-seed` stream/state or deterministic draw reference required for replay.

Do not infer pity from repeated misses; if protection exists, call `pity-table` with a stable pool/counter identity. A selected reward is committed once through `inventory-economy`, `currency-dual`, `equipment-progression`, or another true owner using the source event/transaction ID.

Wear replacement, encounter spend coverage, rarity cadence and sample sizes are balancing policy, not universal drop-table laws. Validate statistical claims using enough observations for the stated claim and preserve deterministic replay for individual rolls.

## Acceptance

Replay a captured roll from its stable table/version plus RNG state and obtain the same selected entries. Test duplicate reward callbacks, empty/ineligible pools, table migration and pity integration. Report actual sample size/distribution when making balance claims; do not use an arbitrary kill count as proof that players understand the table.
