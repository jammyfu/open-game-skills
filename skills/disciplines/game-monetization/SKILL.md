---
name: game-monetization
description: Use when a game or game-like product introduces paid offers, ads, passes, subscriptions, trials, premium unlocks, paywalls, or store copy and the boundary between pricing, entitlement, gameplay, and evidence is unclear.
---

# Game Monetization

This skill owns **monetization model selection, offer/gate semantics and evidence boundaries**. It does not verify store transactions, grant ownership, set combat timing, or guarantee business outcomes.

## Modes

| Mode | Offer model |
|---|---|
| cosmetic-iap | paid cosmetic/presentation goods |
| battle-pass | seasonal track tied to `season-track` |
| ad-reward | authored optional reward/continue/ad flow |
| premium-unlock | one-time content/feature gate |
| live-sub | recurring service/content entitlement |
| fair-f2p | project policy emphasizing non-paid gameplay parity |

These are product modes, not moral or revenue claims. A project can define additional models explicitly.

## Ownership boundaries

- SKU/offer copy, gate and price intent live here/`iap-offers`.
- Verified purchase ownership and idempotent delivery live in `entitlement-grant`.
- Restore behavior lives in `restore-purchase`.
- Wallet accounting lives in `currency-dual`.
- Gameplay timing/hitboxes/cancels remain in `action-feel` and their real owners; this skill does not secretly author +frames, cooldowns, or collision.
- Seasonal tier/claim state lives in `season-track`.

## Offer evidence

Every offer identifies what is gated, duration/renewal if applicable, price source/region when known, trial/expiry behavior, and restore/cancel path where the platform/product requires it. Unverified price or competitor data stays marked unverified.

Claims such as conversion, retention, ARPU, uplift or revenue require actual analytics with population/window/experiment context. A configured SKU, debug entitlement, test purchase or design hypothesis does **not** prove revenue impact.

Store/platform compliance is version- and region-specific; verify current platform requirements before shipping. Calling this skill never authorizes a production price change by itself.

## Acceptance

A reviewer can trace offer → verified entitlement/restore owner → granted product state without monetization code owning combat mechanics. Test buy/skip/restore/expiry paths appropriate to the selected model, and keep business performance claims separate from implementation correctness. No sentence promises revenue lift without measured evidence.
