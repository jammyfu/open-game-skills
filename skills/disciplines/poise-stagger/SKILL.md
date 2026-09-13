---
name: poise-stagger
description: Use when a persistent poise/stagger meter must accumulate impact, refill or reset, and transition into a stagger reaction at a defined threshold.
---

# Poise stagger

This skill owns the **poise pool**. `hyper-armor` owns move-local reaction immunity; `hitstun-recover` owns the stagger action lock after the pool breaks.

Choose: `hidden-bar` | `visible-bar` | `none`.

Publish maximum poise, per-hit poise damage, modifiers, refill delay/rate or reset events, and the exact break threshold. Define whether attacks during hyper-armor still damage poise; do not derive that behavior implicitly from visuals.

When the pool crosses the break threshold, emit one stagger transition with a stable event identity. Additional same-tick contacts must not trigger duplicate stagger rewards/effects unless explicitly authored. Throws or special classes bypass/affect poise only when published.

## Accept

Log poise before/after each contact and the single break event. Test exact-threshold, overkill, multiple same-tick hits, refill boundary, reset and interaction with an armored move. Hidden versus visible presentation must not change the numeric result.
