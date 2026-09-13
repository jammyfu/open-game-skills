---
name: save-integrity
description: Use when debug, capture, training, cheats, recovery, or validation sessions could contaminate a player's natural story progress or trusted evidence.
---

# Save integrity

This skill owns trust boundaries between save classes. It does not define the underlying schema or atomic write algorithm (`save-systems`).

## Modes

| Mode | What may be stored |
|---|---|
| story-slot | natural player progress only |
| lab-slot | debug grants, teleports, forced phases, synthetic items |
| capture-slot | reproducible snapshot plus disclosure of overrides |
| settings-only | controls, language, audio, accessibility; no progress |

## Rules

1. Name the destination class before applying cheats or forced state.
2. Debug/capture mutations never autosave into a story slot.
3. Copying lab/capture state into story is an explicit developer action with confirmation and provenance, never an implicit merge.
4. Difficulty overrides and validation helpers use dedicated metadata rather than impersonating natural unlock flags.
5. Cloud sync preserves slot class and never upgrades lab/capture state into trusted story progress.
6. Recovery from a corrupt story save may choose an earlier verified story generation; it must not silently substitute a lab/capture slot.

## Acceptance

Run a debug session that teleports, grants items and changes difficulty, then verify the prior story generation is byte/logically unchanged. Export capture evidence and confirm override provenance is present. Simulate cloud/recovery selection and verify only matching trust classes are candidates.
