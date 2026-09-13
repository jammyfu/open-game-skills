---
name: quest-beat
description: Use when an individual quest step can be accepted, progressed, failed, canceled, abandoned, turned in, or become unrecoverable because required state or items changed unexpectedly.
---

# Quest Beat

This skill owns the **transactional lifecycle and recoverability of one quest step**. `quest-graph` owns node dependencies; `dialogue-flags` owns dialogue branch facts; `world-map` owns pins.

## Modes

| Mode | Failure/recovery emphasis |
|---|---|
| one-hook | focused step with a clear current objective |
| hub-board | repeatable/parallel beat selected from a board/hub |
| fail-forward | failure advances to an alternate authored state |

Use a stable beat ID and explicit states such as unavailable, offered, accepted/active, completed, turned-in, failed, canceled, or abandoned as the project requires. Transitions are idempotent: duplicate callbacks, reloads or repeated interactions do not grant rewards twice or regress a completed beat.

For every destructive transition, identify recoverability: retry, respawn item, alternate route, fail-forward, abandon/reaccept, rollback to checkpoint, or intentionally permanent consequence. A “soft lock” claim requires evidence that no authored recovery path remains.

## Acceptance

Replay accept/progress/complete/fail/cancel/reload transitions including duplicate events. The same stable beat state and reward outcome must result. Test loss of a required resource/object and demonstrate the authored recovery or explicitly record an intentional permanent failure.
