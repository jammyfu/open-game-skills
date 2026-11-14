# Pixel foliage wind

Source: [SpriteCook tree wind guide](https://www.spritecook.ai/blog/pixel-art-trees-wind-animation), accessed 2026-11-15. Independently summarized; no source assets or implementation copied.

Split foliage into a fixed wood layer, movable leaf clusters and a dark interior covering exposed seams. Preserve the shared canvas and ground pivot. Composite interior, wood, then foliage; verify rest reconstruction against the source.

Move clusters in integer art pixels with nearest filtering. Use a short stepped loop, slower than rendering, and world-position phase to propagate wind between trees. Outer foliage responds more than the center. Local gusts alternate with calm; damped canopy recovery must settle. Thin conifers may bend with height while keeping their feet anchored; do not apply that deformation to thick trunks.

## Project-specific delivery contract

Deliver layer PNGs, pivot metadata, timing parameters, a contact sheet and runtime capture separately. Declare art resolution, coordinate convention and sorting policy before implementation. Reject cropped excursions, accidental background holes and camera-dependent wind phase. Compare identical timestamps at different render rates. A generated contact sheet is visual intent, not proof of exact pixels, usable layers or temporal continuity.
