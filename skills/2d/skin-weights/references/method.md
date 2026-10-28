# Method and limits

## Bounded harmonic weights between declared rigid cores

For each part with several influence bones the solver:

1. Computes each bone's setup segment and its **core**: the segment with `coreInset × length` removed from both ends. Zero-length bones use a disc.
2. Pins every vertex within `handleRadius` of a core, measured perpendicular to the bone (a slab without end caps), rigidly to that bone. Vertices claimed by two slabs are left free, so neighbouring rigid zones never touch directly.
3. Solves the Laplace equation per bone with those Dirichlet values on the part's own triangle connectivity. Edge weights are cotangent weights clamped to a small positive floor.

Clamping keeps the system an M-matrix, so the discrete maximum principle holds: weights stay in [0,1] and sum to one before pruning (the solver reports both). Because the solve follows mesh connectivity, influence cannot cross transparent gaps between islands. A heat or Euclidean nearest-bone scheme can; that is the leakage lint's job to catch when weights come from elsewhere.

Then the solver prunes weights below `pruneBelow`, keeps at most `maxInfluences`, renormalizes and writes named bindings with setup-local coordinates.

This follows the harmonic-coordinates family used for automatic skinning (heat diffusion in Baran & Popović's Pinocchio, bounded biharmonic weights of Jacobson et al.). Biharmonic weights are smoother at handles but need a constrained QP to stay bounded. Harmonic weights with an M-matrix are bounded by construction and need only numpy. Spine's own Auto weights is also topology-based and is documented as a starting point to smooth and prune ([Spine weights](https://esotericsoftware.com/spine-weights)).

## Why rigid cores are declared, not inferred

Where a limb is rigid and where it bends depends on anatomy and on what the art hides at the joint. Distance from the image alone cannot know that. The declared core turns that decision into two readable numbers per bone, and lint checks that the declaration stays coherent.

## Linear blend skinning limits

The evaluator and most 2D runtimes use linear blend skinning. LBS shrinks the inner side of a strongly bent joint. With a transition too narrow for the angle, triangles invert and fold visible ink. Widening the transition prevents inversion but spreads compression and stretch over a longer, rubbery band. Measured examples in this repository:

| Case | Narrow band | Chosen band |
|---|---|---|
| Arm, 0→90° elbow, spacing 36 px | inset 0.30: FAIL, 367 visible fold px | inset 0.45: PASS |
| Arm, same, spacing 24 px | inset 0.40: FAIL, 72 px | inset 0.45: PASS |
| Pelican knee, 36–113° pedalling | inset 0.22: FAIL, 1 px | inset 0.30: PASS, min area ratio 0.04 |

A minimum area ratio near zero is a near-collapse that passed. Look at it, and prefer a corrective bone, an alternate drawing or a smaller motion range over widening forever.

## Evaluator and export scope

`pose_trace.py` implements translate/rotate FK, `inheritRotation: false` (rig-c/Spine `noRotationOrReflection`), and analytic two-bone IK with an explicit bend sign. No scale or shear tracks: bone scale is part of the identity lock. Its trace uses the spine-skeletal contract, so the same auditor judges this evaluator and real runtime exports.

`export_rigc.py` bakes the evaluated offsets to linear keys at the sample rate. rig-c then reproduces the evaluator at sample times; the two repository cases match within 2e-5 world units over 121 samples each with rig-c 2.79.0. Baked IK is not a live constraint, and the official Spine parser round trip is not run by this tool.
