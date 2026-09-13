---
name: game-state-flow
description: Use when whole-game startup, loading, play, pause, results or retry transitions conflict, rewards settle twice, or stale scene callbacks affect a new session.
---

# Game state flow

## Scope

Own the session lifecycle, not character move frames or menu widget layout. Preserve the current engine and game loop, including noncombat games. Reuse [menu-flow](../menu-flow/SKILL.md) for focus and [save-systems](../save-systems/SKILL.md) for persistence. One transition authority does not require one global boolean or forbid orthogonal UI states.

## Modes

| Mode | Contract |
|---|---|
| single-session | one active run and explicit restart boundary |
| round-based | multiple rounds share a session; round IDs prevent duplicate settlement |
| persistent-session | world progress survives scene transitions; session identity remains explicit |

## Procedure

1. Inspect existing transitions. Write a table of source state, event, guard, destination, entry/exit work and task/input owner. Map boot/menu/loading/play/results/retry only where the game uses them; add cancellation and load failure paths. Pause may be a substate, not a destructive restart.
2. Process events through one authoritative transition boundary. Specify ordering and priority when victory, death and quit occur in the same tick. A rejected transition has a reason; do not let callback arrival order decide who wins.
3. Assign session/round IDs and an epoch to asynchronous work. On exit, cancel work where possible and invalidate its epoch. A late result must check its owner before changing state. Disconnect listeners and release owned handles; cancellation alone does not guarantee a callback cannot arrive.
4. Make settlement idempotent by a stable settlement ID. Use the persistence owner's transaction/retry semantics; setting a UI flag does not make rewards crash-safe. Retry changes identity only when a new round actually begins. Repeated confirmation cannot create duplicate runs or grants.
5. Publish focus, held-input/buffer clearing, audio and save rules across pause, resume, disconnect and scene failure. Do not arbitrarily reset actors to idle if the authored resume policy restores their state. For online games, the authoritative session decides; a local menu is not permission to pause the server.

## Outputs

Adapt the [contract example](assets/contract.example.json): state/event table, ownership/epoch rules, settlement policy, failure recovery and event trace. Mark unknown decisions. Do not replace working architecture solely to match this example.

## Acceptance

Exercise normal startup-to-outcome, retry twice, simultaneous terminal events, and a callback from an abandoned load. There must be one accepted terminal result, no duplicate reward and no stale mutation. Save interruption checks require the actual persistence adapter. [Evaluation scenarios](assets/evals.json) remain not-run until executed; document tests do not prove a game passed.

## References

[SCXML state-machine semantics](https://www.w3.org/TR/scxml/) is a reference for events, transitions and parallel states, not a requirement to install an SCXML runtime. Preserve the project's existing state machinery when it already enforces the contract.
