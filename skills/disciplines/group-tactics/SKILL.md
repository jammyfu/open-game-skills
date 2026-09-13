---
name: group-tactics
description: Use when several enemies share one encounter and simultaneous attacks, flanks, holds, armor, or role changes create unfair overlap, idle crowds, or nondeterministic coordination.
---

# Group Tactics

This skill owns **encounter-level coordination and concurrency budget**. Individual move legality lives in `enemy-kit-balance`; individual brain states live in `enemy-ai`.

## Modes

| Mode | Coordination |
|---|---|
| swarm | lightweight local roles with authored concurrency cap |
| flank-hold | attackers/flankers/holders exchange engagement slots |
| role-pack | explicit role slots and reassignment rules |
| none | enemies act independently |

## Engagement budget

Publish the concurrency budget in project data. It may be one active attacker, several engagement tokens, weighted attack costs, per-role caps, spatial sectors, or another explicit scheme. **One attacker at a time is a valid configuration, not a universal law.**

Token/slot acquisition and release use stable actor IDs and logical events. Death, stun, distance, phase changes and interrupted windups must release or transfer budget according to the authored rule; do not leak a slot forever.

Armor, grabs, ranged pressure and crowd-control may carry different costs. Do not hardcode a fixed number of armored bodies as universally fair or unfair; validate the chosen overlap budget with encounter evidence.

## Acceptance

Run scenes at minimum/typical/maximum supported group sizes. Log role, token/slot ownership, request time and release reason. Reverse actor iteration and verify the same eligible actors win ties under the stable rule. Test an attacker dying or being interrupted while holding a slot. Measure overlapping unavoidable threat windows rather than judging fairness from animation count alone.
