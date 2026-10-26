# Measurement contract v1

The utility is an offline **asset harness**, not a game loop or automatic anatomy detector. Coordinates come from reviewed image annotations or a validated landmark detector followed by visual review. Annotating an expected point at an arbitrary location does not prove the image has that anatomy.

Run:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/validate_sequence.py --root /path/to/art --lock identity-lock.json --observations observations.json --out /path/to/review
```

Paths in the documents resolve beneath `--root`; images and lock inputs are read-only. The output directory must be separate from source inputs. Exit 0 means all declared checks pass, 1 means a measured failure, 2 means malformed/missing evidence or blocked checks. Review the report, not just the exit code. Finite positive values and unique frame/clip IDs are required.

## Locked reference

`schema` is `ogs.hd-sprite-lock/1`. Required fields:

- `model`: `image`, `sha256`, `reviewer`, and `review` equal to `approved`, `density`, and measured `landmarks` on the actual model PNG in physical pixels. Canonical lengths must agree with these model measurements. This image fixes identity. It may be a neutral/model sheet with face close-ups, not a screen containing several differently sized characters.
- `limits`: `length_rel`, `ratio_rel`, `position_px`, `delta_px`. These are project tolerances frozen before generation; strict examples are 0.025, 0.025, 0.5, 0.5. Their units are logical pixels except relative errors.
- `canvas`: `width`, `height`, `pivot` as `[x,y]` in untrimmed logical coordinates; one character scale across its source sequence.
- `segments`: named pairs of anatomical landmark names. Required measurement names are `head_height`, `head_width`, `face_width`, `face_height`, `torso`, `shoulders`; add limb segments relevant to the actions.
- `lengths`: canonical projected-neutral lengths keyed by every segment name. These define the model's head/body proportions, not an alpha bounding box.
- `ratios`: named pairs of segment names, including face/head and head/torso relationships.
- `frames`: keyed by required stable pose ID. Each contains `landmarks` in local actor/world logical pixels, `projection` factors keyed by segment, `occluded` landmark-to-reason map, `view`, and `reference_evidence` as `{ "path": "pose-or-rig-file", "sha256": "..." }`. The latter pins the actual source pose/rig bytes. A factor is finite, greater than zero and at most one; it represents foreshortening, not a per-frame camera zoom. Occlusion is a predeclared exception, not an empty point assigned zero length. Face checks alone may be occluded for authored back views; an unobservable body remains blocked.
- `logical_tick_hz`: the existing project clock frequency, explicitly supplied; the harness never invents a default gameplay clock.
- `clips`: keyed by action ID, each with positive integer `ticks` paired with each item of `frames`, boolean `loop`, and a nonempty `track` list of contact/socket/root landmarks whose residual motion is checked. Include every shipped transition, including cross-action edges as a clip when needed.

Reference landmark segment lengths themselves must agree with canonical lengths times projection within `length_rel`. This catches a reference that silently enlarges a head midway through a loop. Ratios use **deprojected** lengths, so a crouch does not change anatomical lengths. A severe foreshortening with no measurable endpoint cannot be rescued by setting the factor to zero: use an appropriate approved view or keep that check blocked.

## Independent observations

`schema` is `ogs.hd-sprite-observations/1`; `lock_sha256` binds the exact lock bytes. `build` identifies the generated/exported art version. `frames` keys must match the lock exactly. Each frame has:

- `image`, `sha256`, `density` (finite positive pixels per logical pixel).
- `source_size` equal to the locked logical canvas and `pivot` equal to its pivot.
- `trim_offset` in untrimmed logical coordinates; the PNG physical dimensions divided by density plus the trim offset must fit the source canvas. No per-axis scale.
- `landmarks` measured on **actual trimmed PNG physical pixels**. Conversion to local coordinates is `point / density + trim_offset - pivot`. Do not annotate intended coordinates without checking pixels.
- `review`: `image_sha256`, nonempty `reviewer`, and booleans `identity`, `pose`, `alpha`, `temporal`. These record manual/tool-assisted review; the tool validates binding/completeness, not reviewer authenticity.

Alpha must be genuinely transparent with a transparent border. Effects do not define anatomy; keep their pixels separate from the body art/measurements. An alpha box or maximum width/height can diagnose clipping but cannot validate faces or head/body ratios.

## Output and promotion

`report.json` includes input identities, scope, status, per-frame measurements, codes, missing evidence, temporal edges and the first violation. Its `artifacts` list binds only the current run's output image hashes; files left from an older run are not current evidence. `overlay.png` uses one density, canvas and origin for all cells; it never fits each pose separately. `clip-*.gif` follows authored ticks for inspection only; the game's simulation remains authoritative. Expected landmarks are cyan, observed landmarks red, and the actor origin is a crosshair.

Promotion requires both measured pass and the hash-bound visual reviews for **every** frame. Missing/changed image bytes, missing face points, mismatched canvas, even a small ratio violation, root/socket jitter, and a bad loop join each block promotion independently. If a source face is distorted, produce new pixels; do not change the lock or fabricate annotations. The report does not prove in-engine texture import, gameplay equivalence or correct human annotation semantics.
