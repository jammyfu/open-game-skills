---
name: debug-slate
description: Label debug tools so they cannot be mistaken for a natural clear. Use with gameplay-validation and gameplay-capture.
---

# Debug slate

## Trigger

A build has teleport, god mode, clear-room, force-phase, unlock-all, or a dummy.

## Inputs / columns

Ask: off | labeled-dev | shipping-hidden.

## Flow

1. Every debug verb writes a visible slate line: what was used.
2. A clip that used teleport / clear-room / force-phase is `gameplay-capture` / debug-stage or adjusted-challenge.
3. Unlock flags flipped by a save editor are named on the slate. They do not become a natural ending.
4. Shipping builds hide the verbs. Dev builds show them.

## Constraints

Debug may not invent a second combat clock. Training cancels stay in `training-dummy` / `training-mode` and must match live.

## Accept

A reviewer can tell from the slate whether the clip was a real-input chain or a scripted scene.
