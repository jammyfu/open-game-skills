---
name: game-monetization
description: >
  Engine-neutral money columns for games and game-like apps. Use when a
  shop is a second combat clock, when a paywall is called a tutorial, or
  when a debug VIP is treated as a new-player funnel. Ask the column first.
  Does not promise conversion or revenue.
---

# Game monetization

Ask the column.

| Column | What the player pays for | Combat clock |
|---|---|---|
| cosmetic-iap | look, dance, pet | unchanged |
| battle-pass | seasonal track of cosmetics + small convenience | unchanged |
| ad-reward | optional wait → currency or continue | optional, never required mid-combo |
| premium-unlock | one-time remove ads / unlock acts | must not thicken hitboxes |
| live-sub | live ops / extra slots / cloud | cost must match ongoing service |
| fair-f2p | ads or cosmetics only | same windows as payer |

Do not mix fair-f2p with a shop that sells +frames or shorter cooldowns.
A hard paywall before the first verb is a column you name, not the default.

## Order

```
feel the verb (tutorial-design / game-planning slice)
  → understand the offer (what is gated)
  → buy / skip / restore
  → entitlement lands
  → measure with real purchases, not debug flags
```

Value before wall. Copy after the player has used the free verb once.
See gameplay-validation: a scripted VIP flag is not a new-player funnel.

## Offers

- Name the gate: whole app, one act, one tool, one cosmetic.
- Trials are timed access to *that* gate, not a silent full unlock.
- Lifetime SKUs must price the ongoing cost (servers, AI calls, live ops).
- Stroked-through prices need a real prior price. A planned future price is not history.
- "Most popular" needs a count. Otherwise say "recommended".
- Restore-purchase is a job on the paywall. Missing restore is a defect.
- Debug entitlements write lab-slot only (save-integrity).

## Evidence vs wish

| Allowed | Forbidden |
|---|---|
| this SKU exists in code at path X | this SKU converts at 12% |
| public store page lists price P in region R | guessed monthly from a yearly string |
| a recorded purchase on a test account | debug VIP equals a customer |
| unknown cycle | invent a cycle so the table looks full |

No internet → mark prices unverified. Do not invent competitor medians.
Calling this skill does not authorize shipping a price change.

## Accept

A player can finish the first slice without paying if the column is fair-f2p or ad-reward.
Payer and non-payer share action-feel windows.
A wall states what is bought, what happens when the trial ends, and how to restore.
No sentence promises revenue lift.

## See also

App-style onboarding / paywall method notes: `docs/cases/app-monetization-ref.md`.
