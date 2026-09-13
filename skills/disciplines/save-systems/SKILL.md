---
name: save-systems
description: Use when game progress needs versioned slot schemas, migration rules, atomic persistence, rollback safety, or a single authoritative save-file contract.
---

# Save systems

This skill owns the durable progress document shape and commit protocol. `save-checkpoint` owns when a checkpoint is taken; `save-integrity` owns which slot may contain debug/capture state; `cloud-save` owns cross-device reconciliation.

## Modes

| Mode | Shape |
|---|---|
| single-slot | one logical story slot with explicit overwrite/new-game policy |
| multi-slot | named/player-selected slots with independent revisions |
| profile-plus-slots | profile metadata plus one or more story slots |

## Schema and migration

Every durable document publishes `schema_version`, slot/profile identity, revision/generation, and enough metadata to reject the wrong owner/account. Old schemas migrate through explicit version-to-version steps or fail without overwriting the source. Migration runs on a copy and records success before the old version is replaced.

Unknown/newer schemas are not silently truncated. A migration test fixture keeps at least one representative save from every supported historical version.

## Atomic commit

A save is committed atomically: write/flush a new payload to a temporary or journaled location, validate it, then replace the current committed pointer/file using the target platform's atomic primitive where available. Preserve a previous/backup/last-known-good generation until the new commit is known durable.

Never update the only good copy in place. A process kill between payload write and commit must leave either the old committed save or the complete new save, not a half-written hybrid.

## Load selection

Validate identity, schema, checksum/structure and revision before applying gameplay state. If the newest generation is invalid, fall back only to a verified previous/backup generation and report that recovery occurred. Other slots remain isolated.

## Acceptance

Test normal save/load, kill during write, out-of-space/write failure, corrupt newest generation, v1→current migration and unsupported-future schema. Verify slot isolation, migration evidence, and that the last-known-good save remains loadable after every failed commit. Unrun device/filesystem cases stay `not-run`.
