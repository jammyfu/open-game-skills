# Pixel-grid presentation

Source: [SpriteCook pixel-perfect settings](https://www.spritecook.ai/blog/pixel-perfect-pixel-art-game-settings), accessed 2026-11-15. Independent summary.

Choose one logical art resolution. Present it with nearest sampling and an integer scale, centering unused window space. Inspect inherited transforms and per-texture overrides; a project default alone is insufficient. Snap presentation coordinates, not physics state. Avoid fractional zoom and arbitrary sprite rotation unless explicitly opting out of the strict grid. Check text and effects against the same pixel pitch.

## Additional boundary policy

When the window is smaller than the logical canvas, choose minimum window size, cropping, or an explicitly non-integer fallback. Never silently calculate negative letterbox margins. Test odd window sizes, device-pixel ratio and moving cameras. Reject mixed apparent pixel sizes by visual inspection: AI-generated pixel-style artwork is not automatically a native-resolution sprite. Exact block replication tests validate the renderer, not the artistic authenticity of the input.

## Attachment and media scaling

Check the whole chain: source normalization → attachment draw size → logical target → window/CSS → exported media. A sprite normalized to 58×74 then drawn at 86×110 is fractionally scaled even if its texture uses nearest. Repeated animated squash can defeat a strict pixel-size contract. Use fixed native attachment dimensions, authored poses and a declared exception when scaling is stylistically necessary. A 640-pixel GIF embedded at 800 pixels is another fractional display step. Offer native-width GIF/PNG evidence and an explicitly integer zoom; do not judge grid fidelity from a compressed or rescaled video crop alone.
