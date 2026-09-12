---
name: spine-skeletal
description: Generic 2D skeletal pipeline using Spine-like runtimes — bind first, weight second, tracks for locomotion vs overlay, per-actor timeScale on hitstop.
---

# Spine / 2D skeletal

Order: hierarchy → bind → weights → mesh check at bends → layered clips → export.
Bind in setup pose. Weight from the parent bone down. Game meshes stay in the 4–20 vertex band unless a face close-up needs more.
Tracks: 0 locomotion, 1 attack overlay, 2 face/VFX. Hitstop sets *that skeleton* timeScale to 0. Never freeze the render ticker.
Pack atlas by draw order to cut material switches. Binary skeleton when the runtime allows.
Wear / cancels still live in `durability-economy` and `action-feel`. The skeleton only plays the pose it is told.
