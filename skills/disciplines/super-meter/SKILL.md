---
name: super-meter
description: Use when EX, super, burst, ultimate or similar combat resource gain/spend needs stable resource transactions, eligibility, rollback/interruption behavior and presentation without becoming a second combat clock.
---

# Super meter

## Compatible modes

`cancel-spend` | `invuln-reversal` | `cinematic-super`

These describe common use cases; meter may also be spent outside `combo-design` when the owning action/state explicitly allows it.

## Resource contract

Publish resource ID/cap, gain sources, spend costs, reserve/commit/refund boundary, eligibility, reset/carry rules and stable **transaction** IDs. Gain/spend are **resource** state changes; action timing remains with the action owner.

## Rules

1. `combo-design` may reference meter requirements/spends on graph edges, but it is not the only consumer or owner of meter state.
2. Reversal/invulnerability behavior belongs to the relevant defense/action contract and references meter cost; meter itself does not grant invulnerability.
3. Presentation/cinematic/camera/audio may consume a committed super event but do not alter meter or combat clocks.
4. Duplicate/resimulated callbacks apply one logical gain/spend once according to transaction identity and network/replay policy.
5. Empty/insufficient behavior and meter persistence between rounds/lives are explicit project rules.

## Accept

Ledger traces reconcile gains/spends across normal use, cancel before commit, duplicate callback, rollback/retry and insufficient resource. Action legality and defensive windows remain attributable to their true owners.
