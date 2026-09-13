---
name: entitlement-grant
description: Use when verified purchases, subscriptions, durable unlocks, consumables, or time-limited access must be granted exactly once across retries, crashes, duplicate callbacks, and multiple devices.
---

# Entitlement grant

This skill owns verified purchase-event → durable entitlement state. Store UI and pricing belong elsewhere; `restore-purchase` owns user-initiated/current-entitlement reconstruction.

## Product classes

| Class | Durable state |
|---|---|
| non-consumable/durable-unlock | boolean/ownership keyed by product plus store identity |
| consumable | balance mutation keyed by a unique transaction/purchase token/event id |
| subscription/time-pass | entitlement interval/status keyed by the store's stable subscription identity/token |
| battle-track/season | ownership scoped to season/content identity |

## Idempotent transaction state machine

Use the immutable store transaction ID, purchase token, or equivalent verified event ID as the deduplication key; do not use UI callbacks or order display strings as the primary key.

A safe abstract flow is:

1. receive `pending`/purchased event and persist processing state;
2. verify authenticity/account/product and confirm it is grantable;
3. in one durable transaction, record the event ID and apply the entitlement/balance mutation if that event ID is not already committed;
4. only after durable grant, acknowledge / consume / finish according to product/store requirements;
5. if acknowledgement/consume/finish fails, retry that store-side completion **without granting again**;
6. emit UI refresh from durable entitlement state.

For stores that require consumption before re-purchase, preserve enough pending state that a crash cannot lose a consumed-but-not-accounted grant. Platform adapters may vary the exact store call sequence, but they must prove no crash window can duplicate or lose value.

`PENDING` or unverified purchases do not grant. Revocation/refund handling updates entitlement through an explicit policy rather than deleting unrelated story progress.

## Acceptance

Replay the same transaction/purchase token many times; kill after verification, after durable grant, and before/after acknowledge/consume/finish. The resulting durable entitlement or consumable delta is applied exactly once, and store completion can retry independently. Test pending→purchased and refund/revoke paths. Unrun sandbox/server cases stay `not-run`.
