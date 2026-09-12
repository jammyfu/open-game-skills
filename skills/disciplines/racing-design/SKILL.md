---
name: racing-design
description: Speed feel and race social contract. Ask time-trial vs rubber-band vs kart-chaos vs boost-rail vs drift-weight first. Use for vehicles, hover, on-foot speed games. Do not copy a finished item table or a named track.
---

# Racing design

Ask the column:

| Column | What the race is about | Catch-up |
|---|---|---|
| time-trial | line, brake, ghost | none |
| rubber-band | pack stays in camera | position-based speed |
| kart-chaos | items + pack | last-place power, first-place tax |
| boost-rail | rails, tricks, chains | mild |
| drift-weight | weight transfer, tire slip | none or tiny |

Mario Kart is one filling of kart-chaos. Sonic-likes fill boost-rail. Neither is a rule.

## Speed feel (all columns)

1. Camera owns speed more than the speedometer. FOV, height, and look-ahead scale with velocity. Shake is a last 5%.
2. Acceleration curve is audible. A boost needs a start transient, a sustain, and a snap-off. Silent speed is a bug.
3. Drift / slide is a commitment with a readable fail (spin, scrape, slow). Instant snap-back kills the column.
4. Logic step owns vehicle velocity. Render interpolates. Never scale Engine.time to fake speed.
5. Collision with walls: glancing slide, not a full stop, unless the column is drift-weight and the wall is a tire killer.

## Social contract

- time-trial: a ghost is information, not a bumper. No item that deletes a clean line.
- rubber-band: the pack must stay visible. Catch-up may not exceed the gap a skilled player can reopen in one straight.
- kart-chaos: first place gets weaker items; last place gets a closer. Publish the table. A blue-shell analogue must have a readable tell and a counter, or cut it.
- boost-rail: a dropped combo costs speed, not the race by itself.
- drift-weight: assists are a settings column, not hidden rubber.

## Track grammar

One readable decision every few seconds of travel: brake, hold drift, take a shortcut, or spend a boost. Shortcuts that skip a taught section must cost a risk (narrow, off-camber, item-exposed).

## Accept

- Player can name the column after one race
- Closing a 1s gap on time-trial takes a better line, not a hidden buff
- On kart-chaos, last place can rejoin without first place being deleted from off-screen
- Boost off sounds different from boost on
