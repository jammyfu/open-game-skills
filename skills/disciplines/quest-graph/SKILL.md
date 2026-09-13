---
name: quest-graph
description: Use when quests need stable node identities, prerequisites, branching dependencies, activation/completion conditions, parallel hooks, or graph-level progression without turning map pins into quest logic.
---

# Quest Graph

This skill owns **quest nodes, dependencies, branch conditions and graph-level activation/completion rules**. `quest-beat` owns the transactional lifecycle/recovery of an individual beat; `world-map` owns map markers.

## Modes

| Mode | Graph shape |
|---|---|
| one-hook | one highlighted/primary hook while other state may still exist |
| hub-board | several selectable quest roots from a hub/board |
| rumor-web | loosely connected discovered hooks and optional branches |

Each node has a stable ID, authored prerequisites, activation/completion/failure conditions, and declared rewards/effects. Save data references stable IDs rather than localized titles or array positions.

The number of simultaneously active hooks is project data. UI may highlight one primary objective, several tracked objectives, or none; do not confuse presentation limits with graph-state limits.

Parallel/optional branches may intentionally affect main progression when authored. Validate dependency cycles, unreachable nodes and orphaned prerequisites. Soft-lock/recovery semantics for an individual step belong to `quest-beat`.

## Acceptance

Given a saved graph snapshot, a tester can explain why each visible node is locked, available, active, completed, failed or hidden. Reorder serialized nodes and confirm stable IDs preserve state. Test branch convergence/divergence and missing prerequisite cases without relying on map arrows as logic.
