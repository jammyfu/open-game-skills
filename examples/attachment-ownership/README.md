# Catch neighbouring paint before binding

This anonymous fixture reproduces a real source-atlas failure: two separate pieces have overlapping bounding rectangles. Copying a rectangle preserves every original pixel but includes part of its neighbour.

```sh
python -m pip install -r requirements-dev.txt
python examples/attachment-ownership/run.py --out /tmp/attachment-ownership
python skills/2d/spine-skeletal/scripts/audit_attachment_ownership.py /tmp/attachment-ownership/owned-contract.json
```

The runner asserts both outcomes and writes PNG fixtures, pinned contracts, JSON reports and `preview.svg`:

| Check | Raw rectangle | Declared owner export |
| --- | --- | --- |
| Matches pixels in its source rectangle | Yes | Foreign paint excluded |
| Foreign visible pixels in export A | 3 | 0 |
| Duplicated visible source pixels across exports | 3 | 0 |
| Native ownership audit | FAIL | PASS-NATIVE-OWNERSHIP |
| Anatomy, transformed seams, gameplay | Not evaluated | Not evaluated |

The intentionally bad audit exits2 when called directly. The runner exits0 only when it reproduces that rejection and the correct native export passes. Inputs are tiny mathematical fixtures; no game, ROM, editor, model API or private character art is needed.

For real sources, author and review the integer owner-ID image independently. Keep source views, proportions, hidden caps, front/back surfaces and target-renderer review in the [source preparation workflow](../../skills/2d/spine-skeletal/references/source-elements.md). An incorrect semantic map can still be numerically consistent.
