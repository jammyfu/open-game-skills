---
name: skin-weights
description: Generate, lint and verify 2D skinning weights for layered skeletal characters — alpha-covering meshes, bounded harmonic weights between declared rigid bone cores, static leak/seam/stale-binding lint, reference FK/IK/LBS traces for the spine-skeletal audit, fixed-camera review renders and rig-c/Spine export with round-trip verification.
---

# Skin weights

Use this when a 2D character (layered parts, or one whole approved image for small motion) needs weighted meshes: auto-weighting a part, diagnosing a fold, leak or rubbery joint, or proving that weights survive the actual motion. It owns the weight field and its evidence. Hierarchy, pivots, art readiness, runtime integration and final acceptance stay with [spine-skeletal](../spine-skeletal/SKILL.md), which this skill feeds.

Weights are a design decision, not a solver output. The solver interpolates *between* rigid regions you declare; it cannot know where a joint should bend, what is hidden under a sleeve, or that a beak must stay rigid.

## Workflow

1. **Freeze inputs first.** Approved layered art with painted joint overlap, setup bones on the drawn pivots, and a written rig (`ogs.skin-rig/1`, see [formats](references/formats.md)). Pick the review alpha threshold and any lint bounds now; never loosen them after seeing a result. One part = one attachment with one outline. A head, beak, fist or prop is a single-bone (rigid) part.
2. **Mesh:** `python3 scripts/build_mesh.py rig.json --out mesh.json`. Covers every visible pixel, fills enclosed holes, writes the outline first (Spine/rig-c hull rule). Rigid backdrops with separate islands use `mesh.mode: "quad"`. Choose spacing so a joint's transition gap spans at least three to four cells.
3. **Solve:** `python3 scripts/solve_weights.py rig.json mesh.json --out weights.json`. Per influence bone declare `handleRadius` (half the limb width at that bone) and `coreInset` (fraction of the bone kept free at each end). Transition width at a joint ≈ the gap between neighbouring cores. Read [method](references/method.md) before tuning.
4. **Lint:** `python3 scripts/lint_weights.py rig.json mesh.json weights.json`. FAIL on stale hashes or bindings, normalization, foreign bones, influence count, detached influence islands (leakage) and rigid zones closer than `minTransition` (seam). PASS here is necessary, never sufficient.
5. **Deform with the real motion:** `python3 scripts/pose_trace.py rig.json mesh.json weights.json motion.json --out trace.json --report pose.json`, then the spine-skeletal [audit](../spine-skeletal/scripts/audit_skin.py) and [surface measure](../spine-skeletal/scripts/measure_surface.py) on that trace. Include the extremes of every joint (contacts, IK reach, max flexion). Unreachable IK and follow-contact gaps are failures, not things to stretch away.
6. **Look at it:** `python3 scripts/render_skin.py trace.json --sheet sheet.png --gif loop.gif --scale 4 [--wire] [--weights] [--rings] [--heat BONE] [--bones] [--constraints] [--view=x0,y0,x1,y1]`. One fixed camera for all frames (pass `--view` when a scrolling backdrop would stretch the fitted camera; use the `=` form for negative numbers), bilinear and supersampled; folded triangles are painted red (`--rings` circles them), `--weights` tints each part by bone like Spine's weights view, and `--bones --constraints [--fade 0.5]` draws the skeleton with its IK chains and targets over the art. Check the inner joint crease, outline continuity and rigid parts at full and game size.
7. **Export when it holds:** `python3 scripts/export_rigc.py rig.json mesh.json weights.json --motion motion.json --out build/` writes rig-c specs (y-up). With `--verify-rigc <rig-c package> --bun <bun>` it compiles with that rig-c, poses with rig-c's own core and compares every vertex. The official Spine editor/parser round trip remains `not-run` unless you run it.

## Whole-figure mode (small motion, no cut parts)

For small-amplitude motion the figure does not have to be split. Declare **one part that is the whole approved image** (no hidden-cap art, no element inventory) and give its mesh the whole skeleton: head and torso as rigid cores, each limb segment a bone with its own `handleRadius`/`coreInset`, joints as the only transitions. Because nothing is cut, there is no seam at the elbow, knee or sleeve.

- Set the amplitude budget per joint before solving (see [spine-skeletal](../spine-skeletal/SKILL.md) mode table) and run the bend sweep to those angles on the real mesh. Stay inside the budget; do not widen bands to rescue a larger action.
- Keep head, face, hands, boots, hair and painted cuffs on one bone each (rigid cores with generous `handleRadius`). Small arm and leg swings use per-bone insets so the transition sits at the joint, not along the limb.
- Lint's influence-island and `minTransition` checks are the leak guard. If a limb pixel region touches the torso or the other leg in the image, check it at full size: harmonic weights cannot separate overlapping paint, so that region limits the amplitude.
- The pose report's `softLengthFraction`, the fold audit and the surface measures must be reported at the budget extremes. A failed extreme means the action belongs to layered parts or redrawn frames, not to bigger weights.

## Fixing failures

| Evidence | Likely cause | Change |
|---|---|---|
| Visible fold at the inner joint | Transition too narrow for the bend angle | Raise `coreInset` on the side the band is short; refine mesh; then corrective bone or alternate drawing for extreme angles |
| Result flips between mesh spacings | Marginal transition | Keep widening until it passes at two spacings |
| Lint seam (rigid zones too close) | `handleRadius` sweeps sideways into the neighbour, typical at short bones (foot, head) | Per-bone radius/inset; never cover it with a larger tolerance |
| Detached influence island | A bone reaches a second region (other limb, across a gap) | Split the part, restrict `bones`, or fix the handle |
| Area ratio near 0 or P95 stretch high without folds | LBS volume loss / rubbery band | Narrower band or corrective/alternate art; widening further trades folds for rubber |
| Thin limb visibly curves (high `softLengthFraction` in the pose report) | Symmetric insets spread the bend into the thin segment | Asymmetric `coreInset: [head, tail]` so the bend sits in the soft/covered side; hinge joints that rotate far (ankle, wrist) become a separate rigid layer under a painted joint cap |
| Stale bind drift | Setup pose edited after binding | Re-solve; do not hand-edit local coordinates |

The narrow-vs-wide trade-off is real: a band that is too narrow folds, one that is too wide makes the limb rubbery. Report both the fold audit and the surface measures.

## Acceptance

Report separately: lint, pose report (IK/contacts), audit `technicalStatus`, surface measures, visual review, export verification and runtime integration. A reference-evaluator trace is tool evidence; the shipping runtime still owes its own exported trace. `characterAccepted` stays false here. Keep failed candidates and their reports. Soft bodies are ordinary weighted parts: a tyre is a ring skinned to zero-length bones that the motion pushes, a fish is a four-bone chain with wide transitions. Worked cases in the source repository (not installed with the pack): `examples/pelican-bicycle/run.py` and `examples/weighted-skinning/harmonic_case.py`. Run `python3 scripts/test_skin_weights.py` after changing any script.
