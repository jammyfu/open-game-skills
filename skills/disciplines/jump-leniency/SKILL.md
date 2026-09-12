---
name: jump-leniency
description: Coyote time, jump buffer, variable height, corner nudge. Ask strict-arcade vs generous-platform vs none. Windows stay short. This is locomotion data, not a second clock.
---

# Jump leniency

Ask the column:

| Column | Forgiveness |
|---|---|
| none | edge is edge |
| generous-platform | coyote + buffer + variable height |
| strict-arcade | buffer only, tiny or zero coyote |

## Rules

1. Coyote is 2-6 logic frames after leaving ground. Buffer is 4-10 frames before landing. Both under ~150ms unless the column says otherwise.
2. Variable jump: release early cuts height. Hold does not add a second jump unless double-jump is data.
3. Corner nudge slides a near-miss along a wall instead of bonking. It must not skip a published lethal line.
4. These windows do not extend hitstop or cancel graphs. See action-feel.
5. A bot that needs 30 frames of coyote is automation, not a reason to grow the window.

## Accept

A jump that looks late by one beat still lands on a generous-platform slice. A jump that is late by a walk cycle still fails.
