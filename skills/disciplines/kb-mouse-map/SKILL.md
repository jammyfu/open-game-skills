---
name: kb-mouse-map
description: >
  Engine-neutral keyboard and mouse roles per genre. Use when binds fight
  each other, when a fighter inherits WASD+mouse-look, or when rebind
  only changes labels. Ask the genre column first. Stack on input-design.
---

# Keyboard × mouse

Ask the column. Devices have **jobs**, not favorite keys.

| Column | Keyboard job | Mouse job |
|---|---|---|
| vs-fighter | walk + attack rows + start | unused, or menu only |
| fps-look | move + jump + utility | look + fire + aim |
| orbit-third | move + verb row | orbit camera + lock optional |
| twin-stick | move (or left stick emulate) | aim independent of move |
| rts-select | camera + hotkeys + groups | select / command / box |
| point-click | modifiers + cancel | move-to and use |
| racing-steer | steer + accel + look-back | optional look, not steer |
| platform-run | run + jump + interact | unused or camera-only |
| menu-cursor | confirm / cancel / tab | pointer same as cursor |

Do not give an fps-look actor a vs-fighter numpad and a mouse-look at the same time unless the user named a hybrid.

## Jobs, not keys

Every bind is one of these jobs. Rebind changes the key. It does not change the job graph.

```
Move         translate the body
Look         rotate camera or aim
Primary      the attack / fire / confirm of the genre
Secondary    block / aim-down / interact (column picks)
Context      looked-at object (input-design few-buttons-context)
Menu         pause, inventory, map — never on Primary
```

Default *suggestions* (not iron law, always remappable):

| Job | Keyboard suggestion | Mouse suggestion |
|---|---|---|
| Move | WASD or arrows | — |
| Look | — (fps/orbit) | delta + optional hold-to-orbit |
| Primary | J / Space / LMB | LMB in fps / rts / point-click |
| Secondary | K / Shift / RMB | RMB |
| Context | E / F | extra button |
| Menu | Esc / Tab | — |

vs-fighter attack row is a **grid**, not WASD: one axis walk, the other axis punches/kicks or two rows of buttons. WASD as both walk and camera is illegal on this column.

## Genre rules

**vs-fighter**
- Keyboard emulates a stick + 4 or 6 attack keys. Mouse does not aim punches.
- Hold-back is block. Down is crouch. These are directions, not extra mouse chords.

**fps-look**
- Mouse owns yaw/pitch. Keyboard owns translation.
- Fire on a keyboard key is allowed; look on a keyboard key is a last-resort accessibility column.
- Sensitivity and accel are feel sliders. They are not a second combat clock.

**orbit-third**
- Mouse orbits. Keyboard moves relative to camera yaw.
- Lock-on is a toggle job. While locked, mouse may orbit the lock, not free-look the world.
- Click-to-attack is optional; default is a keyboard/pad verb.

**twin-stick**
- Move and aim never share one stick or one WASD cluster.
- Mouse aim is the desktop filling of the right stick.

**rts-select / point-click**
- Select and command live on the mouse. Keyboard is chords and camera.
- Drag box must not start if the cursor began on a dragging UI slider.

**racing-steer**
- Steer is analog or held keys. Mouse-steer is a novelty column, default off.
- Look-back is a hold, not a toggle that strands the camera.

## Iron rules

- Publish a remap screen. Glyphs follow the last used device.
- Confirm and Cancel are never the same key.
- Jump and Primary may share a key only on platform-run, never on vs-fighter or fps-look.
- Left-handed and one-hand columns remake the *layout*, not the jobs.
- Pad and keyboard must expose the same jobs. Missing jobs on one device is a bug.
- Do not copy a commercial default layout as the only legal map.

## Accept

A player can name which device looks and which device moves. Rebind Primary and the character still attacks on that job. Switching to pad mid-session does not invent a new verb. A vs-fighter on keyboard can walk and block without touching the mouse.
