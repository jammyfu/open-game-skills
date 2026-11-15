# Pixel scenery and parallax integration

Source: [Godot official 2D Parallax tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/2d_parallax.html), read 2026-11-15. Independent summary. Inspect the installed version before selecting APIs; the current tutorial uses Parallax2D.

## Engine mapping

Give independently scrolling scenery its own parallax node. Define a repeat canvas covered by child artwork from its top-left origin. Match repeat dimensions to actual coverage; child scaling does not automatically reconcile repeat_size or region_rect. A centered sprite crossing negative coordinates can leave gaps. Fix positioning before adding copies. Zooming out can require additional repeats and vertical artwork coverage. Split-screen cameras require their own parallax presentation nodes and visibility masks.

## Project acceptance additions

Combine this adapter with the [pixel-grid contract](../../../2d/pixel-animation/reference/pixel-grid.md) and [atmospheric-depth contract](../../../assets/materials/reference/atmospheric-depth.md). Preserve logical art pixel size when covering large viewports. Camera-relative draw coordinates must not become the input to world-space wind. For haze, specify the mapping from a parallax layer's cropped rows to sky sampling coordinates.

Test slow camera movement in both directions across a full repeat boundary. Include the widest viewport, maximum supported zoom-out, vertical motion and every split-screen camera. Capture debug repeat rectangles and normal rendering. Check for uncovered strips, repeated silhouettes jumping, changes of apparent pixel size, and haze jumping at wrap boundaries. Record the engine version and actual settings. These are adapter acceptance requirements, not a claim that the offline Pillow example has passed Godot integration.
