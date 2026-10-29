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

A minimum area ratio near zero is a near-collapse that passed. Look at it, and prefer a corrective bone, an alternate drawing or a smaller motion range over widening forever.

## Passing the fold audit is not looking right

The fold audit and surface measures catch inversion and collapse. They do not catch a limb that bends like rubber. In the pelican case the knee swings 48°–114° and the ankle more than 100°:

| Leg configuration | Fold audit | Min area ratio (near leg) | Shin `softLengthFraction` |
|---|---|---|---|
| Foot inside the leg mesh, symmetric 30% insets (earlier draft) | PASS | 0.46 | shin visibly curved into the ankle |
| Foot as a rigid layer, symmetric 30% insets | PASS | 0.38 | 0.30 near, 0.30 far |
| Foot as a rigid layer, thigh `[0.1, 0.3]`, shin `[0.06, 0.0]` | PASS | 0.38 | 0.05 near, 0.10 far |

All three pass. Only the last keeps the thin shin straight; its bend sits in the feathered thigh end, which the knee cap covers. Two rules follow:

- Put the transition on the side that can hide or absorb it with asymmetric `coreInset`. Thin, hard segments (shins, forearms, beaks, weapons) stay rigid.
- A hinge that rotates far, like an ankle on a pedal or a wrist, is a separate rigid layer under a painted joint cap, not a mesh bend.

`pose_trace.py` reports `softLengthFraction` per bone so this is measured, not only eyeballed. There is no universal bound; freeze one per segment before iterating.

## Soft bodies, contact and loops

- **Ring bones.** A tyre or balloon is a ring mesh skinned to zero-length bones around its circumference. Each bone owns a disc-shaped rigid zone and the solver blends between them. Animate the bones with translate tracks only: push each one by how far its section of the ring would sink into the ground, bulge the sides and sink the crown. Keep any spinning art (spokes) in a separate rigid layer so the soft ring never has to rotate.
- **Chains.** A fish or tail is a bone chain with wide, symmetric transitions. Drive it with a travelling wave, `A_i sin(wt - i*phase)`, with amplitude growing toward the tip. Check `softLengthFraction`: soft is the goal here, so freeze a bound that matches intent rather than copying the limb values.
- **Loops with a scrolling world.** Make the scrolling content periodic in one tyre revolution so one period of scroll per second matches wheel rotation. Resets to zero at the loop point keep the trace's first and last samples identical for the loop audit. Solve any spring in the frequency domain (`irfft(rfft(x) * H)`) so periodic forcing gives an exactly periodic response.

## Evaluator and export scope

`pose_trace.py` implements translate/rotate FK, `inheritRotation: false` (rig-c/Spine `noRotationOrReflection`), and analytic two-bone IK with an explicit bend sign. No scale or shear tracks: bone scale is part of the identity lock. Its trace uses the spine-skeletal contract, so the same auditor judges this evaluator and real runtime exports.

`export_rigc.py` bakes the evaluated offsets to linear keys at the sample rate. rig-c then reproduces the evaluator at sample times; the two repository cases match within 2e-5 world units over 121 samples each with rig-c 2.79.0. Baked IK is not a live constraint, and the official Spine parser round trip is not run by this tool.
