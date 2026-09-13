---
name: stealth-info
description: Use when stealth perception state needs readable cones, suspicion, sound/light indicators or threat lanes without letting HUD presentation create, widen or bypass the underlying perception truth.
---

# Stealth info

Ask: `cone-alert | suspicion-meter | full-sim-sound`.

## Ownership

`enemy-perception` owns detection/suspicion truth. `enemy-ai` owns state transitions after perception. `stealth-info` consumes authorized perception data and decides how much of it the player may see, hear or otherwise perceive.

## Contract

Publish:
- stable observer/target IDs
- perception revision
- authorized presentation channel IDs
- source reason categories such as visual, sound, light or project-defined
- optional normalized suspicion/threshold data from the perception owner
- display latency/smoothing policy that cannot alter source state

Detection is not universally `cone + light + noise`, stealth failure is not universally combat/reset, and instant failure is not universally disabled. Those are project design choices.

## Runtime rules

1. A HUD cone/meter is derived presentation, not a detection query.
2. Occluded/unknown information remains constrained by the perception owner's visibility policy.
3. Presentation smoothing may delay or interpolate a display but cannot feed back into the authoritative suspicion value.
4. Localization/color/audio alternatives preserve meaning without changing detection truth.
5. Stale observer/target revisions are discarded instead of presenting ghost threat state.

## Acceptance

For the same authorized perception snapshot and UI policy revision, the same canonical information is exposed. Disabling or changing HUD presentation does not change who detects whom, and evidence can name the authoritative perception reason separately from the display cue.
