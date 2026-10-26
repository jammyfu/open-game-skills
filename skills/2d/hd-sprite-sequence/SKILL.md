---
name: hd-sprite-sequence
description: Use when redrawing a game's sprites in HD or generating pose sequences that must keep the same face, head-to-body proportions, anatomical scale and anchors, especially when frames breathe, resize or jitter despite matching canvas bounds.
---

# HD sprite sequence

Own **source-art identity and sequence consistency**. [Sprite catalog](../sprite-catalog/SKILL.md) owns inventory, [sprite-atlas](../sprite-atlas/SKILL.md) owns packing/import, and [pixel-animation](../pixel-animation/SKILL.md) owns gameplay-frame mapping. Do not change gameplay to accommodate art.

## Modes

| Mode | Deliverable |
|---|---|
| author | pinned character model, pose/landmark lock, constrained image generation, reviewed source frames |
| audit | executable measurements, overlays, fixed-scale playback and explicit failing frames |
| repair | revised source images for failed identity/anatomy frames, followed by the same immutable lock |

## Hard source-art contract

Before generation, pin the character model image, face/profile references, canonical anatomy measurements and per-pose projected landmarks in a hashed lock. Freeze head crown-to-chin, head width, brow-to-chin, cheek width, neck-to-pelvis, shoulder width and relevant limb lengths. Freeze ratios as well as absolute scale; matching one silhouette axis cannot establish correct head/body proportions. Use the project's approved model, not a universal number of heads.

The lock also specifies logical units, density, untrimmed canvas, pivot, expected contacts/sockets, pose order/duration, permitted perspective/occlusion and hard numerical tolerances. Projection exceptions must exist **before** generation and have pose evidence; never invent them to excuse a failed face. For an invisible face, explicitly scope the face check as occluded; head/body checks and the visible silhouette still apply.

Give the image tool the model, facial close-up and pose guides together. Generate an entire coherent action strip from one model, with root/contact/head guides and the exact frame count. Keep body and VFX on separate source layers. Lock hair mass, jaw, eye spacing, facial scale, limb lengths, outfit and camera magnification. Preserve transparency. A prompt is a constraint request, **not proof** that the model obeyed it. Use the installed image-generation capability; the bundled harness does not call a provider or grant API permission.

Do not promote artwork because files exist, the atlas is complete, the longest body axis matches, or the game loads. Measure the **actual image** using independent reviewed landmarks; never copy expected coordinates into observations. Bind observations/reviews to image hashes. Re-read the pixels after every regeneration or resampling operation.

## Repair rules

- A trim/pivot/import error can be repaired in metadata while preserving the source coordinate system.
- A consistent camera/density mismatch can use one documented uniform transform for the action strip. Never stretch X/Y separately or normalize every frame to the same ink height.
- A changed face size, head/body ratio, limb length or costume shape is an **art failure**. Redraw the failed strip/frames using the same pinned model and pose guides. Whole-frame resizing cannot repair anatomical ratios.
- Grounded contacts and held sockets follow the authored reference trajectory. Do not bottom-align airborne, rotated or prone frames as if they were standing. Compare residual motion against the intended pose change, including the last-to-first loop transition.
- Keep the prior accepted art while a replacement is draft. Do not silently mix an unreviewed sequence into the shipping manifest. Never relabel a failed lock or relax tolerances merely to get green output.

## Harness and evidence

Read [the measurement contract](reference/measurement-contract.md), then run [validate_sequence.py](scripts/validate_sequence.py) with a locked reference and separately authored observations. Install its [image dependency](scripts/requirements.txt) in the target environment. The harness validates decode/alpha/trim geometry, hash identity, projected anatomy, face/head ratios, absolute landmark errors and temporal residuals. It writes a report and common-scale overlays/playback. Missing measurements/reviews are blocked, numerical violations fail, and neither may pass the promotion gate.

Annotations are reviewed measurements, not an automatic face detector. The harness cannot prove the annotator put a point on the correct jaw or identify a face from coordinates. Inspect the paired images/landmark overlays, facial close-ups and slow/normal-speed playback; record reviewer/build/configuration and image/lock hashes. Review in the actual renderer at intended densities, both facings and relevant depth scales. Check alpha against light/dark backgrounds and preserve original input/timing/collision traces. Tool fixtures are not engine or human-playtest evidence.

## Acceptance

Every required pose and transition is accounted for; no missing or silently duplicated frame. Absolute face/head dimensions **and** anatomical ratios satisfy the pinned contract. Contacts, sockets and loop closure follow the reference within its published tolerance. Fixed-scale playback shows no unplanned growth, shrinking, foot sliding or face morphing. Failed or blocked frames remain draft; publish the report and per-frame reasons rather than claiming a whole game or character is fully validated.
