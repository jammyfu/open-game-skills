---
name: pixijs
description: PixiJS adapter. Fixed logic step separate from PIXI.Ticker. Use with 2D / Spine.
---

# PixiJS adapter

`PIXI.Ticker` renders. Your loop owns 60Hz logic. Hitstop sets that actor's pose clock to 0, never `ticker.stop()`.
Display objects follow pose. Collision is a second graph (AABB / SAT), not the scene graph.
Camera is a container offset + clamp. No 3D sphere sweep here — use `camera-anti-clip` only if you moved to 3D.
