---
name: menu-flow
description: Pause, shop, inventory screens. Menus release look. Complements ui-flow. Use for 菜单, 暂停, 确认取消.
---

# Menu flow

Ask first: which menus freeze the sim? Which stay live (hotbar)?

Rules: Esc is pause or back, never an attack (`kb-mouse-map`). Confirm and cancel are different keys (`input-design`). Shop uses shop-price. Bags use inventory-economy. A menu that opens mid-hitstop waits until the clock resumes. Stacks with ui-flow for widget grammar.

## Ownership

Play owns look + verbs. Menu owns widgets. Opening a menu releases pointer-lock / look. Closing restores the play column, not a stuck hold.

Multi-touch: one finger look and one finger move must both work (`kb-mouse-map` + `platform-targets`). A game hotkey must not eat the menu shortcut that the player can see.

Pointer cancel and blur: every held verb releases. Missing Pointer Lock publishes a fallback (click-to-look or always-relative) instead of a dead camera.

## Accept

A fighter can pause and quit with keyboard only. Alt-tab then return does not keep firing. Phone: move + look work together, not only one axis.
