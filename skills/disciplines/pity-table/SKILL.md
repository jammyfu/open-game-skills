---
name: pity-table
description: Use when a randomized reward pool has a pity counter, bad-luck protection, guaranteed floor, reset/carry policy, or cross-pool migration that must remain deterministic and auditable across sessions.
---

# Pity Table

This skill owns **protection counter state and guaranteed-floor policy for a random reward pool**. `loot-roll` owns the actual table draw; `rng-seed` owns random-stream state; wallet/item owners commit rewards.

## Modes

| Mode | Protection |
|---|---|
| no-gacha | no pull-style protection state |
| pity-count | stable counter triggers an authored guaranteed outcome/eligibility rule |
| bad-luck-protect | probability/weight changes as authored state advances |
| none | raw table draw with no protection counter |

## Counter contract

Each protection state has a stable `pool_id`/counter ID, version, current value/state, trigger/reset/carry rules, and account/save scope. Do not identify pity solely by displayed banner name or transient UI position.

A qualifying roll and pity update form one transaction with `loot-roll`: the same reward event ID cannot increment/reset the counter twice. Define what happens when pools rotate, merge, split or migrate versions. Cross-pool carry/reset is project policy and must be explicit.

Guaranteed story/progression items, paid power policy and public rate disclosure are product/platform choices governed elsewhere. This skill does not impose one monetization model; it makes any selected protection behavior auditable.

## Acceptance

Test one-before/at/after trigger, duplicate reward callback, non-qualifying roll, reset/carry, pool rotation and save/reload. Counter state and selected reward transaction agree exactly once. Forced/debug outcomes remain labeled test evidence rather than natural statistical evidence.
