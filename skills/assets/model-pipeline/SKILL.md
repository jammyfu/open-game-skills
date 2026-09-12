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
7. Layout data is shared by render and collision. Do not author two mismatched floors.
8. Do not static-batch a skinned or socketed node. Attach sockets survive optimize.
9. After texture compress, re-check pose and collision. A cheaper map that moves a foot is a failed export.

Accept: dropping the file into any adapter leaves the character standing on y=0 at human scale. A weapon still finds its socket.
