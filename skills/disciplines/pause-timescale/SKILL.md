---
name: pause-timescale
description: Pause, bullet-time, and UI freeze are not hitstop. Ask hard-pause vs bullet-time vs ui-freeze vs online-pause. ActorClocks stay honest.
---

# Pause timescale

Ask the column:

| Column | What stops |
|---|---|
| hard-pause | world + combat clocks, audio beds duck |
| bullet-time | world scale < 1, player scale published |
| ui-freeze | world stops, cursor lives |
| online-pause | only if netcode column allows |

## Rules

1. Hitstop freezes two colliding ActorClocks. Pause is a world scale. Do not reuse the hitstop flag.
2. Bullet-time publishes both scales. Cancels and i-frames still count actor frames, not wall clocks.
3. UI-freeze must not leave a held attack charge running.
4. Online-pause is none unless both peers agree. See netcode-feel.
5. Retry must not stack the paused BGM. See audio-feel.

## Accept

Open inventory mid-swing: charge does not complete behind the menu. Bullet-time does not silently add cancel frames.
