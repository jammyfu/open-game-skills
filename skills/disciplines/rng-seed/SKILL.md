---
name: rng-seed
description: Use when procedural generation, combat rolls, loot, replays, rollback, or deterministic tests require reproducible random streams that remain stable across refactors and resimulation.
---

# RNG seed

A seed is only one part of a reproducibility contract.

## Stream contract

Publish the RNG algorithm/version plus stable named streams for domains whose call order must not affect each other, for example `world`, `combat`, `loot`, `cosmetic`. Derive child stream seeds from stable semantic identifiers, not mutable container iteration order.

Each stream has serializable state or a counter/index that can be snapshotted. A replay or rollback snapshot restores the exact stream state/counter for the rewind tick; reseeding from a root seed and hoping the same number of calls occurred is not sufficient.

Random draws happen on the logical simulation path that owns the outcome. Render-only variation uses a separate presentation stream and must not mutate gameplay RNG.

## Replay identity

A reproducible replay records at least the game/simulation version, RNG algorithm/version, root/run identity, initial deterministic state/config, named stream derivation rules, logical tick/input trace, and any authoritative external events. If rules or algorithm change, treat old replays as a different compatibility version rather than silently producing new outcomes.

## Acceptance

Run the same recorded initial state + inputs twice and compare deterministic state hashes and every named RNG stream state at checkpoints. Insert an unrelated cosmetic random draw and verify combat/loot results do not change. Snapshot mid-run, restore, and reproduce subsequent draws exactly. Unrun engine/platform replays stay `not-run`.
