---
name: ad-break
description: Use when a game integrates rewarded, interstitial or banner ads and needs explicit placement, lifecycle, resume and reward-grant boundaries without interrupting authoritative gameplay actions.
---

# Ad break

Ask the mode: rewarded, interstitial, banner, none, or existing.

## Contract

Publish:
- stable `ad_session_id` / request identity
- placement ID and placement-policy revision
- provider/platform capability and availability result
- pre-show game/session state and resume target
- completion / skip / cancel / error outcome
- reward receipt or grant reference when applicable
- fallback when the ad is unavailable, interrupted or duplicated

## Ownership

`ad-break` owns ad placement/lifecycle and resume handoff. `game-state-flow` / UI skills own the surrounding game state, `entitlement-grant` owns idempotent rewarded grants, `game-monetization` owns the product/value policy, and provider/store rules remain live external constraints.

## Rules

1. Placement eligibility is project data. Ads need a declared safe boundary; "after fail" or "between encounters" are examples, not universal requirements.
2. Do not pause or splice an authoritative action/cancel/hit resolution in progress. If an ad request arrives at an unsafe boundary, queue, reject or defer it by policy.
3. Rewarded completion produces one grant request keyed by stable receipt/session identity. Duplicate provider callbacks cannot duplicate the grant.
4. No-fill, cancel, background/resume, provider error and session loss have explicit outcomes and do not masquerade as completed reward views.
5. Banner layout obeys UI/safe-area ownership and does not become gameplay collision or input truth.
6. Ads-off / ad-remove behavior is explicit; required game verbs cannot depend on an ad provider being available unless the product intentionally defines that dependency elsewhere.

## Acceptance

For the same placement policy and `ad_session_id`, duplicate lifecycle callbacks settle once, resume returns to the declared valid game state, and rewarded completion maps to at most one entitlement grant. Unavailable or cancelled ads leave the game in a legal non-granted state.
