# Pixel foliage wind

Source: [SpriteCook tree wind guide](https://www.spritecook.ai/blog/pixel-art-trees-wind-animation), accessed 2026-11-15. Independently summarized; no source assets or implementation copied.

Split foliage into a fixed wood layer, movable leaf clusters and a dark interior covering exposed seams. Preserve the shared canvas and ground pivot. Composite interior, wood, then foliage; verify rest reconstruction against the source.

Move clusters in integer art pixels with nearest filtering. Use a short stepped loop, slower than rendering, and world-position phase to propagate wind between trees. Outer foliage responds more than the center. Local gusts alternate with calm; damped canopy recovery must settle. Thin conifers may bend with height while keeping their feet anchored; do not apply that deformation to thick trunks.

## Project-specific delivery contract

Deliver layer PNGs, pivot metadata, timing parameters, a contact sheet and runtime capture separately. Declare art resolution, coordinate convention and sorting policy before implementation. Reject cropped excursions, accidental background holes and camera-dependent wind phase. Compare identical timestamps at different render rates. A generated contact sheet is visual intent, not proof of exact pixels, usable layers or temporal continuity.

## Generated-material handoff

For generated inputs, preserve the original alongside normalized art. Record resize method and alpha policy: reconstruction must name which image it compares against. Color-based ownership requires palette constraints; manually inspected cluster centers are an acceptable fallback, but must not be described as automatic semantic segmentation.

Export actual registered layers, not a diagram depicting layers. Render a calm–gust–calm cycle and retain per-sample group offsets. Show a separate debug recording with cluster IDs, displacement vectors and wind position. A dark static interior can deliberately preserve the old silhouette; disclose that limitation and separately inspect moving outer edges.

Require pixel comparisons for anchored roots, rest reconstruction and newly transparent holes inside the reference silhouette. Check translated layer bounds before compositing, since image libraries can silently crop. Decode the exported GIF to verify duration. Keep a simple procedural fixture as a control, but use the generated source in the principal demonstration whenever generated-asset animation is requested.
