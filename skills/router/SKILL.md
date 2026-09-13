---
name: router
description: Use when an existing integration invokes the legacy router entry instead of the canonical dispatcher.
---

# Router compatibility entry

`router` is a compatibility alias. Delegate to [dispatcher](../dispatcher/SKILL.md), the single routing-policy owner.

## Rules

- Do not maintain a second keyword table, genre matrix, engine selector or mode resolver here.
- Preserve explicit project engine/mode choices and pass the request through unchanged except for compatibility normalization required by the host integration.
- Do not load additional skills merely because this legacy entry was used.
- Dispatcher acceptance/evidence rules apply unchanged.

## Acceptance

For the same project facts and request, entering through `router` yields the same USE / ENGINE / ASK / DEFER decision as entering through `dispatcher`. Any divergence is a compatibility bug, not a new routing policy.
