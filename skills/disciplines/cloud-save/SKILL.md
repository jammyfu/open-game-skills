---
name: cloud-save
description: Use when local and remote progress can diverge across devices, accounts, offline sessions, reinstalls, or interrupted synchronization.
---

# Cloud save

Cloud synchronization reconciles already-valid local save generations. It does not replace `save-systems` atomic persistence or `save-integrity` trust classes.

## Modes

| Mode | Reconciliation |
|---|---|
| single-authoritative | one server/backend revision is authoritative and clients submit against a known base |
| prompt-conflict | divergent descendants require a player/operator choice |
| deterministic-merge | only fields with an explicit domain-safe merge rule combine automatically |

Blind `last-write-wins` is not a safe default for divergent progress.

## Revision model

Every synchronized generation carries a stable slot/profile ID plus a monotonic revision/generation and, when supported, the base version/ancestor it was derived from. Uploads use compare-and-set/precondition semantics where the backend permits them.

If local and remote share an ancestor and only one side advanced, fast-forward. If both advanced from the same base, classify it as a conflict unless every changed field has a declared deterministic merge rule. Playtime, timestamp, or file size alone do not decide which progress is correct.

## Failure handling

Download to a temporary generation, validate with `save-systems`, then atomically commit locally. Upload failure leaves the local committed save intact and queues/reports retry state. Account changes never merge different owners. Story/lab/capture classes remain separate.

## Acceptance

Test offline edits on two devices from the same base version, one-sided fast-forward, divergent quest/inventory changes, stale upload, account switch and interrupted download. The system must explain the winning revision or present a conflict; no valid branch is silently deleted. Unrun backend/device tests remain `not-run`.
