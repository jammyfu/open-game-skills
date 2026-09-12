---
name: face-morph
description: Face weights contract. FACS / ARKit / visemes. Not a second skeleton.
---

# Face morph

Ask: facs-52 | viseme-15 | stylized-few.

Weights live on the logic tick or a published face tick that cannot change hitboxes. Lip-sync uses visemes (`audio-feel` does not own geometry). Blink and look-at are idle juice.
Do not apply 52 morphs on a distant LOD. Export names stay stable across engines (`character-rig`).
Creator sliders map onto these weights (`avatar-create`). A random photo-to-mesh dump still passes `model-pipeline` and `art-bible`.

Accept: setting jawOpen 0.4 on two machines matches. Combat hurtbox at the head does not scale with a smile.
