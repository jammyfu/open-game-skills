---
name: attack-tell
description: Use when an attack, grab, area hazard, projectile, or one-shot-capable action becomes active before players receive a readable and accessible warning through the intended sensory channels.
---

# Attack Tell

This skill owns the **warning contract before logical activation**. `enemy-kit-balance` owns move balance; `action-feel` owns logical move timing; `camera-shots`/lock systems own framing.

## Modes

| Mode | Primary warning channel |
|---|---|
| pose-only | silhouette/pose change |
| pose-audio | pose plus authored sound cue |
| marked-aoe | spatial floor/beam/volume mark before activation |
| color-flash | color flash only as an additional channel |

The mode is project data. Do not assign universal warning modes by attack class.

## Timing contract

Publish `tell_start_tick` and `activation_tick` (or equivalent logical events). The warning must begin before the harmful/grab/activation event by the authored interval. Presentation interpolation may smooth the tell but cannot move logical activation earlier.

Channels are explicit: pose/motion, spatial mark, audio, haptic, text/icon, color. Accessibility settings may suppress some channels, so critical warnings need the project's required redundant channel policy. Color alone should not be the only mandatory channel when color accessibility requires another cue.

Off-screen policy is project-specific: camera reframing, edge indicator, audio cue, attack suppression, spawn policy or intentional unseen threat can all be valid when authored and tested.

## Acceptance

Log tell start, activation and channel availability for representative attacks. Test immediately-before/at activation boundaries, sound-disabled and reduced-flash/color-accessibility settings, plus off-screen conditions supported by the project. A VFX flash that begins on the activation tick is accent, not evidence of an earlier tell.
