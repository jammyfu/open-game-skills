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

## Layered impacts and variation

For `layered-action`, build impact cues from roles rather than one sample: a contact transient, a body/weight layer, a texture layer (flesh, cloth, armor, debris) and an optional space/tail layer. Which roles exist per strength or source class, and their lengths and levels, are project data.

1. Parameterise cues from data the gameplay owner already publishes: strength class, source kind (strike limb, projectile, throw), counter/critical flags, combo index and position. Do not infer them from animation names, particles or audio state.
2. Make the repetition policy explicit: variant pool, authored pitch/gain jitter, and no-immediate-repeat or round-robin where repeats are audible. Presentation randomness uses its own stream and never draws from the gameplay/replay RNG.
3. Vocal cues (effort, pain, defeat) use a per-actor voice slot with an authored interrupt/priority policy. They are parameterised by actor profile data, and can be disabled when the product offers that setting, without hiding critical information.
4. Prepare decoded, streamed or procedurally synthesised buffers away from the frame that presents the event: on a load screen, in idle slices or in background work. A cold first use must not stall the hit frame; if a buffer is not ready, apply the declared fallback instead of blocking.
5. Moment-specific mix changes, such as a defeat muffle or a duck, are snapshot requests to `audio-buses` and are released by explicit state/end events.

## Accept

Replay named logical event traces including overlap, cancellation, retry and missing-cue/device fallback. Cue IDs and lifecycle decisions are explainable from event/state data, while disabling or delaying audio does not change gameplay outcomes.

Objective signal checks are tool-level evidence that synthesis or mapping did what was specified. Examples: finite output, no clipping, onset position, level/spectral ordering across strength classes, and pitch range for vocal cues. Perceived quality stays not-run until a human listening pass is recorded.
