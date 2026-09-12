---
name: landing-lag
description: Touchdown frames after air attacks. Use for 落地硬直, 入地.
---

# Landing lag

Ask first: shared lag, per-move lag, or cancel-on-land?

Rules: landing lag is recover on the same clock (`hitstun-recover`). Air-to-land cancels are edges on `combo-design`. Soft land (empty hop) is shorter than an aerial that connected. Platform-jump coyote does not erase lag.

Accept: a heavy aerial that lands is punishable if the column said so. Training shows land-lag frames.
