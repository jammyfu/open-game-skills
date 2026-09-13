---
name: iap-offers
description: Use when a game exposes real-money offers, passes, ad-removal or paid power/convenience and needs a versioned offer catalog, eligibility and purchase handoff without owning platform transaction fulfillment.
---

# IAP and offers

Ask the product class: none, cosmetic, convenience, battle-pass, ad-remove, power-pay, subscription, or existing.

## Contract

Publish:
- stable `offer_id` and catalog revision
- provider/store `product_id` / SKU mapping
- product class and entitlement mapping
- offer eligibility / visibility predicate
- live price/currency source and last-refresh state
- purchase request identity and current lifecycle state
- presentation / disclosure requirements for the project/platform
- fallback when store data, payment or entitlement service is unavailable

## Ownership

`iap-offers` owns catalog composition, eligibility and purchase-entry presentation. Platform/store APIs own transaction truth; `entitlement-grant` owns idempotent granting, `restore-purchase` owns restoration, `season-track` owns season progression, `ad-break` owns ad lifecycle, and `balance-design` owns any gameplay-balance consequences.

## Rules

1. Store price, currency, subscription period and localized product metadata are live provider facts. Do not hardcode stale price claims as gameplay truth.
2. UI selection creates or resumes a purchase request; it never grants the entitlement merely because a button was pressed or a checkout UI closed.
3. Pending, cancelled, failed, deferred and successful provider states remain distinct. Only authoritative transaction evidence is forwarded to the grant owner.
4. Duplicate purchase/provider callbacks are safe because grant processing keys off stable transaction/purchase identity.
5. Product class is explicit. Consumable, non-consumable, subscription, pass and ad-removal products do not share one restore/lifetime policy.
6. Paid power or progression effects are disclosed to their owning balance/economy policy; this skill does not silently rewrite combat, drops or difficulty.
7. Debug/test products and sandbox receipts stay distinguishable from production entitlements and evidence.

## Acceptance

A reviewer can trace `offer_id` → live store product → purchase request → provider outcome → entitlement mapping without any UI-only success granting value. Duplicate callbacks do not duplicate ownership, failed/cancelled/pending paths grant nothing prematurely, and restore behavior follows the declared product class.
