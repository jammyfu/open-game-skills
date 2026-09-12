---
name: pixel-animation
description: Generic pixel-art animation contract — hit frames equal hurtbox frames, no long blends pretending to be cancels.
---

# Pixel animation

One cell = one pose the combat clock can name. Startup / active / recovery are frame counts, not a 200ms crossfade.
The frame a slash reads as a hit is the frame the hurtbox exists. Do not offset them.
Smear frames are juice. They do not extend i-frames unless authored.
Palette swaps beat extra sheets when you only need a rank tint.
Hitstop holds the current cell; it does not skip to idle.
