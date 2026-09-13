---
name: patch-cadence
description: Use when client builds, content/config revisions, balance changes, staged rollouts, schema migrations, or rollback plans need an explicit compatibility and change-management contract.
---

# Patch cadence

Cadence is project policy, not a fixed statement about which content is allowed to change weekly or seasonally.

## Change record

For each release/config change publish:

```text
release/config revision
minimum client / supported client range
schema or data-version changes
behavior/content changes + owner
rollout policy / cohort if staged
rollback target + rollback trigger
save/economy compatibility notes
telemetry comparison window
```

## Rules

1. User-visible rule changes are attributable to a version/revision; do not silently mutate core behavior behind an old build label.
2. **Minimum client** and data/config **schema** compatibility are checked before activation.
3. A staged **rollout** has a stable cohort rule and an observed health gate; 100% is not assumed from one healthy sample.
4. A **rollback** names the last compatible revision and how newer persistent data is handled. Rollback must not corrupt saves or duplicate economy/entitlement transactions.
5. Persistent progression follows `save-integrity`; do not hardcode any particular numbered slot.
6. Live event activation stays in `live-ops`; this skill owns cross-version rollout/compatibility policy.

## Accept

Given any active client/build and config revision, a reviewer can determine compatibility, rollout state, data/schema expectations, rollback target, evidence window and unresolved migration risk.
