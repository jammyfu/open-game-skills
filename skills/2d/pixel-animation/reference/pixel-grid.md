# Pixel-grid presentation

Source: [SpriteCook pixel-perfect settings](https://www.spritecook.ai/blog/pixel-perfect-pixel-art-game-settings), accessed 2026-11-15. Independent summary.

Choose one logical art resolution. Present it with nearest sampling and an integer scale, centering unused window space. Inspect inherited transforms and per-texture overrides; a project default alone is insufficient. Snap presentation coordinates, not physics state. Avoid fractional zoom and arbitrary sprite rotation unless explicitly opting out of the strict grid. Check text and effects against the same pixel pitch.

## Additional boundary policy

When the window is smaller than the logical canvas, choose minimum window size, cropping, or an explicitly non-integer fallback. Never silently calculate negative letterbox margins. Test odd window sizes, device-pixel ratio and moving cameras. Reject mixed apparent pixel sizes by visual inspection: AI-generated pixel-style artwork is not automatically a native-resolution sprite. Exact block replication tests validate the renderer, not the artistic authenticity of the input.
