---
name: spine-skeletal
description: Bind and weight layered 2D characters, repair joint deformation, and verify fixed proportions, contacts, attachment swaps and gameplay-driven animation in Spine or equivalent mesh runtimes.
---

# Spine / 2D skeletal

Use authored layers with painted hidden surfaces, a fixed setup skeleton, weighted meshes and authored view/hand alternatives. A drawing of a skeleton is only a guide; it does not enforce pixel proportions. Confirm which editor/compiler/runtime is actually executable before promising a pipeline.

## Workflow

1. Pin the approved source views, setup joint observations, bone lengths, head dimensions, palette and action/contact references. Record units, density and uncertainty. Separate measured artwork landmarks from authored controls. Do not regenerate faces per pose or rescale individual frames to conceal drift.
2. Establish hierarchy and joint pivots before animation. Paint sufficient hidden overlap under sleeves and joints. Bind in setup pose. Keep head/body scale fixed unless the reference explicitly requires a deformation; disable accidental IK stretch.
3. For topology, weight envelopes, bends and corrective choices, read [weighting.md](references/weighting.md). [bind_joint.py](scripts/bind_joint.py) authors named two-bone bindings for a reviewed joint patch from setup world matrices and a declared anatomical envelope. It does not choose anatomy, pivots or envelopes for you. Inspect actual artwork at the required extremes before producing the whole action set. No universal mesh density or elbow-width number applies to every character.
4. Export actual posed bone matrices and mesh vertices using the runtime that will play the asset. Run [audit_skin.py](scripts/audit_skin.py) using [the portable trace contract](references/audit-contract.md). It checks weights, source identity, lengths/scales, alpha-aware folds, time coverage, pinned contacts and loop closure. It does **not** approve anatomy or native motion fidelity.
5. Review common-camera normal/slow playback, enlarged joints/face, light/dark alpha and the loop seam. For turnarounds or large foreshortening, key reviewed attachments and draw order; do not stretch one frontal drawing through every view. Recheck switch positions, palette and occlusion in the target renderer.
6. Preserve the game's clock, input, root physics and hitboxes. Animation displays the pose requested by gameplay. Hitstop pauses that actor's animation, not the render ticker. Blend changes must not create extra gameplay hit events. Track layout may use locomotion / attack / face-FX when the rig supports those overlays; it is a convention, not a requirement to layer every full-body attack.

## Tools and handoff

- [Tool adapters](references/tool-adapters.md): official Spine/PixiJS, rig-c, version/licence boundaries, and truthful reporting of skipped parser checks.
- [Transfer and evidence](references/transfer.md): package layout for open-game-skills, project adapters and the Chu elbow failure case. Keep ROM/character images outside the portable skill.
- `scripts/requirements.txt` declares the audit's image dependencies. Run `python3 scripts/test_audit_skin.py` and `python3 scripts/test_bind_joint.py` after changing the harness or binding helper.

## Acceptance

Report format validity, measured geometry, visual review, native-reference timing and runtime integration separately. Missing evidence stays blocked. A technically green limb test never closes a full character. Required poses, contacts and attachment switches need explicit coverage; declared fallbacks are not newly completed art. Keep failed candidates and prior accepted assets, and never relax the lock merely to make a report green.
