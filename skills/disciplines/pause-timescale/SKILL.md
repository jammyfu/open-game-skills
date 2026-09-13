---
name: pause-timescale
description: Use when pause, slow motion, UI freeze, cutscene hold or network-aware time control needs explicit clock ownership, arbitration and resume semantics separate from hitstop.
---

# Pause / timescale

Ask the mode: hard-pause, scaled-time, ui-freeze, network-aware, layered, or existing.

## Contract

Publish:
- stable `pause_policy_id` and revision
- stable `pause_request_id`
- requester/scope/priority and `arbitration` rules
- affected clock owner(s) and scale/stop behavior
- input/audio/presentation resume policy
- nesting/stacking semantics
- online/session authority requirements where applicable

## Ownership

This skill owns world/actor time-control policy and arbitration. Hitstop remains with combat timing, UI focus remains with UI skills, audio routing with audio skills, and network authority with netcode/session systems.

## Rules

1. A pause request never assumes a universal timescale implementation; engine adapters map the policy to project clocks.
2. Multiple requests resolve by explicit arbitration/stack policy and release only their own scope.
3. Resume consumes fresh semantic input edges where required so held actions do not fire unintentionally.
4. Slow-motion and accessibility variants publish which clocks scale and which remain real-time.
5. Networked pause behavior is project/session policy with explicit authority/consensus rules, not a universal allow/deny rule.

## Acceptance

Given the same policy revision and request set, the same effective clock states result. Duplicate acquire/release calls are idempotent, nested requests restore correctly, and resume does not silently add gameplay frames or replay stale input.
