---
name: threejs
description: Three.js / R3F adapter for open-game-skills primitives. Use for WebGL games that need a fixed logic clock, pose playback, hits, and camera sphere sweep.
---

# Three.js adapter

Map the six primitives. Do not put feel rules in `useFrame`.

| Primitive | Binding |
|---|---|
| poll_input | key Set + pointer-lock deltas |
| now_logical_frame | accumulator `while (acc >= 1/60)` |
| play_pose | `AnimationMixer.setTime(frame/60)` or pose snapshot |
| query_hits | authored Box3 / sphere vs hurt boxes, not `Raycaster` for melee |
| apply_knockback | next logic frame after hitstop hits 0 |
| juice_hook | camera shake / flash uniforms |

Camera anti-clip: sweep a sphere along pivot→desired against a collision mesh. `Raycaster` to a point is not enough.
R3F: run the accumulator inside `useFrame`, keep JSX free of clocks.
