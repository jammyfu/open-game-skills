---
name: godot
description: Godot adapter mapping open-game-skills primitives onto `_physics_process` and nodes.
---

# Godot adapter

Logic in `_physics_process` (fixed). Input via `Input`. Pose via `AnimationPlayer` / `AnimationTree` speed on *that* node, not `Engine.time_scale`.
Hits: `Area3D` / `ShapeCast3D`. Camera: `SpringArm3D` + sphere shape, never a lone ray.
Feel rules stay in disciplines.
