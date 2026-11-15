# Applying evidence-led review to the generated tree

Review ID: `foliage-review-01`. Baseline: commit `bdc6fcd`, normalized GPT source and committed Pillow outputs. Driver: code/record inspection by the editing agent; no independent reviewer or human playtest. This is an asset-presentation review, not a gameplay slice. Process: [design review](../../skills/references/design-review.md).

## Findings

| Observation and evidence | Interpretation | Bounded action | Acceptance and status |
|---|---|---|---|
| `gpt-report.json` reports zero root changes, exact rest reconstruction and restored calm | The renderer satisfies these image-level invariants | Preserve these checks while changing motion | Functional, Pillow-level assertions: pass in the recorded run |
| `inside.png` is a static copy of the complete leaf silhouette; compositor starts with it | Zero holes within the original silhouette is partly guaranteed by construction; it does not prove believable exposed branches | Retain conservative fill, disclose its limitation; inspect edges at peak displacement before claiming art acceptance | Disclosure present; artistic edge acceptance not-run |
| Script assigns nine groups by distance from manually authored centers | The result is source-specific; it does not establish general semantic leaf segmentation | Keep the editable centers and palette constraint with the source | Source-specific layer export exists; arbitrary-art segmentation not-run |
| `gpt-debug.gif` and `gpt-trace.json` cover one tree and one gust | Evidence supports a single-tree response only | Use a two-tree camera-independent scene if a shared world-wind claim is needed | Multi-tree engine test not-run |
| `gpt-depth.png` uses a constant sky color | A useful static color comparison does not validate scrolling sky-row lookup | Add cropped/gradient-sky mapping only when a runtime needs it | Live parallax and Godot integration not-run |

No extra effect is necessary to satisfy the existing fixed-root tree demonstration. Falling leaves, fabric and multi-source wind remain separate proposals rather than silently expanding the acceptance claim.

## Decision ledger

- Keep stepped leaf poses: they are the declared style and are covered by numerical pose-hold checks. Smooth interpolation would require a separate style decision.
- Keep the thick trunk fixed: this matches the chosen oak treatment. Thin-pine trunk bending does not belong in this asset's acceptance criteria.
- Reject “zero holes proves production readiness”: the static interior and source-specific partition leave visual and integration questions unresolved.
- Defer a Godot pass until there is an actual Godot scene. A headless numerical test cannot replace it.

The source-inspired workflow is demonstrated by these concrete findings and decisions. It does not imply that the external summary, its original videos, or this review establish how players will perceive the finished game.
