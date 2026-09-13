---
name: equipment-progression
description: Use when weapons, armor, tools, loadouts, upgrades, affixes, fusion, set effects, or replacement gear need a clear ownership and progression model without mixing incompatible item identities.
---

# Equipment Progression

This skill owns **equipment instance identity, slot compatibility and progression transforms**. `inventory-economy` owns storage, `crafting-loop` owns recipe transactions, and `durability-economy` owns wear.

## Modes

| Mode | Persistent identity | Progression |
|---|---|---|
| replace | instance is normally superseded by another | acquire another instance |
| tree | same instance | authored upgrade branch |
| affix | same base identity | add/reroll/masterwork attributes |
| fuse | output identity is authored from inputs | consume/combine instances |
| eternal | named/persistent identity | authored unlock/bond/cooldown progression |

A project may combine systems when identity and transition semantics are explicit. Do not declare a combination illegal merely because another genre usually avoids it.

## Stable item contract

Each equipable instance has a stable instance ID plus item definition ID, slot/type, progression mode/state and authored modifiers. Save/migration must not key an item by localized display name or transient list index.

Upgrade/fuse/reroll operations are transactions coordinated with `crafting-loop` and `inventory-economy`: inputs are validated, consumed once, output is created/updated once, and duplicate callbacks do not duplicate gear or lose materials.

Set bonuses, starter viability, tier pacing, slot caps and acquisition geography are project design choices. Publish them in data and validate them against the intended game instead of imposing universal tier or endgame laws.

## Acceptance

Replay acquire/equip/replace/upgrade/fuse/save/load paths including duplicate callbacks and a failed transaction. Stable item identities, consumed inputs and resulting slot state remain consistent. Test at least one project-specific progression edge case; rarity color or “bigger number” alone is not progression evidence.
