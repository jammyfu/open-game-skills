---
name: parry-guard
description: >
  Block, parry, and guard-break as data. Use when block is a pose with no
  window, or when a parry flash freezes the world. Stacks on action-feel.
---

# Parry / guard

Ask the column.

| Column | Block | Parry |
|---|---|---|
| hold-block | hold reduces damage | none |
| chip-block | hold, chip still bites | none |
| parry-window | short tap window | on-success cancel |
| stance-guard | direction or stance | optional |

Parry-window is a move row with startup / active / recover, not a juice flash.

## Clock

Guard is an ActorClock state. Hitstop still only freezes the two colliding clocks.
A successful parry is a published edge on the combo graph (stun, punish, or resource).
Guard-break is a named result when chip or a breaker exceeds a meter. It is not surprise armor-off.

## Iron rules

- Block and parry are different jobs or a documented hold-vs-tap on one job.
- Invuln frames, if any, are on the row next to dodge-iframe. Do not hide them in VFX.
- A missed parry must be punishable inside the written recover.
- Color-safe: success is pose + audio + icon, not a green flash only.

## Accept

A new player can block in the first minute. A lab dummy can hold block. Frame advantage after parry is visible in training-mode.
