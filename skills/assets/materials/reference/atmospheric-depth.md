# Atmospheric depth for 2D layers

Source: [SpriteCook atmospheric perspective](https://www.spritecook.ai/blog/2d-parallax-background-atmospheric-perspective), accessed 2026-11-15. Independent summary.

Blend distant scenery RGB toward the sky color behind each screen row, increasing the blend with distance. Preserve alpha. Keep gameplay foreground unaffected. Multiplication cannot lighten dark silhouettes; reducing opacity exposes unwanted layers. Cropped or vertically moving backgrounds need an explicit screen-to-sky coordinate mapping. Give each layer independent controls and avoid doubling haze already painted into artwork.

## Delivery and checks

Document color space, sky lookup mapping, layer order and editable depth strengths. Test disabled strength as exact identity, full strength as sky RGB, unchanged alpha, and foreground exclusion. Review background separation in grayscale as well as color. Mathematical checks do not establish readability around the player; perform that review at gameplay scale in the target engine.
