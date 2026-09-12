---
name: weapon-swap
description: Changing the held verb. Ask instant-holster vs commit-swap vs no-swap. Swap must restore a legal action-feel state. Sockets come from model-pipeline.
---

# Weapon swap

Ask the column:

| Column | During the swap |
|---|---|
| instant-holster | short holster frames |
| commit-swap | cannot attack until the new socket is live |
| no-swap | one weapon per slice |

## Rules

1. Swap is a move. It cancels only if the graph says so.
2. Charge and held block die on swap unless data keeps them.
3. The new weapon's boxes start on its first active frame, not when the key is pressed.
4. Missing socket is a pipeline fail, not a mid-air float.
5. HUD and audio swap on the same logic frame.

## Accept

Alt-tab or a swap never leaves a stuck charge. Two colors of the same body swap identically.
