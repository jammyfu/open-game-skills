---
name: telemetry-events
description: Use when product, gameplay, QA, economy, or reliability questions require measurable events with stable schemas, denominators, sampling, privacy boundaries, and explicit evidence limits.
---

# Telemetry events

Choose the minimum collection scope that answers the named question.

| Mode | Scope |
|---|---|
| off | no product telemetry |
| funnel-only | session and named funnel milestones |
| domain-events | explicitly approved gameplay/economy/reliability events |

## Event schema

Each event type has a stable name plus `schema_version`. Define field names/types, timestamp/clock semantics, session/account/device identifiers at the minimum necessary granularity, environment/build version, and provenance such as QA/capture status when relevant. Schema changes are versioned or backwards-compatible; dashboards do not silently reinterpret old rows.

Every reported rate publishes numerator, denominator, eligibility population and time window. Trial start is not paid conversion; an impression is not revenue; a missing event is not automatically a user action.

## Sampling and quality

Publish sampling policy and weight sampled rows correctly. Record dropped/buffered event counts where transport can fail. Validate duplicate/retry handling, client-clock anomalies and schema rejection. Small or biased samples are labeled accordingly.

## Privacy

Apply the project's consent, privacy, retention and deletion requirements before collection. Do not place secrets, auth tokens, message bodies or unnecessary personal data in event payloads. Identifier strategy must be documented rather than improvised per event.

## Acceptance

Given a metric, another reviewer can derive the same numerator, denominator, window and eligible population from the versioned schema. Test duplicate events, offline buffering, schema migration, sampling, consent-disabled mode and clock anomalies. State what the telemetry can support and what it cannot prove.
