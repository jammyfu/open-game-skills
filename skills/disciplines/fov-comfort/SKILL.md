---
name: fov-comfort
description: Use when camera field of view, zoom, shake, motion amplification, or comfort settings need boundaries that preserve gameplay meaning across user preferences.
---

# FOV comfort

Choose: `fixed | player-fov | comfort-pack`.

## Contract

Publish:
- stable `comfort_profile_id` and profile revision
- adapter `projection convention` (vertical, horizontal or derived)
- supported min/default/max or authored camera-state bounds
- baseline-plus-temporary-effect composition policy
- persistence owner (`settings-persist`)
- supported aspect/device matrix and evidence

This skill owns comfort-facing camera settings and their interaction with authored camera effects. It does not own hitboxes, lock-on range, projectile spread or other gameplay geometry.

## Rules

1. Aspect-ratio conversion must not silently change the intended framing policy.
2. A player FOV setting persists through `settings-persist`. Temporary sprint/aim/impact FOV effects are authored deltas or camera states layered on the user's baseline unless the project explicitly defines another composition rule.
3. Reduced/off camera shake is an accessibility/comfort option. Disabling shake must not remove logical tells, damage, lock state or timing.
4. If a wider/narrower FOV exposes camera collision defects, route them to `camera-anti-clip`; document platform bounds rather than using them to conceal unrelated defects.
5. FOV-dependent UI/reticle projection is recomputed from the active camera projection rather than assuming the default profile.

## Acceptance

At supported profile bounds and aspect ratios, replay the same `gameplay trace`. Hit results, lock eligibility and movement state remain unchanged while framing/projection updates correctly. Record profile/revision, projection convention and the camera/device combinations actually tested.
