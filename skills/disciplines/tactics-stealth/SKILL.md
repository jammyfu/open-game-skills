---
name: tactics-stealth
description: Use when a real-time squad or multi-actor stealth game must compose perception, information, planning, movement and ranged/melee actions without hardcoding one specific cone model or command cadence.
---

# Tactics stealth

Ask which project modes already exist: perception model, information presentation, planning/queue mode, movement/stance model, ranged/melee action owners, and alert-sharing policy.

## Contract

Publish:
- stable `stealth_scenario_id` and revision
- actor/squad identities and authored role capabilities
- perception policy reference from `enemy-perception`
- information/presentation policy reference from `stealth-info`
- planning/commit policy from `plan-queue` when commands are queued
- action owners for movement, melee and ranged resolution
- alert/noise propagation policy and stable event identity
- fail/recovery/reset policy

## Ownership

`tactics-stealth` owns composition of a multi-actor stealth scenario. It does not redefine sight/hearing truth, shot resolution, queue timing, locomotion, HUD cones or enemy target selection.

## Rules

1. Inner/outer cones, continuous suspicion, light/noise fields or other perception models are project data; dual-cone stealth is not universal.
2. Crawl/stand visibility, stance speed and cover behavior come from the owning perception/locomotion policies rather than genre assumptions.
3. A noise or alert event affects only recipients selected by the authored propagation policy; one loud action does not universally alert the whole map.
4. Queued commands follow `plan-queue` commit ordering. They are not required to start on the same logical tick.
5. Melee, ranged, enemy-fire and targeting keep their own stable action/event identities and clocks.
6. Tactical UI may visualize authorized information but cannot grant NPCs knowledge or modify perception truth.

## Acceptance

Given the same scenario revision, actor state, perception/alert inputs and queued command set, the same scenario-level transitions and delegated action requests are produced. Changing tactical UI presentation or render cadence does not change who perceived what, which commands committed, or the authoritative action outcomes.
