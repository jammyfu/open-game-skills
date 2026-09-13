---
name: throw-tech
description: Use when throws, command grabs, grab eligibility, throw breaks/techs, escape windows or throw-vs-armor/invulnerability interactions need a deterministic attempt/result contract.
---

# Throw tech

## Compatible modes

`break-window` | `command-grab` | `both`

## Throw contract

Each attempt receives a stable **throw attempt ID** and references its grab volume/range (`hitbox-hurtbox`), source/target, logical attempt window, **eligibility** rules, break/tech options if any, priority/trade policy, resulting states and resource/cooldown effects.

## Rules

1. Hit/grab geometry and candidate collection stay with `hitbox-hurtbox`; this skill decides throw-specific eligibility and resolve/escape rules.
2. Break/tech windows are project-authored logical intervals/actions. Command grabs may be untechable, state-guaranteed or otherwise specialised when explicitly published.
3. Armor/invulnerability interaction delegates to `hyper-armor`/defense eligibility contracts; no universal “throws always beat armor” rule is assumed.
4. Duplicate overlap/callbacks for one throw attempt resolve at most once according to stable attempt identity.
5. Whiff/miss behavior is project data; a guaranteed throw in a specifically eligible state is not inherently a bug.

## Accept

Test ineligible/eligible/breakable/unbreakable/boundary cases and repeated overlap. The throw attempt ID explains exactly one result and recovery state, independent of render overlap duration or container iteration order.
