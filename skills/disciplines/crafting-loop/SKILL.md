---
name: crafting-loop
description: >
  Engine-neutral craft loop. Pick a column first. Use when recipes are a
  wiki, when stations hide the verb, or when craft skips the gather loop.
  Do not copy a franchise recipe book.
---

# Crafting loop

Ask the column.

| Column | Where it happens | What it costs |
|---|---|---|
| hand-craft | anywhere, short list | inventory + time |
| station-craft | bench / fire / anvil | station + recipe + mats |
| fuse-two | two items in, one out | identity of both |
| cook-buff | meal / potion with timer | mats + duration |
| schematic-unlock | recipe is the loot | find then craft |

Do not mix fuse-two identity destruction with schematic-unlock on the same bench unless both columns are named.

## Loop

```
see need → gather (world or vendor) → meet recipe → spend → hold result → use / wear
```

If the player cannot name the gather step, the craft is a shop with extra clicks.
Wear and slots live in durability-economy and equipment-progression. This skill only authors the *transform*.

## Recipe readability

- A recipe is a sentence: N of tag A + M of tag B → item C.
- Tags come from chemistry-verbs when possible. Do not invent a second material language.
- Unknown recipes fail loudly (missing 2 oil), they do not silently no-op.
- Discover-by-doing is a column (schematic-unlock or cook-buff experiment). Default is a readable list at the station.

## Time

Craft time is a clock the player can walk away from, or a 1-beat confirm.
Long crafts need a visible finish. No hidden overnight unless time-weather is stacked and published.

## Iron rules

- No recipe that only works on one named quest prop.
- Result must fit inventory-economy. Overflow is visible.
- Consume-wear items that come from craft must state their lifespan on the result card.
- Do not hide the only repair bench behind an unmarked mountain.

## Accept

The player can craft the first useful item without a wiki. A missing mat is named. Using the result is a different verb from crafting it.
