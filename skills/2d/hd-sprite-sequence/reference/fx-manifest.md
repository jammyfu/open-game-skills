# Independent FX comparison manifest

Both reference and candidate JSON use this schema. Paths resolve relative to their own manifest. Every file is SHA-256 verified; the candidate hash is not expected to equal the reference hash. Images are untrimmed RGBA PNGs. Logical frame dimensions and anchors remain exact; density may change.

```json
{
  "schema": "ogs.independent-fx/1",
  "context": {"hflip": false, "vflip": true, "depth": "actor", "interrupt": "clear", "reset": "clear"},
  "frames": [
    {"id": "impact-0", "image": "impact-0.png", "sha256": "actual-file-sha256", "density": 4,
     "frame": {"ax": 16, "ay": 24, "w": 32, "h": 32}, "durationTicks": 3}
  ]
}
```

`density` is source pixels per logical pixel. Image dimensions must equal `w*density` and `h*density` exactly. A source pixel center `(x+.5,y+.5)` is logical `((x+.5)/density-ax,(y+.5)/density-ay)`. Durations are positive integer native ticks. Frame order/IDs, geometry, duration and the entire optional `context` value are compared exactly. Context is a declaration checked for drift, not a substitute for runtime testing; use separate manifests for contexts with different orientation/behavior. Export a repeating animation's expanded native step sequence when one mapping has different durations in different steps; use unique step IDs even when PNGs repeat.

Threshold JSON is required; choose and record it before creating candidates. This example suits a strict silhouette-preserving redraw, not all art styles:

```json
{"alphaThreshold":128,"sampleDensity":4,"minSilhouetteIoU":0.96,"maxCentroidDrift":0.25,"maxPaletteDrift":10}
```

```sh
python3 scripts/validate_fx.py reference.json candidate.json --thresholds thresholds.json --out report.json
```

Install the skill's existing Pillow requirement. Exit code 0 means these pixel/registration checks pass; 1 means failed or blocked input. The report binds both manifest hashes and thresholds. It never grants art acceptance.

- **Silhouette IoU**: binary alpha at `alphaThreshold`, nearest-sampled onto a common logical grid at `sampleDensity`; intersection/union. Both empty masks give 1. Different canvas bounds or pivots cannot hide displacement. Geometry mismatch fails independently. Comparison grids above 16 million samples are blocked.
- **Centroid drift**: Euclidean distance in logical pixels between all-alpha-weighted pixel-center centroids, including subthreshold AA pixels. One empty frame versus a nonempty frame fails. Both empty give 0.
- **Palette drift**: candidate visible RGB → nearest reference visible RGB Euclidean distance, averaged with candidate alpha weights. Visible means alpha at least `alphaThreshold`. RGB beneath alpha zero is excluded. This directed metric tests candidate palette proximity, not preservation of every native color region or perceptual color identity; review regions and playback separately. A missing color region can require independent masks/visual review.
- **SHA/timing/geometry**: exact checks, without tolerance fitting, automatic trimming, image rewriting or bbox normalization. The script does not reject edge contact by itself; an original edge-touching effect remains valid.

The checker performs no source-sheet gutter detection, character anatomy approval, emulator decoding or engine execution. Pair it with native decode proofs, source-sheet isolation review, the body measurement harness where applicable and actual-input renderer evidence.
