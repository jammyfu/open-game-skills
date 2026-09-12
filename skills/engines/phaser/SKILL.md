---
name: phaser
description: Phaser 3 adapter for browser 2D. Bind the six primitives. Arcade/Matter collide is query_hits, not the render list. Do not freeze game.loop for hitstop.
---

# Phaser adapter

Use when the user says Phaser / 微信小游戏常见 Web 2D / arcade runtime. PixiJS is the raw display list. Phaser is the scene + arcade body runtime. Do not write arcade logic against a raw PIXI ticker.

Bind:

| Primitive | Phaser |
|---|---|
| poll_input | input.keyboard + gamepad + pointers; never read keys in a render event |
| now_logical_frame | a fixed step beside scene.update; 60Hz default |
| play_pose | sprite anims or a Spine plugin; hitstop scales *that* anim, not `scene.sys.game.loop` |
| query_hits | arcade/matter overlap or your own hitbox list |
| apply_knockback | body velocity on the logic step |
| juice_hook | cameras.shake / particles after the logical hit |

## Rules

1. `scene.physics.pause()` is not hitstop. Hitstop is ActorClock = 0.
2. Collision groups map to collision-layers. Render list is not a hurtbox.
3. Pointer lock and touch split still use browser-input.
4. Spine in Phaser still uses skills/2d/spine-skeletal tracks.
5. No Phaser API encyclopedia. Six primitives only.

## Accept

A 60Hz logic step survives a 30fps canvas. Hitstop does not freeze emitters belonging to other actors.
