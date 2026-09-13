---
name: analytics-funnel
description: Use when product or gameplay telemetry must be grouped into a versioned funnel with explicit steps, cohort, denominator and observation window so drop-off claims are auditable rather than inferred from screenshots or raw event counts.
---

# Analytics funnel

Ask the analysis intent: first-session, progression, encounter, commerce, retention, or existing.

## Contract

Publish:
- stable `funnel_id` and revision
- ordered step IDs and the `telemetry-events` schema/version each step consumes
- cohort / eligibility predicate
- denominator definition
- observation window and timezone/session boundary policy
- deduplication / late-event policy
- segment dimensions allowed for comparison
- excluded or unknown population

## Ownership

`analytics-funnel` owns funnel definition and aggregation semantics. `telemetry-events` owns event schema/emission, gameplay systems own state truth, and `gameplay-validation` owns qualitative/playability claims. Funnel correlation is not causal proof.

## Rules

1. Do not require events to occur on one universal logic tick; consume the authoritative event timestamp/session identity defined by `telemetry-events`.
2. Event names, step order and denominator are versioned. A schema or eligibility change starts a new comparable revision or is explicitly migrated.
3. Duplicate/retried events are deduplicated by stable event/session identity according to policy.
4. A drop-off rate always names numerator, denominator, cohort, build/ruleset and time window.
5. Privacy/data-minimization rules are project/platform constraints; do not add person-identifying inputs merely to make a funnel easier to join.
6. Heat maps and funnels suggest where to investigate; they do not prove why a player failed, quit or converted.

## Acceptance

Given the same event set, funnel revision, cohort and window, aggregation produces the same step counts and denominator independent of ingestion order. A reviewer can reproduce the reported drop-off and identify excluded/late/duplicate events without treating the result as causal gameplay proof.
