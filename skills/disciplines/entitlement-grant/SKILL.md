---
name: entitlement-grant
description: >
  Grant, restore, and revoke what was paid for. Use when a purchase
  succeeds and the item is missing, when debug VIP leaks into story-slot,
  or when restore is a dead button. Stacks on game-monetization.
---

# Entitlement grant

Ask the column.

| Column | Lands how |
|---|---|
| durable-unlock | once, restore-safe (remove-ads, act, cosmetic) |
| consumable-stack | count += N, no restore |
| time-pass | start → expiry, server or signed clock |
| battle-track | season id + tier |

## Order

```
store says ok → verify receipt → write entitlement → refresh HUD / inventory
restore tap → same verify → same write (idempotent)
```

Client-only "I bought it" flags are not durable-unlock.
Debug VIP writes lab-slot only (save-integrity). It is not a receipt.

## Iron rules

- Restore exists on the wall and in settings for every durable-unlock SKU.
- A second grant of the same durable id is a no-op, not a duplicate item.
- Consumable-stack does not use restore. Say so on the SKU card.
- Expiry uses a trusted clock. Local date rollback does not extend a pass.
- Failed verify: keep the pending UI, do not grant, do not eat the receipt.
- Combat columns do not read entitlements to shorten hitstop or cancels.

## Accept

Kill the app after a sandbox purchase; the unlock is still there. Restore on a second device grants once. A debug flag does not survive a story-slot load.
