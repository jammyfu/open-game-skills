---
name: haptic-rumble
description: Use when gameplay or UI events should request controller/device haptics with explicit capability checks, lifecycle, accessibility settings and non-haptic fallback cues.
---

# Haptic rumble

Haptics are presentation driven by authoritative events. They never extend hitstop, hitstun, cancel windows, movement or damage.

## Compatible modes

`off` | `hit-only` | `layered-with-audio`

Treat them as project presets, not mandatory device behavior.

## Contract

Publish event ID, effect/pattern ID, supported actuator/capability requirements, intensity/frequency envelope supported by the target API, retrigger/overlap policy, cancellation/end event and user setting.

## Rules

1. Query device/platform **capability** before requesting an effect; unsupported hardware follows the declared **fallback** without failing gameplay.
2. Haptics are not the sole carrier of **critical** state or warning information when the project requires accessible alternatives; pair with appropriate visual/audio/UI feedback.
3. Comfort/intensity limits are product/device data and user settings, not a universal “cap per second.”
4. Disconnect, focus loss, pause, scene teardown and effect-owner cancellation stop/reconcile active patterns as appropriate.
5. Repeated event callbacks use stable event/effect identity so overlap behavior is deliberate rather than accidental stacking.

## Accept

Test supported/unsupported devices, off/reduced settings, overlap/retrigger, disconnect and cancellation. Gameplay result remains identical, and every required critical cue retains a declared non-haptic fallback.
