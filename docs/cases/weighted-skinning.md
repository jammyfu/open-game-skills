# From a green build to a joint you can trust

[Live PixiJS comparison](https://jammyfu.github.io/open-game-skills/weighted-skinning/) · [Runnable case](../../examples/weighted-skinning/README.md) · [spine-skeletal](../../skills/2d/spine-skeletal/SKILL.md)

![Before and after the elbow envelope correction](../demos/weighted-skinning/preview.gif)

The trigger was repeated character-art drift in a fighting-game remake: changing head proportions, feet that bobbed, and joints that looked assembled. A real layered skeleton can hold geometry more reliably than independent redraw prompts, but it introduces a different failure mode: a numerically valid mesh can still fold visible artwork.

This example isolates that problem so another developer can reproduce it without the game, ROM or paid editor.

## The failure that a compiler accepted

A continuous arm was bound by name to an upper arm and forearm, with a wrist socket. Weights were normalized and the bones retained their lengths. The first envelope blended over a narrow strip near the elbow. Format/weight checks passed. At deep flexion, inner-joint triangles inverted through **2,529 visible source pixels**.

The repair broadened the fixed setup weight envelope, then reran the same angle sweep and source-alpha audit. Visible inverted pixels fell to **0**. Transparent-canvas triangles still invert; reports retain them. The alpha threshold was 32 for both candidates. No bone length, source image, action duration or acceptance tolerance changed to conceal the failure.

| Evidence | Narrow envelope | Revised envelope |
|---|---|---|
| Same source SHA256 / 703 vertices / 1,296 triangles | Yes | Yes |
| Compiler's format and normalized-weight checks | Pass | Pass |
| Actual evaluated samples | 121 | 121 |
| Visible source pixels in folded triangles | 2,529 | 0 |
| Portable skin audit | FAIL | PASS |
| Whole-character / gameplay acceptance | Not claimed | Not claimed |

## The reusable capability

`spine-skeletal` now owns a concrete loop: setup observations → fixed bones and named bindings → actual runtime exports → alpha-aware fold/length/scale/contact/loop checks → independent visual review. Its two-bone helper computes binding coordinates from setup matrices. Its portable Python audit needs ordinary JSON and images, rather than a proprietary runtime.

The Skill also covers hidden shoulder/hip surfaces, IK reach and knee poles, corrective meshes, large-angle attachment swaps and keeping gameplay clocks authoritative. These are workflow requirements; this limb case does not claim to exercise all of them.

The [HD sequence harness](../../skills/2d/hd-sprite-sequence/SKILL.md) complements this rig audit by checking independently observed head/body landmarks, source identity, contact trajectories, trim/import geometry and frame sequences. Neither tool can tell whether an annotator picked the correct jawline. Code-level gates and actual-image review work together.

## Reproduce and extend

```sh
python -m pip install -r requirements-dev.txt
python examples/weighted-skinning/run.py --out /tmp/weighted-skin-review
python -m unittest discover -s tests -v
```

For your own character, export your runtime's evaluated matrices/vertices under the [trace contract](../../skills/2d/spine-skeletal/references/audit-contract.md). Pin the identity/projection and thresholds before iteration. Review the source image, normal/slow loops, seams and the target engine. Use a different view or corrective art when two-bone deformation cannot represent the anatomy naturally.

The included live demo uses PixiJS and rig-c's own MIT core; it does not bundle the official Spine runtime. Official Spine editor/runtime use remains subject to its own licences. This is a recorded tool case, not an LLM benchmark or a completed character showcase.
