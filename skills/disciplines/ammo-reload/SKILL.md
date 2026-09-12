---
name: ammo-reload
description: Magazines, reserve, reload move. Ask infinite vs mag-and-reserve vs one-shot-chamber. Reload is a move on the action-feel graph. Interact and reload are different keys.
---

# Ammo and reload

Ask the column:

| Column | What empties |
|---|---|
| infinite | no count |
| mag-and-reserve | mag + pack |
| one-shot-chamber | each shot is a commit |

## Rules

1. Reload has start / active / cancel. Firing during reload only if the graph says so.
2. Empty mag does not eat the next interact. See input-design.
3. Reserve is inventory. A shop refill uses shop-price, not a silent debug grant.
4. ADS and hip share the same ammo pool unless the column splits them.
5. Juice muzzle flash is not a spent round. Count changes on the logic frame of the shot.

## Accept

Player can say how many shots remain without a wiki. Cancelled reload does not invent a full mag.
