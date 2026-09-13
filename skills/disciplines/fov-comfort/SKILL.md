---
name: fov-comfort
description: Use when camera field of view, zoom, shake, motion amplification, or comfort settings need boundaries that preserve gameplay meaning across user preferences.
---

# FOV comfort

Choose: `fixed` | `player-fov` | `comfort-pack`.

This skill owns comfort-facing camera settings and their interaction with authored camera effects. It does not own hitboxes, lock-on range, projectile spread or other gameplay geometry.

## Rules

1. Publish which FOV convention the adapter exposes (vertical, horizontal, or derived) and the supported min/default/max. Aspect-ratio conversion must not silently change the intended framing policy.
2. A player FOV setting persists through `settings-persist`. Temporary sprint/aim/impact FOV effects are authored deltas or camera states layered on the user's baseline, not a hidden replacement for it.
3. Reduced/off camera shake is an accessibility/comfort option. Disabling shake must not remove logical tells, damage, lock state or timing.
4. If a wider/narrower FOV exposes camera collision defects, fix `camera-anti-clip`; do not restrict the setting merely to hide clipping unless the platform budget requires a documented bound.
5. Any FOV-dependent UI, reticle or aim projection must be recomputed from the active camera projection rather than assuming the default FOV.

## Accept

At min/default/max FOV and supported aspect ratios, replay the same gameplay trace. Hit results, lock eligibility and movement state remain unchanged while framing/projection updates correctly. Turn shake off and verify the encounter remains readable through pose/audio/UI alternatives. Record which camera/device combinations were actually tested.
