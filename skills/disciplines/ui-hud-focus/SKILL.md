---
name: ui-hud-focus
description: HUD and menus own focus. Ask play-hud vs pause-stack vs pad-cursor vs safe-area. Opening UI must park gameplay reads. Closing must not dump a buffered attack.
---

# UI HUD focus

Ask the column:

| Column | Who reads input |
|---|---|
| play-hud | combat owns sticks; HUD is paint only |
| pause-stack | a stack of menus; top owns buttons |
| pad-cursor | virtual cursor on lists |
| safe-area | notches, overscan, 16:9 letter |

## Rules

1. Menu open parks gameplay. Same handoff as cutscene-handoff and input-combo-test.
2. HUD never hides a tell that attack-tell requires. Low-HP flash is juice, not the only warning.
3. Pad-cursor and mouse pointer are one focus. Two highlights is a bug.
4. Safe-area: interact prompts and combo counters stay inside the published inset.
5. Localization overflow is game-localization. This skill only parks input and paints slots.

## Accept

Pause, inventory, map, then close: actor is idle, no buffered special. A 21:9 screen still shows the lock mark.
