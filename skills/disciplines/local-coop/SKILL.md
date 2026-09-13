---
name: local-coop
description: Use when multiple local players share one game instance and the project needs stable player/device ownership, join/leave rules, camera policy and shared-state boundaries.
---

# Local co-op

Ask the presentation/control model: shared-camera, split-screen, take-turns, hybrid, or existing.

## Contract

Publish:
- stable `coop_session_id` and revision
- stable `player_id` and bound `device_id`
- join/leave request identity and eligibility
- camera/view policy per local player set
- shared versus per-player inventory/progression/input context
- respawn/reconnect behavior

## Ownership

This skill owns local player membership and device-to-player binding. `input-design` owns semantic actions, camera skills own camera behavior, inventory/progression own canonical state, and `performance-budget` owns presentation budgets.

## Rules

1. Join/leave/rebind requests are idempotent and cannot create duplicate players or leave one device controlling two unintended actors.
2. Shared-camera, split-screen and take-turns are project policies; presentation degradation strategy is owned by performance budgets, not hardcoded here.
3. Mid-session join may use onboarding, spectating or immediate control according to project policy; no universal re-tutorial rule.
4. Device disconnect preserves player identity long enough for the declared reconnect/fallback policy.
5. Shared resources use their owning transaction systems; local co-op does not invent a second inventory or progression truth.

## Acceptance

Given the same `coop_session_id`, membership revision and join/leave requests, the same player/device ownership results. A reviewer can identify camera policy, shared-state boundaries and reconnect behavior without inferring identity from screen index.
