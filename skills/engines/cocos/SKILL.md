---
name: cocos
description: Cocos / minigame adapter. Six primitives only.
---

# Cocos adapter

Bind `poll_input` · `now_logical_frame` · `play_pose` · `query_hits` · `apply_knockback` · `juice_hook`.

Do not freeze the engine ticker for hitstop — scale the actor clock. Minigame input stacks `browser-input`. The same three disciplines must run on `phaser` with only this file changed.
