---
name: hd-sprite-sequence
description: Use when redrawing game sprites or independent effects in HD from native frames, or baking 2D pose sequences that must preserve identity, proportions, anchors and original timing, especially when frames resize, jitter or decode incorrectly.
---

# HD sprite sequence

Own **source-art identity and sequence consistency**. [Sprite catalog](../sprite-catalog/SKILL.md) owns inventory, [sprite-atlas](../sprite-atlas/SKILL.md) owns packing/import, and [pixel-animation](../pixel-animation/SKILL.md) owns gameplay-frame mapping. Do not change gameplay to accommodate art.

## Modes

| Mode | Deliverable |
|---|---|
| author | pinned character model, pose/landmark lock, constrained image generation, reviewed source frames |
| rig-bake | fixed approved parts, fixed bone lengths and offline PNG baking with no per-frame scaling or face regeneration |
| audit | executable measurements, overlays, fixed-scale playback and explicit failing frames |
| repair | revised source images for failed identity/anatomy frames, followed by the same immutable lock |

## Hard source-art contract

Before generation, pin the character model image, face/profile references, canonical anatomy measurements and per-pose projected landmarks in a hashed lock. Freeze head crown-to-chin, head width, brow-to-chin, cheek width, neck-to-pelvis, shoulder width and relevant limb lengths. A full-body humanoid audit also measures the arm/leg chains and deprojected head-to-body chain ratio; a face/torso-only audit must declare its narrower scope and cannot certify the whole character. Freeze ratios as well as absolute scale; matching one silhouette axis cannot establish correct head/body proportions. Use the project's approved model, not a universal number of heads.

The lock also specifies logical units, density, untrimmed canvas, pivot, expected contacts/sockets, pose order/duration, permitted perspective/occlusion and hard numerical tolerances. Projection exceptions must exist **before** generation and have pose evidence; never invent them to excuse a failed face. For an invisible face, explicitly scope the face check as occluded; head/body checks and the visible silhouette still apply.

Give the image tool the model, facial close-up and pose guides together. Generate an entire coherent action strip from one model, with root/contact/head guides and the exact frame count. Keep body and VFX on separate source layers. Lock hair mass, jaw, eye spacing, facial scale, limb lengths, outfit and camera magnification. Preserve transparency. A prompt is a constraint request, **not proof** that the model obeyed it. Use the installed image-generation capability; the bundled harness does not call a provider or grant API permission.

When a literal unchanged face is required, reuse approved head/face source parts per view through an existing layered/rigged sprite workflow; do not independently regenerate a face in every cell. If that workflow does not exist, preserve the chosen runtime architecture, constrain the redraw and reject drift rather than promising a prompt can freeze pixels.

Do not promote artwork because files exist, the atlas is complete, the longest body axis matches, or the game loads. Measure the **actual image** using independent reviewed landmarks; never copy expected coordinates into observations. Bind observations/reviews to image hashes. Re-read the pixels after every regeneration or resampling operation.

## Repair rules

- A trim/pivot/import error can be repaired in metadata while preserving the source coordinate system.
- A consistent camera/density mismatch can use one documented uniform transform for the action strip. Never stretch X/Y separately or normalize every frame to the same ink height.
- A changed face size, head/body ratio, limb length or costume shape is an **art failure**. Redraw the failed strip/frames using the same pinned model and pose guides. Whole-frame resizing cannot repair anatomical ratios.
- Grounded contacts and held sockets follow the authored reference trajectory. Do not bottom-align airborne, rotated or prone frames as if they were standing. Compare residual motion against the intended pose change, including the last-to-first loop transition.
- Keep the prior accepted art while a replacement is draft. Do not silently mix an unreviewed sequence into the shipping manifest. Never relabel a failed lock or relax tolerances merely to get green output.

## Skeleton and face control for continuous redraws

For a complete continuous-body redraw, use [the landmark control workflow](reference/landmark-control.md): pin bone lengths, declared projection, a head ellipse and facial feature layout on a common grid, then generate the **whole human figure** in each pose. A skeleton/face reference is a generation constraint request, not proof the pixels obey it; distinguish reference-guided generation from an actually configured conditioning model. Keep actual-image observations independent from control points.

If a cutout/rig attempt produces unnatural shoulders, elbows or knees and is rejected, stop repairing that route. Preserve it as rejected evidence and return to a complete coherent model plus native pose guides. Do not feed broken assembled anatomy back as the main drawing reference. When transparent reference edges carry colored contamination, the workflow may generate on an opaque neutral matte and remove only connected exterior background while preserving retained artwork pixels. Inspect the actual results before broad engine tests or promotion.

## Fixed-part baking

When hard pixel identity is required, follow [the fixed-part recipe](reference/locked-rig.md) and [bake_rig.py](scripts/bake_rig.py). It reuses one approved face/part image per view, permits only rigid joint rotations and translations, preserves source bone offsets and bakes ordinary PNGs without adding a game clock or changing the runtime architecture. Generate/review the master parts once through the available image tool; do not improvise a new face for every action. A bake remains `baked-not-accepted` until independent image, pose and temporal review passes the measurement harness.

## Harness and evidence

For ROM/native-reference reproduction and independent VFX, read [native-to-HD closure](reference/native-to-hd.md). Establish verified tile/palette/SAT decoding before generation, preserve contextual flips and native state timing, and verify the result with actual inputs. Use [validate_fx.py](scripts/validate_fx.py) and its [manifest contract](reference/fx-manifest.md) for independent effects; explicit silhouette/centroid/palette thresholds complement visual review and do not approve character anatomy. Validate transfer on a separately scoped second character before claiming a reusable end-to-end workflow.

Read [the measurement contract](reference/measurement-contract.md), then run [validate_sequence.py](scripts/validate_sequence.py) with a locked reference and separately authored observations. Install its [image dependency](scripts/requirements.txt) in the target environment. The harness validates decode/alpha/trim geometry, hash identity, projected anatomy, face/head ratios, absolute landmark errors and temporal residuals. It writes a report and common-scale overlays/playback. Missing measurements/reviews are blocked, numerical violations fail, and neither may pass the promotion gate.

Annotations are reviewed measurements, not an automatic face detector. The harness cannot prove the annotator put a point on the correct jaw or identify a face from coordinates. Inspect the paired images/landmark overlays, facial close-ups and slow/normal-speed playback; record reviewer/build/configuration and image/lock hashes. Review in the actual renderer at intended densities, both facings and relevant depth scales. Check alpha against light/dark backgrounds and preserve original input/timing/collision traces. Tool fixtures are not engine or human-playtest evidence.

## Acceptance

Every required pose and transition is accounted for; no missing or silently duplicated frame. Absolute face/head dimensions **and** anatomical ratios satisfy the pinned contract. Contacts, sockets and loop closure follow the reference within its published tolerance. Fixed-scale playback shows no unplanned growth, shrinking, foot sliding or face morphing. Failed or blocked frames remain draft; publish the report and per-frame reasons rather than claiming a whole game or character is fully validated.
