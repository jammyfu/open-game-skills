---
name: fighting-design
description: Use when a versus or arena fighter needs explicit neutral, space, round/win, roster-resource and interaction grammar while timing, combos, hit resolution and netcode remain delegated to their specialist owners.
---

# Fighting design

This skill owns **match/interaction grammar**, not the low-level combat clock.

## Compatible columns

`grounded-footsies` | `air-dash` | `tag-assist` | `platform-fighter`

Use these as project directions, not franchise implementations.

## Contract

Publish the applicable arena/space model, movement/resource affordances, round/stock/KO/blast/win rules, guard/throw/projectile or other interaction classes, roster/team/tag rules, stage/hazard policy and comeback/resource constraints.

## Ownership

- `action-feel`: logical combat clock, hitstop/cancel processing and move commitment.
- `combo-design`: route graph.
- `hitbox-hurtbox`, `throw-tech`, `parry-guard`, etc.: contact/defense mechanics.
- `netcode-feel`: prediction/rollback/delay/correction. This skill does not prescribe a networking architecture.
- `super-meter` / other resource owners: resource transactions.

## Rules

1. “Neutral,” pressure, defense and comeback tools are described through observable project rules; no universal throw/projectile/block triangle is required.
2. Character identity is gameplay affordance/data selected by the project, not copied named-character movelists.
3. Stage collision/hazards follow their owners; platform/blast/health win models are column/project choices, not interchangeable hidden defaults.
4. Input parsing, hitstop and rollback policy are referenced, never duplicated here.

## Accept

A match-state trace explains legal neutral/engagement options, resources, round/stock progression and win outcome while the referenced specialist skills explain timing/contact/network details. Mirror or asymmetric matchups use the same published system rules.
