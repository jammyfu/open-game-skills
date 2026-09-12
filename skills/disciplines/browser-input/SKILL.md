---
name: browser-input
description: Generic web/runtime input. Pointer lock, focus, multi-touch, session. Use when move works but look does not.
---

# Browser input

## Trigger

The game runs in a browser or an embedded web view. Phone or desktop.

## Inputs / columns

Ask: pointer-lock | always-relative | click-to-look.
Stack with `input-design`, `kb-mouse-map`, `menu-flow`, `platform-targets`.

## Flow

1. Publish what happens when Pointer Lock is denied. Dead camera is a blocker.
2. Focus lost: release every held verb (charge, fire, sprint). Do not keep shooting after alt-tab.
3. Multi-touch: move + look together. One axis working is not a pass.
4. Menu shortcuts the player can see must not be eaten by the play bind (`menu-flow`).
5. Session drop (tab discard, permission prompt, lost lock) is a *setup* failure in `gameplay-validation`, not a difficulty proof.

## Constraints

Do not require a mouse for core verbs on phone. Do not require pointer-lock for the first look on desktop without a fallback.

## Accept

Phone: walk and turn in one gesture combination. Desktop: lose focus, return, next tap starts a new move. A denied lock still lets the player look.
