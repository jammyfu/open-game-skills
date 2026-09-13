---
name: rest-site
description: Use when a rest, bench, camp or checkpoint interaction may heal, save, repopulate or restore state and needs an atomic rest transaction, stable site identity and project-defined repopulation policy.
---

# Rest site

Ask: `heal-only | heal-and-save | heal-save-repop | off`.

## Ownership

`rest-site` owns the rest interaction transaction. Save persistence delegates to `save-checkpoint` / `save-systems`; encounter/world owners define what may repopulate; difficulty/debug state remains with its owner.

## Contract

Publish:
- stable `site_id`
- `rest_txn_id`
- ordered effects such as heal/resource restore/checkpoint/repopulate
- commit boundary
- interruption policy
- project-defined repopulation set/rules

Do not assume ordinary enemies always return or bosses always stay dead. Repopulation is explicit data keyed by stable encounter/entity IDs.

A repeated callback for one committed `rest_txn_id` is idempotent. If an interaction is interrupted before commit, no partial save/repopulate side effects remain; after commit, retry reconstructs the same result.

## Acceptance

Rest, quit and reload preserves the committed checkpoint and unlock state. Repeating the same transaction cannot heal, grant, save or repopulate twice, and the evidence can state exactly which site/revision/entity set changed.
