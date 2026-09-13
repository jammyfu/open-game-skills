---
name: live-ops
description: Use when timed events, rotations, experiments, remote configuration, event rewards, temporary modes, offers, or calendar-driven content need versioned activation and safe expiry/fallback behavior.
---

# Live ops

`live-ops` owns event activation state. Gameplay systems keep ownership of their own rules; live configuration may select published variants but does not create hidden clocks or undocumented balance mutations.

## Event contract

Every event publishes:

```text
event ID
config revision
start/end and time authority
minimum/maximum compatible client when applicable
eligibility rule / cohort assignment
content/rule references
reward transaction identity and idempotent grant policy
fallback when config/content/service is missing
post-event state / cleanup
```

## Rules

1. Eligibility and cohort assignment are deterministic for the declared identity/experiment policy; a refresh must not randomly move a player between incompatible branches.
2. Reward delivery delegates to `entitlement-grant` / economy owners and is **idempotent** across retries.
3. An expired or unavailable event returns to a declared fallback/base configuration without blocking required progression.
4. Remote config is schema/version checked before activation. Unknown required fields fail to the published fallback, not a partially applied mixed state.
5. Temporary modes or encounter mixes reference `encounter-design`/other owners. Monetization cannot silently alter unrelated combat logic to manufacture demand.
6. `patch-cadence` owns rollout/rollback compatibility across client versions.

## Accept

Replay activation, refresh/retry, expiry, clock boundary, incompatible client and missing-config cases. The same event ID/config revision produces explainable eligibility and reward outcomes, and fallback restores a usable base experience.
