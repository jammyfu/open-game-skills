---
name: roguelike-run
description: Use when a run-based mode needs stable run identity, ruleset revision, seed/stream provenance, reset semantics and explicit meta carry without leaking temporary state between runs.
---

# Roguelike run

Ask the run model: reset-heavy, meta-progression, daily-seed, persistent-world-run, hybrid, or existing.

## Contract

Publish:
- stable `run_id` and `ruleset_revision`
- start snapshot/template revision
- seed plus owned `RNG stream` references
- explicit `meta carry policy`
- run-local versus persistent state IDs
- completion/reset/abandon predicates
- persistence/checkpoint integration

## Ownership

This skill owns run lifecycle boundaries and which state is run-local versus persistent. `rng-seed` owns RNG algorithm/stream state, `death-carry` owns death transformation, and save/progression systems own their canonical persistence.

## Rules

1. A run starts from the authored start template/persistent context; it does not have to be universally "clean."
2. Meta progression may affect future runs according to the published policy; mid-run changes require an explicit rule/revision rather than hidden mutation.
3. Daily/fixed/generated seeds publish enough stream provenance for replay.
4. Reset/abandon/completion transitions are idempotent and cannot grant or clear state twice.
5. A ruleset or start-template change increments revision so old replays/saves are not silently reinterpreted.

## Acceptance

A reviewer can identify `run_id`, ruleset revision, start template, RNG stream provenance, run-local state and meta carry policy. Replaying deterministic inputs does not inherit unrelated temporary state from another run.
