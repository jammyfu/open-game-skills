---
name: telemetry-events
description: >
  Named events for funnels. Use when a dashboard claims conversion from
  debug VIP, or when every frame is logged. Events are evidence labels,
  not revenue promises.
---

# Telemetry events

Ask the column.

| Column | What you log |
|---|---|
| funnel-min | boot, first-verb, first-fight, reward, wall-see, purchase-ok |
| combat-lab | hit, whiff, cancel, death — sampled |
| live-ops | event start/end, track claim |
| off | ship without analytics |

## Rules

- An event has: name, build, column, cheat-flag, device.
- Debug / lab-slot / teleport sessions tag `cheat=1`. They never sit in the same conversion bucket as story-slot.
- Purchase-ok fires after entitlement-grant, not on button down.
- Wall-see is not a payment. Trial-start is not a payment.
- Do not log secrets, raw receipts, or full chat.
- Sample combat-lab. A 60 Hz dump is a performance bug (performance-budget).

## Accept

A dashboard can filter cheat=1 out of "new players cleared". A missing purchase-ok with a granted item is a grant bug, not a marketing win.
