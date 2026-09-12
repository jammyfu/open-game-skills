---
name: equipment-progression
description: Engine-neutral equipment economy. Pick one growth model per slot — replace, upgrade in place, affix-craft, or fuse. Use for loot, crafting, loadout caps, set bonuses.
---

# Equipment Progression

Ask which column each *slot* uses. Mixing columns on the same instance is the usual failure.

| Column | What the player keeps | What "upgrade" means |
|---|---|---|
| A Replace | Nothing; next drop is the upgrade | Find a better instance |
| B Tree | The same instance | Spend mats, pick a branch |
| C Affix | The same base | Reroll / add / masterwork stats |
| D Fuse | The same instance + a spent mat | Function changes; may add wear |
| E Eternal | A named unique | Cooldown or bond, not a town repair |

Legal split: weapons A + armor B. Illegal: one sword that both shatters *and* trees to endgame.

## Rules that do not belong to any franchise

1. Attack lives on the item. Defense lives on the body. Buff food is a third, timed layer.
2. Set bonuses open at mid-tier or full set, never at +0.
3. Slot caps are difficulty. Expanding a page is a reward, not a vendor dump on minute one.
4. An upgrade recipe must name the missing mat *and* the region class it comes from. That is map gravity.
5. Failed upgrades are readable. Do not swallow materials into a silent RNG without a tell.

## Data

```
Item { id, slot, column: A|B|C|D|E, tier,
       attack?, defense?, set_id?,
       wear?, upgrade[]{ mats[], unlocks? } }
```

## Accept

The starter item in a Replace slot cannot finish the game unless it is tagged Eternal. The player can look at a mountain and know why they would go there for a mat. Inventory is tight enough that discard is a real choice.
