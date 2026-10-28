# Prepare source elements before binding

This ledger applies to the **layered-parts** mode. Small-amplitude motion can skip it entirely by skinning one approved whole-figure image (see the mode table in [SKILL.md](../SKILL.md)); choose parts only when the required motion needs them.

A valid atlas, correct part count and separate alpha islands do not establish correct anatomical decomposition. A cell named `forearm` may still contain an upper arm and a bent elbow. Binding that cell as one forearm duplicates the joint and carries the wrong silhouette into every action. Check the actual artwork before tuning weights.

## Source readiness ledger

Keep the approved model immutable, with its hash, setup density, visible feature observations and authored joint controls recorded separately. A generated assembled figure on the sheet is a comparison candidate; it cannot silently replace that approved model.

List every required source element and alternate view. For each, record:

- **Ownership and identity:** which anatomical segment or accessory it contains; near/far relative to the approved setup, independent of its atlas cell location. Check hand/thumb orientation and front/back hair or collar ownership.
- **Complete contour:** a complete intended element with painted hidden caps, rather than a visible fragment or a second limb accidentally included in the cut. Do not automatically split every continuous weighted limb: use the decomposition appropriate to the chosen rig, and document it.
- **Shared proportions:** observed feature spans, declared units and setup density. Outer bounding boxes include hidden caps and cannot stand in for anatomical length. Record uncertain cap centers as authored interpretations, not measured bone truth.
- **Overlap and draw order:** the surfaces needed behind sleeves, wrists, hips, knees and fur cuffs; the intended front/back order at bends and attachment changes. Closed source contours alone do not prove sufficient overlap.
- **Material consistency:** same-reference skin/fabric palette, line weight and alpha on light/dark backgrounds. Regional color medians may reveal drift but differing shadow populations prevent treating them as palette acceptance.
- **Evidence:** source hashes, independent observations, enlarged common-scale comparison, reviewer and unresolved issues. Keep generated guides/prompts separate from actual output measurements.

When complete preparation is the chosen workflow, finish this ledger for all required elements before binding. An incomplete source inventory is a preparation task, not an excuse to broaden weights over invalid art. File count, cap-distance fits and green geometry reports do not grant source acceptance.

## One shared master, explicit registration

A common sheet is useful for identity and color review but does not enforce scale. Retain an editable master and a fixed setup-density contract. A static uniform source transform can correct an evidenced camera/density mismatch. It cannot repair changed facial ratios, wrong wrist orientation or mismatched muscle contours. Keep those residuals visible; do not hide them with anisotropic scaling, shear or per-frame fitting.

Inspect alpha ownership before extracting. Disjoint parts can have overlapping bounding rectangles, so a rectangular crop may sample an adjacent limb. Preserve visible detached details; ambiguous ownership must stop extraction for review. Antialias expansion must not merge neighbors across a narrow gap. Report any discarded low-alpha residue and the threshold used.

Use [audit_attachment_ownership.py](../scripts/audit_attachment_ownership.py) for exported native paint. Its `ogs.attachment-ownership/1` contract pins an RGBA atlas and same-size integer owner-ID PNG, with each named part's positive `ownerId`, native `[x0,y0,x1,y1]` bounds and pinned exported image. All paths are relative to the contract package; each file entry has `path` and `sha256`. `alphaThreshold` defaults to32. The auditor requires exact premultiplied source paint on the declared owner, no exported alpha from other owners, and exactly one export of every source pixel above the threshold. It reports omitted lower-alpha material separately. `PASS-NATIVE-OWNERSHIP` is not art or runtime acceptance; the authored map still needs anatomical review.

Test the rejected extraction too. Comparing an exported rectangle with the same original rectangle can pass while including a neighbouring fur piece. A synthetic fixture with separate L-shaped parts and overlapping bounds proves that failure: the raw rectangle is pixel-identical but duplicates foreign paint. Also inspect the complete posed assembly: an isolated native crop can hide a small foreign fragment that becomes obvious after rotation and layering.

One semantic part can require multiple rendering surfaces. A shirt may need an interior layer behind the upper arm and a front layer above it, while the near forearm is in front of the shirt. Record sublayer ownership and paint order explicitly instead of forcing one global slot order. Native source recomposition can be exact while transformed filtering creates seams; verify source details and actual renderer output independently before adoption.

Inspect suspicious edge RGB together with its alpha and an actual light/dark composite. Saturated RGB at alpha1/255 is not equivalent to an opaque colored outline. Preserve the raw source, quantify visible contribution and avoid unnecessary generative repainting based on an uncomposited preview. A cleanup prompt does not guarantee an identical canvas or unchanged interior.

Verify every exported piece is nonempty and matches its intended source pixels. Some SVG renderers reject parent-directory image references without making the export command fail. For setup registration, declare the matrix convention and verify transformed observed points against target controls in the actual SVG/runtime convention; row-vector and column-vector matrices are transposes of each other. Successful export and zero length residual alone do not prove correctly placed artwork.

For a targeted shared-master repair, preserve unrelated reviewed elements and the approved reference. Record which source layers changed and compare actual non-target composited pixels; a generative edit request does not prove that only the requested layers changed. Keep old failed parts and provenance. Recheck the new element's physical dimensions, source view, caps and material independently before binding.

## Review the repaired source

Show the approved reference and repaired element at one physical scale, with observed feature markers and authored controls clearly distinguished. Include the full contour and enlarged joint/face detail without clipping. A two-point cap registration can align a segment exactly while its width, palette or anatomy remains wrong. Label it as registered, not accepted.

Only then bind the fixed setup skeleton and local weights. Continue with actual runtime bend sweeps, surface strain, contact pixels, view/draw-order switches and complete action coverage. Source readiness and runtime acceptance are separate gates.
