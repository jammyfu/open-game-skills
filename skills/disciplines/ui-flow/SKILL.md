---
name: ui-flow
description: Pause, inventory, map, shop, rebind pages. Ask diegetic vs pause-pages vs hotbar-only vs radial. Opening UI must not eat a combat input already in the buffer unless pause-full-stop.
---

# UI flow

Ask the column:

| Column | World clock |
|---|---|
| diegetic | keeps running |
| pause-pages | stops sim |
| hotbar-only | no page |
| radial | short freeze |

## Rules

1. Confirm and Cancel stay distinct.
2. Rebind lives here as a page; roles live in kb-mouse-map.
3. Shop pages use shop-price. Map pages use world-map pins.
4. Do not cover a boss tell with a level-up modal.
5. Safe area follows platform-targets.

## Accept

- Opening inventory does not fire the buffered attack
- Every page closes with the same Cancel role
