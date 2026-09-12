---
name: telemetry-events
description: Events have a name, a denominator, and a window. Ask off vs funnel-only vs full-economy. An event is not a conversion promise. Do not log secrets.
---

# Telemetry events

Ask the column:

| Column | What you record |
|---|---|
| off | none |
| funnel-only | session, slice accept, wall, pay, skip |
| full-economy | plus sinks, grants, ads |

## Rules

1. Every rate names a numerator, a denominator, and a time window.
2. Trial start is not a paid convert. Ad impression is not revenue.
3. Debug and lab flags travel with the event or the row is junk.
4. No tokens, no message bodies, no other players' ids in client logs.
5. A/B needs a published baseline. Tiny samples are watch notes, not stats.

## Accept

A report can say what was counted and what was not proven. See gameplay-validation.
