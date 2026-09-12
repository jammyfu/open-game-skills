---
name: kb-mouse-map
description: Map keyboard and mouse roles per game type. Mouse aims, clicks, or does neither. Keyboard walks or is a button box. Use when the user mentions WASD, keybinds, or mouse look.
---

# Keyboard × mouse map

Ask the genre column first. Do not copy a finished title's default.ini into the rules.

| Column | Keyboard does | Mouse does | Do not |
|---|---|---|---|
| fighter-plane | arrows / WASD = walk + motion; UIO/JKL = buttons | optional UI only | mouse-aim the punch |
| fps-look | WASD move; space jump; shift sprint | look + fire (LMB) + alt-fire (RMB) | bind look to keys unless accessibility |
| tps-orbit | WASD move relative to camera | orbit camera + lock optional | let LMB be both attack and camera drag |
| twin-stick-kb | WASD move | mouse aim independently | snap aim to walk |
| click-world | hotkeys for verbs | select, move-order, camera-drag | require hold-W to walk |
| race-line | arrows / WASD steer + accel | look-behind or UI, not steer | mouse-steer unless a column says so |
| platform-side | arrows / WASD run + jump | unused in play, UI only | mouse-click to jump |
| menu-heavy | confirm / cancel / skip | click widgets | fight and menu on the same click |
| build-sim | hotkeys + camera WASD | pick tiles, rotate, confirm | hide every verb behind a right-click tree |

## Split of labor

1. **Look** and **move** are two axes. If mouse owns look, keyboard owns move. If keyboard owns motion-gestures (fighter), mouse does not own look.
2. **LMB** is one job in play: fire, or confirm-click, or attack. Never fire + orbit-drag on the same press.
3. **RMB** is the other job: aim-down, camera-drag, or cancel. Publish it.
4. **WASD** is either world movement *or* fight-plane movement. Switching mid-match is a bug.
5. Numpad / extra mouse buttons are extras. Core verbs must work with WASD + mouse + Space + LMB + RMB + Esc.
6. Rebind keeps the grammar (`input-design`). Swapping W and Jump is legal; making Jump also Confirm is not.
7. Accessibility: hold-to-toggle sprint, mouse-keys, and remap of look-to-stick must not change cancel windows.

## Street-fighter-like 3D (worked example, not a clone)

```
column: fighter-plane
W/S or Up/Down   = jump / crouch   (plane, not free 3D fly)
A/D or Left/Right = walk the plane
U I O / J K L     = punches / kicks
mouse             = menus + replay only
```

If they later pick full-3D sidestep, switch column to a walk-strafe keyboard and give mouse *camera only* or no mouse look. Do not keep motion-gestures and mouse-aim on the same actor.

## Accept

A player can say in one sentence what WASD does and what the mouse does. Unplugging the mouse still lets a fighter walk and attack. Unplugging the keyboard still lets an FPS look around (but not walk).
