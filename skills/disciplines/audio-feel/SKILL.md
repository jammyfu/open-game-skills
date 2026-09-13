---
name: audio-feel
description: Use when authoritative gameplay or UI events need audible cues, music-state changes, surface/speed feedback or looping audio whose identity, lifecycle and fallback must remain separate from gameplay timing.
---

# Audio feel

This skill owns **event-to-audio presentation mapping**. `audio-buses` owns routing/mix; gameplay systems own the logical event and timing.

## Compatible modes

`minimal-foley` | `layered-action` | `adaptive-music`

Modes select presentation density, not a different gameplay clock.

## Event contract

For each important cue publish applicable data:

```text
event ID / logical event source
cue ID or state transition
variant/seed policy when randomised
start/stop/retrigger policy
loop owner and cancellation/end event
spatial/surface context
fallback if asset/device/voice is unavailable
bus/snapshot request -> audio-buses
```

A logical event timestamp identifies **why/when the cue was requested**. Actual audio playback may have buffering/device latency and must not be used as the authoritative hit, cancel, movement or UI clock.

## Rules

1. Hit/miss/danger/speed/readability channels are project choices. Audio must not be the sole required critical signal when an accessibility/product requirement needs another channel.
2. Music states/stems are project data; do not require a universal explore/fight/win/fail/retry set.
3. Loops stop or transition from explicit state/end events, including cancellation/retry/scene teardown; duplicate callbacks remain idempotent.
4. Surface/velocity/pose data may parameterise cues, but audio does not infer or modify hitboxes, movement speed or animation state.
5. Gain, pitch, duck amounts and cue lengths are authored/validated in context, not universal constants. Routing/ducking stays in `audio-buses`.

## Accept

Replay named logical event traces including overlap, cancellation, retry and missing-cue/device fallback. Cue IDs and lifecycle decisions are explainable from event/state data, while disabling or delaying audio does not change gameplay outcomes.
