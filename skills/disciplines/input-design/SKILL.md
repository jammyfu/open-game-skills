---
name: input-design
description: Button grammar. Tap is commitment, hold is charge or aim, context face-button is the looked-at object. Menus and play do not share a stuck hold.
---

# Input design

Ask the column:

| Column | Grammar |
|---|---|
| few-buttons-context | one face button reads the world |
| orthogonal-fight | each attack button is a distinct move class |
| hotbar-abilities | bar slots, queue or GCD lives in action-feel |

## Rules

1. Tap = commit. Hold = charge or aim. Release can fire.
2. Jump and confirm are not the same key on a 3D climber.
3. The same key must not be Confirm and Cancel.
4. Publish a context priority list if you use a context button (interact > grab > talk > mount > none).
5. Buffer length and cancel graphs live in action-feel, not here.
6. Rebind must preserve the grammar, not just the labels.
7. Play owns look + verbs. Menu owns widgets (`menu-flow`). Opening a menu releases look and pointer-lock. Blur / pointer-cancel releases every held verb.
8. Multi-touch: move and look must work together on a phone. One axis working is not a pass.
9. If Pointer Lock is missing, publish a fallback (click-to-look or always-relative). A dead camera is a ship blocker.

## Accept

- A new player can say what tap vs hold does after one minute
- Context button never attacks
- Fight column buttons do not change meaning when a crate is nearby
- Alt-tab then return does not keep firing
- Phone: move + look work together
