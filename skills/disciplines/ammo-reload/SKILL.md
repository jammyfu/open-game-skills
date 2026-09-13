---
name: ammo-reload
description: Use when weapons need magazine/chamber/reserve ammunition, shot consumption and reload transfer with atomic resource updates, interruption/cancel policy and semantic input actions.
---

# Ammo and reload

## Compatible modes

`infinite` | `mag-and-reserve` | `one-shot-chamber`

## Resource contract

Publish weapon/ammo resource IDs, magazine/chamber capacity, reserve ownership, fire consume boundary, reload transfer policy, cancel/interruption state and a stable **reload transaction** ID for each committed transfer.

## Rules

1. Fire/reload are semantic actions routed through `input-design`; do not require reload and interact to use universally different physical keys.
2. A shot consumes ammo once at the authoritative fire/shot-commit event. Muzzle flash/audio/animation never spends ammunition.
3. Reload magazine/reserve movement is **atomic** at the published commit boundary (or explicit staged transfers when the design uses them). Cancellation cannot invent or destroy rounds.
4. Repeated/resimulated reload callbacks use the same reload transaction identity and remain idempotent.
5. Firing/ADS/hip/cancel behavior during reload is project action-graph data; shared/split ammo pools are declared rather than assumed.
6. Inventory/shop/economy replenishment uses their own transaction owners and stable ammo resource ID.

## Accept

Reconcile magazine/chamber/reserve across fire, exact-empty, partial reload, cancel before/after commit, duplicate callback, weapon swap and insufficient reserve. Total ammo changes only through named consumption/grant transactions.
