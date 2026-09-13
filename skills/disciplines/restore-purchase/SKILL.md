---
name: restore-purchase
description: Use when a user needs previously purchased non-consumables or subscriptions reconstructed on a new/reinstalled device, or when local entitlement state may be stale.
---

# Restore purchase

Restoration discovers currently restorable store/account history or entitlements, then feeds each verified item through the same idempotent `entitlement-grant` path used for purchases.

## Product eligibility

| Product type | Restore behavior |
|---|---|
| non-consumable | restorable/current-entitlement item; re-grant idempotently |
| auto-renewing subscription | reconstruct current entitlement/status from authoritative store/server state |
| non-renewing/time-limited product | restore only if the product/store contract and your persistence strategy support it |
| consumable | normally not reconstructed as spendable balance from generic restore history; use your durable/server ledger if the design requires cross-device consumable balance |

Do not treat "restore" as "replay every historical purchase and increment counters".

## Flow

1. start from an explicit user action or the platform-approved current-entitlement refresh path;
2. fetch/sync store state without deleting local entitlements on transient failure;
3. verify product/account identity and classify restorable vs non-restorable items;
4. send each verified item through the idempotent grant function keyed by original/stable transaction identity or purchase token as appropriate;
5. report completion, partial failure, or no-restorable-items without touching story-save trust classes.

Restored callbacks may repeat or replay history. Repetition must not duplicate durable unlocks or consumable balances.

## Acceptance

On a second device/reinstall, restore a non-consumable and active subscription, repeat restore multiple times, test no-purchase account, expired/revoked subscription, store/network failure, and a consumable SKU. Restorable access returns once; consumable balance is not blindly incremented; transient failure never wipes known-good entitlement state.
