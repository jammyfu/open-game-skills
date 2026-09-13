---
name: squad-tactics
description: Use when a controllable multi-character squad needs distinct roles, coordinated actions, shared verbs, or planning/execution rules and one character dominates or coordination becomes unreadable.
---

# Squad Tactics

This skill owns **player-controlled or allied squad role composition and coordination contracts**. It does not prescribe camera genre, squad size, or weapon policy.

## Modes

| Mode | Coordination focus |
|---|---|
| role-kit | distinct authored role/tool identities |
| ghost-clear | stealth-oriented coordination when the project chooses it |
| loud-fail | loud-response/failure-pressure variant when the project chooses it |

The project defines squad size, viewpoint, pause/real-time rules and combat/stealth balance. Top-down, isometric, over-the-shoulder and other presentations can all use the same role contract.

## Role contract

For each controllable body, publish unique capabilities plus shared baseline actions needed to avoid dead-end composition. A unique verb should create a decision, not force a character to exist only for one scripted cameo.

Cross-character actions declare prerequisites, ordering, ownership transfer and interruption behavior. If actions can be queued, integrate with `plan-queue`; perception/stealth information comes from `enemy-perception`/`stealth-info` when relevant.

Weapons/noise are authored project rules. If a shot creates a noise event, publish it through the same perception contract; do not assume ranged combat must always be last resort.

## Acceptance

Test at least two squad compositions supported by the project, including one missing a preferred specialist. A tester can explain each role, shared fallback verbs, and at least one interaction requiring coordination. Interrupt/reorder a coordinated action and verify ownership/state recovery. Camera angle or squad headcount alone is not acceptance evidence.
