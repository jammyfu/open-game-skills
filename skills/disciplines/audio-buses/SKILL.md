---
name: audio-buses
description: Use when music, SFX, UI, ambience or voice need explicit routing, gain, ducking, mute, snapshot or retry/scene-transition behavior without changing gameplay events.
---

# Audio buses

This skill owns **audio routing and mix state**. `audio-feel` maps authoritative game/presentation events to cues; gameplay owners decide whether an event happened.

## Compatible modes

| Mode | Routing intent |
|---|---|
| sfx-bus | route action/world SFX to a controllable bus |
| music-bus | route music/stems to a controllable bus |
| duck-on-hit | apply an authored duck snapshot/envelope when the project requests it |
| retry-clear | stop/fade/reuse scoped loops so retry/scene transitions do not stack stale playback |

## Contract

Publish applicable bus IDs, parent routing, gain ranges, mute/solo/settings mapping, duck/snapshot source event, attack/release/fade values, voice/sidechain priority, and loop ownership.

The numbers are project data. Hitstop, pause, dodge, combat state or UI state may request a mix snapshot, but this skill does not impose a universal mute/duck policy or rewrite their logical timing.

## Rules

1. Routing is stable by bus/cue identity rather than display label/order.
2. Ducking responds to a named event/state and has an authored return path; repeated events do not leave the mix permanently attenuated.
3. Retry/scene transitions reconcile scoped loops idempotently: a repeated start/stop callback must not stack duplicate music.
4. Missing optional audio degrades through the declared fallback and is reported separately from a gameplay defect.
5. User volume/mute/accessibility settings remain independent from gameplay success criteria.

## Accept

Exercise start/overlap/retry/pause/scene-change plus missing-device/cue cases. Logs show route, active snapshot/duck owner and loop identity; repeated equivalent events settle to the same mix state without altering gameplay clocks.
