---
name: haptic-rumble
description: Rumble as juice on the same event. Use for 振动, 触觉, rumble.
---

# Haptic rumble

Ask first: off, hit-only, or layered-with-audio?

Rules: rumble fires from `juice_hook` after the logical hit. It does not extend hitstop or hitstun. Intensity cap per second. Off is a persist setting (`settings-persist`). Missing a pad is not a fail of the slice.

Accept: mute rumble and cancel windows stay the same. A hit still reads on screen and in audio.
