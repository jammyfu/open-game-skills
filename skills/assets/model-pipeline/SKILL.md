---
name: model-pipeline
description: Generic 3D model contract for games — units, origin, collision vs render, export. Use before rigging or dropping a mesh in-engine.
---

# Model pipeline

1. 1 unit = 1 meter. Origin at the feet (characters) or bounds center (props).
2. Apply / freeze transforms before export. Do not fix scale in the game loop.
3. Render mesh ≠ collision mesh. Collision is hulls / capsules / simplified tris.
4. Joint loops at bend points if the mesh will deform.
5. Export glTF with extras you actually read. AI-generated meshes are retopo'd before bind.
6. Name sockets (hand_r, weapon, camera_pivot) in the file, not in tribal knowledge.

Accept: dropping the file into any adapter leaves the character standing on y=0 at human scale.
