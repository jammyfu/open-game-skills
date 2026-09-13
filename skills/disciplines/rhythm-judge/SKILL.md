---
name: rhythm-judge
description: Use when timed input must be judged against a chart or action timeline and the project needs stable event identity, clock mapping, calibration and versioned judgement windows.
---

# Rhythm judge

Ask the timing model: audio/song-clock, simulation/action-clock, hybrid, or existing.

## Contract

Publish:
- stable `chart_id` and chart revision
- stable `note_event_id` / timing-event identity
- authoritative timing source plus explicit `clock mapping`
- input timestamp source
- judgement window table and revision
- device/user `calibration` offsets and limits
- pause/seek/resume policy

## Ownership

This skill owns timestamp-to-event judgement. Audio playback, input sampling, pause, gameplay actions and accessibility settings remain with their owners and provide mapped timestamps/configuration.

## Rules

1. Perfect/good/miss/other grades and window widths are project data; an off-window input is not universally one specific grade.
2. Calibration shifts timestamp mapping or authored windows according to policy; it does not mutate chart event times silently.
3. Clock discontinuities, seek/resume and device latency changes are explicit and versioned in evidence.
4. A `note_event_id` is judged at most once for one judgement attempt/request identity.
5. Rendering/audio visualization is not the timing oracle; use the declared clock mapping and captured timestamps.

## Acceptance

Given the same chart revision, event IDs, clock mapping, calibration and input timestamps, the same judgement results occur independent of render cadence. Evidence records early/late delta and the exact window revision used.
