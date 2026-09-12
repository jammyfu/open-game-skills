---
name: iap-offers
description: What the player may buy. Ask none vs cosmetic vs convenience vs battle-pass vs power-pay vs ad-remove. Store prices are live facts, not code comments. Do not promise conversion.
---

# IAP and offers

Ask the column:

| Column | What money changes |
|---|---|
| none | no real-money SKU |
| cosmetic | look only |
| convenience | time / slots, not box size |
| battle-pass | season track |
| ad-remove | juice/ads off |
| power-pay | numbers / drops |

Power-pay must be published to balance-design. Silent power-pay is a broken column.

## Trigger

A store, a wall, a pass, an ad-remove, or a request to price a slice.

## Flow

1. Draw the live path: first open → first value → wall or shop → SKU pick → pay / skip → entitlement lands.
2. Separate facts: code, store listing, runtime SKU, operator guess. See gameplay-validation.
3. Free, trial, and paid must list different verbs. A trial of one move is not a trial of the whole game.
4. Lifetime SKUs cannot talk like a subscription. A strike-through price needs a real prior price.
5. Restore-purchase is a role. Pending and fail must not look like success.

## Constraints

- Do not invent revenue or lift percents.
- Debug entitlements write a lab slot. See save-integrity.
- Ads and walls must not steal a buffered attack. See menu-flow.
- shop-price is NPC gold. This skill is real money.
- Competitor mid-price is a starting guess, not a law.

## Accept

Player can name what they buy before they tap. Skip still reaches play. A failed pay does not grant the pass.

## Source method

Adapted from public pay-wall practice (value first, then rights, then a real receipt). Not a copy of any app skill pack.
