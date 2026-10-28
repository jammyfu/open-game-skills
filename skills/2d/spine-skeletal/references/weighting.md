# Weighted mesh decisions

## Bind and material preparation

Place the bone pivot on the drawn joint, with attachment offsets from it. Parent, hidden pivot and anatomical length are authored interpretations when the image cannot determine them; record that uncertainty. Freeze these decisions before fitting actions. Use explicit named bindings rather than raw bone indices when the tool supports them.

Layered animation needs artwork under occlusion: sleeve openings, shoulder caps, torso behind arms, the inner elbow, pelvis and knee overlaps. Extracting only visible fragments leaves holes on movement. Do not use an earlier broken assembled figure as the identity master. Source layers should share the approved palette, line weight and a declared setup density. Pin a head view as a rigid attachment; generate/review new views only when a turn needs them.

## Topology and weights

- Put edge loops where the silhouette or joint bends, with enough inner/outer joint resolution. More vertices alone cannot repair a wrong pivot or missing surface.
- Start rigid well away from the joint and blend within that joint's anatomical region. Keep unrelated arm/torso or adjacent-leg weights separate. Nearest-bone distance over a whole-body image can bind the wrong overlapping surface.
- Every vertex needs finite, nonnegative named weights summing to1 within a predeclared tolerance. Unknown bones, zero-influence vertices and duplicate bone entries need correction. Preserve each binding's setup local coordinates.
- Do not scale or shear the face, head or limb bones to fit a bad drawing. If foreshortening needs a different projection, author that view and keep its setup/projection contract explicit.

## Bend sweep before action production

For a reviewed two-bone joint patch, `scripts/bind_joint.py` accepts world-space setup vertices, two named setup affine matrices `[a,b,c,d,x,y]`, and an envelope with a world-space origin, nonzero axis and increasing start/end distances. It uses a smooth longitudinal transition, inverts each setup matrix for binding coordinates, and leaves vertices outside the transition rigid. The CLI writes candidate weights only. Partition the character into anatomically appropriate patches yourself; this helper is not a nearest-distance auto-rig or an anatomy validator. Use different topology, envelopes or correction mechanisms when a two-bone patch cannot represent the required bend naturally.

Sweep each joint through the actual required angles, including maximum flexion/extension, the native key poses and their transitions. Use one camera and one scale throughout; include source UVs, posed vertices, bones and time stamps. Inspect the silhouette, joint crease, volume, line art and overlap at full size, then at intended game size.

Linear blend skinning can invert inner-joint triangles despite normalized weights and fixed bones. A narrow weight transition can compress the inner elbow into a spike. Test topology and broaden or reshape the anatomical envelope where justified; then inspect whether the broader region itself becomes rubbery. If it still looks wrong, use an elbow corrective bone/deform key, revise the setup art, or switch to a reviewed large-angle attachment. Never hide the failure by turning off wireframes, shrinking the whole actor or raising the allowed error after seeing the result.

An alpha-aware fold audit intersects inverted source-UV triangles with the actual image alpha. It distinguishes transparent-canvas folds from folds in visible ink. Record the alpha threshold before comparing candidates; it is not a knob for hiding outlines. Near-zero triangles also need checking. This detects a necessary defect, not all defects: an intact triangle can still draw unnatural anatomy.

## Contacts, swaps and runtime

Foot IK targets follow the native contact trajectory, including intended sliding, airborne and prone phases. Do not bottom-align every pose. A locked foot and fixed bone lengths need a feasible reach and a stable knee pole; unreachable targets require corrected controls or a different authored pose, not automatic stretch. Verify actual shoe pixels in addition to the joint target.

When changing hand/view attachments, preserve the hand socket, projection, density and palette. Key slot draw order for occlusion rather than reparenting a limb during an action. Review before/at/after each switch; for native stepped artwork, retain intended holds rather than imposing smooth interpolation everywhere. Allow corrective deformation only where reviewed, and keep the independent head/body and contact checks.

Use native startup/active/recovery and hitstop ticks as the authority. Root movement remains in gameplay. Separate effect layers follow declared sockets and lifetimes; blending or attachment changes cannot alter collision or consume stored character state.
