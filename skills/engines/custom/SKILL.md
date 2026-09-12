---
name: custom
description: Engine adapter for a custom loop. Implement six primitives. Do not invent feel rules here.
---

# Custom engine

Implement only:

```
poll_input()
now_logical_frame()          # fixed 60Hz accumulator, not display fps
play_pose(actor, move, frame)
query_hits()
apply_knockback(actor, vec)
juice_hook(event)
```

Camera sweep is a sphere against world colliders, not a single ray parked on a hit point.
Render may run at any fps. Actor clocks pause per-actor (hitstop) without pausing the world.
