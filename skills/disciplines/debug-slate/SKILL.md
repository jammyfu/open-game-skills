---
name: debug-slate
description: Use when QA, capture, training, development, or automation modifies game state and the resulting evidence must record exactly which non-natural tools or overrides were active.
---

# Debug slate

Debug provenance is structured evidence, not merely an on-screen label.

## Modes

| Mode | Availability policy |
|---|---|
| off | no QA/debug override is active for this session |
| labeled-dev | QA/debug tools may be active and every state change is recorded in structured provenance |
| shipping-hidden | tools are removed, disabled, authenticated, or otherwise unavailable to normal play according to the shipping policy |

These names are compatibility modes, not a requirement that every development build expose every debug verb.

## Session record

Assign a stable **session ID** and record structured fields such as:

```text
session ID
build ID + commit/version
save/profile provenance
active QA/debug tools or state overrides
activation/deactivation timestamps or logical ticks when relevant
linked capture/case IDs
```

`save-integrity` owns which profile/slot may persist synthetic state. `gameplay-capture` consumes this provenance when labeling evidence.

## Rules

1. Any state-changing QA/debug action appends structured provenance rather than relying on the reviewer noticing a visual overlay.
2. Runtime debug UI availability is a project/build policy. Production may remove, disable, authenticate or hide tools; do not require every development build to expose every verb.
3. Debug/training tools reuse live gameplay owners and clocks unless explicitly testing an alternate implementation.
4. Modified-state evidence may prove a focused feature but cannot silently become proof of a natural progression/challenge path.
5. Restart/load behavior must make clear whether the override persisted, was reapplied, or was cleared.

## Accept

From the session ID a reviewer can recover the exact build, save provenance, active overrides and linked evidence, and distinguish natural state from QA-created state without inspecting implementation code.
