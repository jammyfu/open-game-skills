---
name: spine-skeletal
description: Choose between whole-figure skinning (small motion, no cut parts), layered parts and redrawn frames; bind and weight 2D characters, repair joint deformation, and verify fixed proportions, contacts, attachment swaps and gameplay-driven animation in Spine or equivalent mesh runtimes.
---

# Spine / 2D skeletal

Use authored layers with painted hidden surfaces, a fixed setup skeleton, weighted meshes and authored view/hand alternatives. A drawing of a skeleton is only a guide; it does not enforce pixel proportions. Confirm which editor/compiler/runtime is actually executable before promising a pipeline.

## Choose the mode before cutting anything

Splitting a character into separate part images is a cost, not a default: every cut adds seams, hidden-cap art and draw-order problems. Pick the lightest mode that the required motion allows.

| Mode | Use when | Source | Deformation |
|---|---|---|---|
| **Whole figure, small motion** | Idle breathing, sway, slight lean, small arm/leg swings, planted feet; the motion fits a declared amplitude budget | One approved full-character image. No cut parts, no painted hidden caps, no part inventory | One continuous mesh over the whole image, rigid cores for head/torso/each limb segment, local joint transitions, [skin-weights](../skin-weights/SKILL.md) |
| **Layered parts** | Large bends, limbs that cross or leave the torso silhouette, occlusion order that changes, hand/foot/face alternates | Complete element ledger, see [source-elements.md](references/source-elements.md) | Per part, local joint transitions |
| **Redraw frames** | The budget is exceeded, the view turns, the silhouette or contacts change, or a joint cannot bend naturally from the available art | Regenerate or draw each frame from the approved setup image, keeping head/body ratios, palette and foot anchors fixed; judge them as a sequence | None; the frames are the animation |

Whole-figure mode rules:

- **Declare the budget first** for each joint (maximum bend in degrees, maximum displacement in pixels) from the required poses. Verify it with a bend sweep on the actual mesh using the same fold audit and surface measure, and freeze it before looking at results.
- **The image must already show separable limbs.** Weights cannot tell overlapping pixels apart, so an arm pressed against the chest, a crossed leg or a fur cuff over a boot will drag its neighbour. Run the leak/island lint and look at those regions at full size; if they smear, that region is not eligible.
- **Rigid where the art cannot bend:** head and face, hands, feet and boots, hair, and any region whose drawing includes a painted cuff, collar or seam stay on one bone. Keep bone lengths and global scale fixed; never scale a body region to hide drift.
- **Contacts stay pinned.** Foot targets follow the native contact trajectory; unreachable targets mean the pose is out of budget.
- **Exceeding the budget switches mode.** Widening transitions until the fold audit passes trades folds for a rubbery limb. Move that action to layered parts or redraw frames and keep the failed whole-figure evidence.
- A technically clean sweep is still not visual acceptance. Review normal and slow playback, enlarged joints, the loop seam and light/dark alpha at the target runtime.

## Workflow

1. Pin the approved source views, setup joint observations, bone lengths, head dimensions, palette and action/contact references. Record units, density and uncertainty. Separate measured artwork landmarks from authored controls. Do not regenerate faces per pose or rescale individual frames to conceal drift.
2. *Layered-parts mode only:* prepare and review the complete required source-element inventory using [source-elements.md](references/source-elements.md): actual anatomical ownership, shared proportions, painted hidden caps, palette and near/far draw order. A common atlas or separate alpha islands does not prove correct parts. Then establish hierarchy and joint pivots before animation. Paint sufficient hidden overlap under sleeves and joints. Bind in setup pose. Keep head/body scale fixed unless the reference explicitly requires a deformation; disable accidental IK stretch.
3. For topology, weight envelopes, bends and corrective choices, read [weighting.md](references/weighting.md). [bind_joint.py](scripts/bind_joint.py) authors named two-bone bindings for a reviewed joint patch from setup world matrices and a declared anatomical envelope. It does not choose anatomy, pivots or envelopes for you. For whole-part weights (several bones, harmonic transitions, leak/seam lint, IK motion traces and rig-c export) use [skin-weights](../skin-weights/SKILL.md). Inspect actual artwork at the required extremes before producing the whole action set. No universal mesh density or elbow-width number applies to every character.
4. Export actual posed bone matrices and mesh vertices using the runtime that will play the asset. Run [audit_skin.py](scripts/audit_skin.py) using [the portable trace contract](references/audit-contract.md). It checks weights, source identity, lengths/scales, alpha-aware folds, time coverage, pinned contacts and loop closure. It does **not** approve anatomy or native motion fidelity.
5. Measure surface deformation with [measure_surface.py](scripts/measure_surface.py), using the same evaluated trace. Unit bone scales and zero folds do not prove preserved skin volume: a triangle may stretch twofold or nearly collapse without flipping. The diagnostic reports source-visible principal scales, signed area ratios and pixel-weighted tails; its output is `MEASURED-NOT-ACCEPTED`, never anatomy acceptance. Freeze reviewed bounds for each anatomical region/view before iteration. Review rigid cores separately from legitimate joint compression. Keep weight transitions local; paint hidden joint overlap or use corrective/alternate views when a single view cannot bend naturally. Do not spread weights over the entire limb merely to eliminate fold errors.
6. Review common-camera normal/slow playback, enlarged joints/face, light/dark alpha and the loop seam. For turnarounds or large foreshortening, key reviewed attachments and draw order; do not stretch one frontal drawing through every view. Recheck switch positions, palette and occlusion in the target renderer.
7. Preserve the game's clock, input, root physics and hitboxes. Animation displays the pose requested by gameplay. Hitstop pauses that actor's animation, not the render ticker. Blend changes must not create extra gameplay hit events. Track layout may use locomotion / attack / face-FX when the rig supports those overlays; it is a convention, not a requirement to layer every full-body attack.

## Tools and handoff

- [Public reference patterns](references/reference-patterns.md): source-inspected Spineboy rigid/mesh attachments, independent foot IK, DragonBones slot replacement, and why elastic-limb examples do not fit locked anatomy.
- [Native attachment ownership audit](scripts/audit_attachment_ownership.py): reject neighbouring paint in overlapping atlas rectangles, missing/duplicated visible pixels and stale sources using an authored ownership map. Run `python3 scripts/test_attachment_ownership.py`; a pixel-identical rectangle is intentionally a failing fixture. This does not approve anatomical ownership or transformed rendering.
- [Tool adapters](references/tool-adapters.md): official Spine/PixiJS, rig-c, version/licence boundaries, and truthful reporting of skipped parser checks.
- [Transfer and evidence](references/transfer.md): package layout for open-game-skills, project adapters and the Chu elbow failure case. Keep ROM/character images outside the portable skill.
- `scripts/requirements.txt` declares the audit's image dependencies. Run `python3 scripts/test_audit_skin.py` and `python3 scripts/test_bind_joint.py` after changing the harness or binding helper.

## Acceptance

Report format validity, measured geometry, visual review, native-reference timing and runtime integration separately. Missing evidence stays blocked. A technically green limb test never closes a full character. Required poses, contacts and attachment switches need explicit coverage; declared fallbacks are not newly completed art. Keep failed candidates and prior accepted assets, and never relax the lock merely to make a report green.
