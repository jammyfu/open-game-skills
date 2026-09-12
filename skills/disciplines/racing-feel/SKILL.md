---
name: racing-feel
description: >
  Engine-neutral speed and race-pressure systems. Pick a column first.
  Use when a vehicle or runner feels floaty, catch-up is invisible, or
  boost reads as a stat instead of a timing verb. Kart and rail titles
  are columns, not templates.
---

# Racing feel

Ask the column before writing a vehicle or runner.

| Column | Speed comes from | Contest |
|---|---|---|
| drift-kart | drift charge + slipstream + optional items | pack + last-lap pressure |
| boost-rail | pads, rails, queued boost, path memory | time attack vs ghost, or pack |
| grip-weight | tire load, brake bias, weight transfer | clean line vs dirty air |
| combat-arena | boost + weapons on an arena loop | disruption is the sport |

Do not mix grip-weight tire sim with drift-kart item rain on the same vehicle unless the user asked for that hybrid and named both columns.

## Shared clock

Logical tick stays 60 Hz even if render drops. Speed is a state, not a camera FOV trick. FOV and camera lean are juice after the physics step.

```
each logical frame:
  sample steer / accel / brake / drift / item
  integrate traction (column model)
  apply boost / slipstream / surface
  resolve collisions
  update race ranking + pressure
  camera follows AFTER integration
```

## Speed readability (all columns)

- Acceleration curve is steep then flattens. Top speed is a ceiling the player can feel approaching.
- Boost is a timed verb with startup, hold, and falloff. It is not +12% forever.
- Camera: extra FOV only during true acceleration, not while coasting at cap.
- Audio pitch tracks speed. Surface change must change grip and sound in the same frame.
- Near-miss and slipstream need a visible / audible cone, not a hidden multiplier.

## Pack pressure

Ranking is public. First place is lonely; mid-pack is noisy.
Catch-up, if any, is a **named column**, not a silent stat:

| Catch-up column | What it may do | What it may not do |
|---|---|---|
| none | pack skill decides | secretly scale top speed |
| draft-only | sit in wake to gain | teleport the last place |
| item-pressure | worse rank → richer item table | auto-win the last lap |
| ghost-assist | rubber the *ghost*, not rivals | rewrite player inputs |

If you turn item-pressure on, publish the table. Hidden catch-up destroys trust.

## Drift-kart notes

- Drift is a hold that charges a burst. Tight turn without charge is just a turn.
- Mini-burst on release. Failed drift (wrong stick, wall) dumps charge.
- Items are information weapons: they create look-behind and blocking lines. Do not copy any commercial item list. Write 3-5 verbs max (slow / seek / shield / steal / boost).
- Off-road is a tax, not a cliff, unless the track authored a cliff.

## Boost-rail notes

- The path is a sentence the player memorizes. Rails, pads, and queues are punctuation.
- Boost queue: tap stores one; spend on a straight. Missing a pad is readable.
- Homing / grind is a commit onto a spline. Exit is a jump or a drop, not a cancel-anything.
- Speed character vs power character is two data rows, not two codepaths.

## Grip-weight notes

- Lateral grip falls off with slip angle. Brake lock is a player error you can hear.
- Weight transfer on entry/exit is the skill. Assist columns (ABS, TC, racing line) are toggles, default off for the "honest" row.

## Iron rules

- Do not fake speed only with motion blur.
- Do not drop the simulation rate to make boost feel heavier.
- Collisions use a vehicle capsule/hull, not the render mesh.
- Respawn puts you back on the racing line with a short speed floor, then hands control back. No full-race rewind unless the save column says so.
- Track width and corner radius are difficulty. Rubber-banding is not difficulty.

## Accept

A player can close their eyes and still tell accelerating vs cap vs off-track from sound. Passing a rival on the inside is a decision, not an animation. Boost has a beginning and an end. Catch-up, if present, can be explained in one sentence.
