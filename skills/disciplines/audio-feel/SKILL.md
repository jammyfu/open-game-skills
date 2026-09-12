---
name: audio-feel
description: Generic audio that sells speed, hit, and danger. Music is a layer, not the clock.
---

# Audio feel

Ask: minimal-foley | layered-action | adaptive-music.
Hitstop may duck music 1–2 dB; it may not stretch the song to match a freeze.
Speed is pitch + wind + surface, not only a louder loop.
A missing footstep on a locked toe is a bug. UI confirms are shorter than combat hits.

## Stems and states

Publish stems for explore / fight / win / fail / retry. Retry stops the old loop before the new one. A looping SFX dies when the move cancels or the charge drops.
Pose, box, and SFX share the same logical frame (`action-feel`).

Accept: play with the HUD hidden and still hear hit / miss / danger / speed. Dying and retrying never stacks two fight tracks.
