---
name: plan-queue
description: Use when players pause or slow execution to author future commands and the project needs stable plan/command identity, validation, ordering and commit semantics without inventing a second simulation clock.
---

# Plan queue

Ask the planning mode: freeze-queue, soft-pause, live-plan, none, or existing.

## Contract

Publish:
- stable `plan_session_id` and plan revision
- stable `command_id` for each queued command
- actor/target/action references and authored parameters
- validation time and invalidation policy
- explicit `commit order` / concurrency semantics
- cancel/edit/confirm request identity
- execution owner and pause policy reference

## Ownership

`plan-queue` owns authored command intent and commit ordering. `pause-timescale` owns time policy. The action/combat/navigation system that receives a command owns whether and how it executes.

## Rules

1. Planning does not create another combat/simulation clock.
2. Commands may execute simultaneously, sequentially, dependency-ordered or actor-authored according to policy; same-tick execution is not universal.
3. Confirm/edit/cancel requests are idempotent by plan/request identity.
4. A command invalidated between planning and execution records a deterministic skip/replan/fallback result rather than silently retargeting.
5. Presentation order in the queue UI is not execution order unless explicitly authored.

## Acceptance

Given the same `plan_session_id`, revision, queued commands and confirm request, the same command set and commit order are produced. A reviewer can distinguish plan validity from the downstream systems that execute each action.
