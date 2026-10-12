---
name: model-pipeline
description: Use when 3D assets need consistent source units, origins, collision proxies, transforms, sockets, export rules, or engine-ready validation.
---

# Model pipeline

1. Publish the source/interchange unit and axis convention. For glTF, author physical scale in meters; an engine adapter may convert once at import. Do not repair scale continuously in the game loop.
2. Characters use a documented ground/contact origin; props use a documented pivot appropriate to placement. Do not assume every runtime uses the same up axis or engine unit.
3. Apply/freeze authoring transforms before export when the format/workflow requires it, while preserving skin and animation transforms.
4. Render mesh ≠ collision mesh. Collision uses explicit hulls, capsules or simplified meshes appropriate to the target physics system.
5. Deforming meshes keep topology needed for the required poses; AI-generated meshes are cleaned/retopologized when deformation, UV, shading or performance evidence requires it.
6. Export only metadata/extras that a consumer actually reads. Name required sockets/attachment points in the asset contract rather than tribal knowledge.
7. Shared layout measurements drive both render and collision. Do not author two mismatched floors or two incompatible scales.
8. Optimization must preserve skinned nodes, sockets, morphs and required animation data. Do not merge/batch nodes whose runtime identity is required.
9. After texture/mesh compression or LOD processing, re-check silhouette, pose, socket positions, bounds and collision.

## Accept

Import the asset into the selected adapter with exactly one documented unit/axis conversion. The character or prop lands at the intended physical scale and contact plane, required sockets still resolve, animation/morph data survives, and collision overlays the render body within the project tolerance. Re-export/reimport must not accumulate rotation or scale corrections.

## Asset fit and perceptual LOD

Use [quality and LOD](reference/quality-lod.md) when models are individually valid but physically incompatible, reductions lose identity, or distance thresholds flicker. Deliver a measured fit record and tier recipe with silhouette/deformation/socket guardrails; triangle counts alone are not acceptance. [Scene assembly](../../disciplines/scene-assembly/SKILL.md) owns placement into a level, not this exporter.
