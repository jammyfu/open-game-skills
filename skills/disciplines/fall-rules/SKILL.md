---
name: fall-rules
description: Use when falling or entering a recovery region needs a project-defined cost function, stable fall event identity, surface/mount/water overrides and deterministic handoff to landing/recovery systems.
---

# Fall rules

Ask: `no-damage | meter-tax | lethal-drop`.

## Ownership

This skill resolves fall cost/recovery intent. `landing-lag` owns landing recovery timing; hazards or recovery volumes may provide a recovery source; water/mount/vehicle systems provide override state.

## Contract

Each fall resolution records:
- stable `fall_event_id`
- start/end height or project fall metric
- landing/recovery surface ID/type
- active override IDs
- selected cost rule/version
- authoritative result

Height thresholds, curves and whether a lethal boundary must be visually obvious are project/accessibility design choices, not universal constants.

Define override priority explicitly: for example water, glide, mount, scripted recovery, hazard or normal landing according to project data. The same fall event commits at most once.

## Runtime rules

1. Pause, streaming or replay cannot duplicate a committed fall result.
2. Teleports or scripted position changes are labeled and do not masquerade as a natural fall.
3. Long-fall recovery timing delegates to `landing-lag`; this skill does not invent a second recovery clock.
4. Cost changes across patches are versioned for replay/save evidence when relevant.

## Acceptance

Given one fall event, rule version and override state, resolution is deterministic and applied once. Evidence names the source metric, surface and override that produced the resulting cost or recovery, rather than relying on visible cliff art alone.
