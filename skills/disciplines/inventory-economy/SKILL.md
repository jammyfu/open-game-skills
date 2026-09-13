---
name: inventory-economy
description: Use when carried items, stacks, unique slots, weight, pages, hotbars, pickup overflow, or discard behavior creates lost items, duplicate ownership, unclear capacity, or unusable inventory pressure.
---

# Inventory Economy

This skill owns **inventory identity, capacity, stacking, containment, overflow and transfer rules**. `equipment-progression` owns item growth; `durability-economy` owns wear; `currency-dual` owns wallets.

## Modes

| Mode | Capacity model |
|---|---|
| stack-tabs | categories plus stack limits |
| unique-slots | one instance per occupied slot |
| weight | capacity derived from authored weight rules |
| page-grid | page/cell capacity and placement |

Capacity pressure is project data. A game may use meaningful scarcity, generous storage, auto-stash, unlimited quest inventory, or no discard at all. Do not force every full bag to become a dramatic choice.

## Identity and transactions

Every item instance or stack has a stable ID/type identity and explicit quantity. Pickup, split, merge, move, equip, drop, discard and stash are transactions: either the source/destination state commits consistently or the operation fails without duplicating/losing items.

Publish stack-key rules, capacity calculation, reserved/quest-item policy and transfer ownership. Repeated pickup callbacks use a stable pickup/transaction ID when duplication is possible.

Overflow behavior is explicit: reject, leave in world, partial pickup, overflow queue, mail/stash, replace prompt, or another project-defined policy. Never silently delete the excess.

Hotbar/quick access is an input/UI policy layered on inventory. Its size and device mapping come from `input-design` and UI constraints, not a universal finger-count formula.

## Acceptance

Test pickup at exact capacity, one-over capacity, stack merge/split, duplicate callback, move/equip interruption, save/reload and project-specific overflow. Item totals and stable identities remain explainable before and after every transaction. A full bag screenshot is not inventory evidence.
