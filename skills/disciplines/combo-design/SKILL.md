---
name: combo-design
description: Use when moves need authored links, cancels, strings, juggles, charge branches, route conditions or combo escape/termination policy on top of the combat timing contracts.
---

# Combo design

`combo-design` owns the **route graph**. `action-feel` owns logical move/cancel timing primitives; `hitstun-recover` owns actionable recovery; launch/body behavior stays with knockback owners.

## Compatible columns

`strict-link` | `cancel-chain` | `launcher-juggle` | `action-string` | `lock-on-brawler`

They are route styles, not universal balance formulas.

## Graph contract

Every edge publishes source/target move IDs, legal window/condition, resource/state requirements, hit/block/whiff/air/ground context and any consume/cooldown behavior. Charge states may be named nodes/edges when needed.

## Rules

1. Route validity follows the directed graph and underlying timing/state owners; animation length or presentation does not create connectivity.
2. Damage/scaling, juggle limits, gravity, proration, escape/burst and route length are project/balance data. Do not require universal damage falloff or a mandatory starter-confirm-ender pattern.
3. A route must expose its actual termination/escape/recovery conditions. Loops are judged against the project's intended rules rather than rejected solely because they repeat.
4. Misses, interruption, focus/device lifecycle and weapon/state changes re-enter a published legal state through their true owners; no phantom pending confirm survives invalidation.
5. Magnet/assist behavior, if used, is an explicit targeting/assist contract and cannot silently convert a miss into a hit.

## Accept

Given a move/state trace, the graph explains each legal/illegal edge, resource consume and eventual recovery/escape according to project rules. Editing one route edge does not require rewriting unrelated move timing owners.
