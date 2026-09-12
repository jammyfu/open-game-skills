---
name: audio-buses
description: Mix buses, not more one-shots. Ask sfx-bus vs music-bus vs duck-on-hit vs retry-clear. Timing stays in audio-feel.
---

# Audio buses

Ask the column:

| Column | Route |
|---|---|
| sfx-bus | hits, UI, footsteps |
| music-bus | beds, stems |
| duck-on-hit | music drops while a published hit plays |
| retry-clear | stop beds before the next start |

## Rules

1. Hitstop does not mute SFX. It may duck music.
2. Retry-clear: no stacked title themes.
3. Dodge or pause may duck music; they do not change cancel windows.
4. Missing VO is not a crash.
5. Do not invent five more audio skills.

## Accept

Die and retry: one music bed. A hit ducks music then returns.
