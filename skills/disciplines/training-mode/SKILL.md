---
name: training-mode
description: >
  Engine-neutral practice room. Use when a fighter or action game has no
  place to see frames, dummy wakeups, or input display. Training is a
  sandbox over the same combat clock, not a second ruleset.
---

# Training mode

Ask the column.

| Column | Dummy does | Extra HUD |
|---|---|---|
| dummy-block | hold block / stand / crouch | input display |
| dummy-wakeup | delayed wake, tech or not | frame advantage |
| dummy-record | record 1-2 replies | playback |
| lab-full | all of the above + reset pos | boxes + cancel highlight |

Fighting-design should ship at least dummy-block. lab-full is the default when the user says 「调帧」 / 「训练场」.

## Same clock

Moves, hitstop, cancels, and boxes are the live game rows. Training may freeze, reset, and display. It may not author a longer cancel window.
Reset is a menu job (see menu-flow). Reset returns both actors to marks with meters published (full / empty / custom).

## Display

- Input display is history, not a second buffer.
- Frame advantage is a number after block or hit. It is not a secret buff.
- Box overlay uses hitbox-hurtbox debug colors. Off by default for screenshots? No — on is fine in the lab.
- Dummy HP can be locked. Lock is a toggle, not infinite armor in the real match.

## Iron rules

- No move that exists only in training.
- Recorded dummy cannot read the player's future inputs.
- Online training, if any, still uses netcode-feel delay; it does not hide lag.
- Leaving the lab restores default columns (no leftover dummy AI in versus).

## Accept

A player can confirm a 2-hit string, see +frames, reset in one tap, and take that string into versus unchanged.
