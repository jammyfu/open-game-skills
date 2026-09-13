---
name: shop-price
description: Use when an in-game vendor, catalog, exchange, restock, discount, or purchase option needs explicit price identity, eligibility, wallet ownership, or comparison against world acquisition without altering gameplay clocks.
---

# Shop Price

This skill owns **vendor/catalog price presentation and eligibility for in-game purchases**. Wallet accounting belongs to `currency-dual`; real-money ownership/grants belong to `entitlement-grant`; randomized grant policy belongs to `loot-roll`/`pity-table`.

## Modes

| Mode | Vendor role |
|---|---|
| convenience | offers an alternate acquisition path |
| sink | intentionally removes an authored wallet resource |
| gacha-display | displays a randomized offer whose actual roll is owned elsewhere |
| none | no vendor pricing |

## Price contract

Each offer has a stable offer/item ID, price amount, wallet/currency ID, availability conditions, stock/restock policy, and optional validity/discount window. Localized labels and crossed-out prices are presentation; they do not replace the underlying price/version data.

The relation between shop acquisition cost and world/drop acquisition time is project balance. A vendor may be cheaper, more expensive, exclusive, convenience-oriented, progression-gated or purely cosmetic when intentionally authored.

A real-money price or entitlement does not directly modify `action-feel`, hitboxes or other gameplay timing. It hands verified grants to `entitlement-grant`/wallet owners.

## Acceptance

Test exact balance, insufficient balance, stock boundary, offer expiry/restock, duplicate purchase callback and price-version change. The charged wallet and granted result reconcile exactly once. Compare shop/world paths only using measured project data rather than a universal “shop must cost more time” rule.
