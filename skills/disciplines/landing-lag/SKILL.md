---
name: landing-lag
description: Use when airborne moves or traversal states need an explicit landing recovery, landing-cancel, or no-lag policy tied to the logical floor-contact event.
---

# Landing lag

Choose: `shared-lag` | `per-move-lag` | `cancel-on-land` | `none`.

Landing lag is authored recovery on the combat/action clock. The move/state data decides how much lag applies; do not assume an empty hop is always shorter, or a connected aerial always longer.

Floor contact comes from the collision/movement owner. On the published landing tick, resolve the air→land transition, any legal landing-cancel edge and recovery state in a deterministic order. Coyote time affects jump eligibility and does not erase landing recovery unless the project explicitly links those mechanics.

## Accept

Log the floor-contact tick, source airborne state, selected landing rule, first legal action tick and any cancel edge. Test whiff, hit, blocked aerial, empty jump, moving platform and same-tick contact/landing boundaries. Render FPS does not change the recovery count.
