---
name: ghost-line
description: Use when a recorded path, replay or racing ghost must be reproduced against a specific track/ruleset while remaining presentation-only and isolated from the live player's simulation truth.
---

# Ghost line

Ask the source: own-best, downloaded, event-pack, debug-replay, off, or existing.

## Contract

Publish:
- stable `ghost_replay_id` and replay schema revision
- source build/ruleset ID
- `track_revision` / world revision
- versioned `input_schema` or state-sample schema
- RNG/seed references when required
- explicit `compatibility` predicate and fallback
- presentation/collision policy

## Ownership

This skill owns ghost/replay compatibility and playback intent. Vehicle/gameplay simulation remains with its owning systems; `gameplay-harness` may provide deterministic tape infrastructure where appropriate.

## Rules

1. A ghost may replay semantic inputs, canonical state samples or another authored replay format; input replay is not universal.
2. Incompatible track/ruleset/schema revisions are rejected, migrated or clearly degraded according to policy; geometry mismatch alone does not dictate one universal response.
3. Ghost presentation cannot alter live-player speed, collision, targeting, rewards or timing unless the project explicitly defines a competitive interaction mode elsewhere.
4. Replay order uses recorded logical identity/timestamps, never render interpolation as truth.
5. Download/source identity and integrity are recorded so evidence can distinguish stale data from a gameplay defect.

## Acceptance

Given the same `ghost_replay_id`, compatible revisions and deterministic inputs, playback follows the same canonical replay data. A compatibility failure is explicit, and changing ghost opacity/interpolation does not alter the live simulation.
