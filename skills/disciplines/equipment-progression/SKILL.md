---
name: equipment-progression
description: Pick one equipment economy — horizontal consumable weapons, vertical armor/weapon trees, or affix crafting — and implement slots, tiers, and upgrade costs. Use for loot, Great Fairy stars, Fuse, Diablo affixes.
---

# Equipment Progression

Ask first. Do not mix economies on the same slot.

| Column | What grows | What dies |
|---|---|---|
| A Horizontal (BotW weapons) | Next drop from the world | This instance. No repair |
| B Vertical tree (MH / Souls weapons) | Same weapon, ores + parts | Nothing; you commit to a branch |
| C Affix craft (Diablo) | Rerolls on one base | Time and currency |
| D Fuse (TotK) | Function + a durability bump on a consumable | The fused material |

BotW uses **A for weapons** and **B for armor** (Great Fairies, 4 stars). That split is the point.

## Rules

1. Do not let a weapon both shatter and upgrade to endgame on the same instance, unless shatter only happens to junk branches.
2. Armor upgrades spend *world* materials (dragon parts, star fragments). The recipe is map gravity.
3. Set bonuses unlock at +2 or full set, never at +0/+1.
4. Slot caps are difficulty. Expanding the weapon page is an exploration reward (Korok-like), not a shop dump.
5. Attack lives on the item. Defense lives on the body. Cooking/elixirs are temporary layers.

## Data

```
Item { id, slot: weapon|bow|shield|armor, tier, attack, defense,
       set_id, durability_hits?, upgrade[4]{ mats[] } }
```

Failed upgrade must name the missing mats and the region class they come from.

## Accept

Starter weapon cannot carry the finale unless it is a named exception (Master Sword). Player can point at a mountain and know which upgrade mat lives there.
