---
name: currency-dual
description: Use when a game has one or more wallets, earned/purchased currency, event tokens, conversions, grants, spends, refunds, or balances that can duplicate, go negative, mix identities, or become hard to audit.
---

# Currency Dual

This skill owns **wallet identity and the currency ledger**. Store purchase verification/ownership belongs to `entitlement-grant`; offers belong to `game-monetization`/`iap-offers`; vendor pricing belongs to `shop-price`.

## Modes

| Mode | Wallet pattern |
|---|---|
| one-wallet | one gameplay wallet |
| soft-hard | separate earned and purchased/premium wallet classes |
| battle-token | event/match/season token wallet |

Names are examples. A project may have additional wallets when each has explicit ownership and accounting rules.

## Ledger contract

Every wallet has a stable wallet ID, currency definition ID and integer/fixed-point balance representation appropriate to the economy. Every grant, spend, conversion, refund and correction writes a ledger entry with stable transaction ID, reason/source and signed delta.

Applying the same transaction ID twice is idempotent. A spend validates sufficient balance or an explicit overdraft rule before commit. Multi-wallet conversion either commits both ledger sides atomically or neither side.

Sources, sinks, inflation targets, exchange rates and whether a wallet intentionally accumulates are project economics. A wallet with no sink is not automatically a bug. Time-limited rates/offers must identify their validity window and owner.

Purchased currency arrival coordinates with `entitlement-grant`/store verification; a client flag alone is not a trusted grant.

## Acceptance

Replay grant/spend/refund/duplicate-callback and conversion-crash cases. Ledger entries reconcile to displayed balances, no duplicate transaction changes a wallet twice, and the user can identify which wallet a price uses. Economic health claims require measured source/sink data, not wallet count alone.
