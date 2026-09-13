---
name: spine-skeletal
description: Use when a 2D skeletal character needs bind, weighting, layered-track, attachment, or per-actor hitstop playback conventions without moving gameplay timing into animation.
---

# Spine / 2D skeletal

Order: hierarchy → bind → weights → mesh check at bends → layered clips → export.
Bind in setup pose. Weight from the parent bone down. Use the minimum mesh density that preserves the required deformation; do not impose a universal vertex band across characters and camera distances.
Tracks: 0 locomotion, 1 attack overlay, 2 face/VFX. Hitstop sets *that skeleton* timeScale to 0. Never freeze the render ticker.
Pack atlas by draw order to cut material switches. Choose binary or text skeleton data according to the target runtime, debugging needs and build pipeline; do not assume one format is universally smaller or safer.
Wear / cancels still live in `durability-economy` and `action-feel`. The skeleton only plays the pose it is told.

## Accept

Scrub setup, locomotion and overlay tracks while showing the logical gameplay clock. Bind pose and weighted bends remain stable; pausing one skeleton for hitstop does not stop unrelated actors or the render loop. Missing attachments use a declared fallback, and changing an animation blend never creates extra gameplay hit frames.
