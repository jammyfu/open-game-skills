---
name: unity
description: Unity adapter. Fixed tick plus per-actor clocks. No Time.timeScale for hitstop.
---

# Unity adapter

Own a 60Hz (or FixedUpdate) actor tick. Hitstop zeroes that actor's clock. `Time.timeScale` is forbidden for combat freeze.
Pose: Animator speed 0 on the actor, or manual root pose. Hits: layer-masked overlap. Camera: sphere cast, Cinemachine collider is an implementation of `camera-anti-clip`, not a replacement for its rules.
