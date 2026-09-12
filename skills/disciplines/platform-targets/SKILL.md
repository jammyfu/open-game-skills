---
name: platform-targets
description: One game, several published budgets. Ask desktop vs home-console vs handheld-dock vs handheld-pc vs web-gpu vs mobile-thermals. Share the logic clock. Change presentation, not feel.
---

# Platform targets

Ask the column (one primary, list the others):

| Column | Constraint |
|---|---|
| desktop-scalable | sliders, unlocked or 60 |
| home-console | fixed SKU, 30 or 60 plus a mode |
| handheld-dock | two budgets, same build |
| handheld-pc | thermals, battery, TDP slider |
| web-gpu | download size, tab life |
| mobile-thermals | heat, touch |

Vendor SDK names live in engine adapters, not here.

## Rules

1. Same logic result from the same inputs on every SKU.
2. Input device is a column: pad, mouse, touch, gyro. Rebind keeps input-design grammar.
3. Handheld-dock publishes both budgets in the pause menu.
4. Weak SKU shortens view distance and shadows, not hitstop or race accel.
5. Dock swap or suspend must not lose the run. Saves are part of the target.
6. Safe area and text size are data per target.

## Accept

- A recorded input tape replays identically on two SKUs
- The player can read the published budget on the device they hold
- The vertical slice is completable with pad or the target's native input
