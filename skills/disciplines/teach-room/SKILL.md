---
name: teach-room
description: Use when older routes, prompts, or project notes refer to teach-room and need the current spatial teaching contract without maintaining a second set of teaching rules.
---

# Teach Room

Compatibility entry. Delegate spatial teaching behavior to [`level-teach`](../level-teach/SKILL.md) and overall onboarding sequence to [`tutorial-design`](../tutorial-design/SKILL.md).

Do not maintain independent room-order, mechanic-count, respawn, or difficulty rules here. Preserve an explicitly chosen legacy mode only long enough to map it to the closest `level-teach` objective:

| Legacy intent | Delegate |
|---|---|
| see-safe-test | `level-teach / show, safe-try, or test` as project requires |
| introduce-expand-remix | `level-teach / show or remix` plus tutorial sequence |
| silent-space | `level-teach / select` with minimal/no text |

## Acceptance

A request routed through `teach-room` reaches the same owner and project data as a direct `level-teach` request. No separate “one mechanic per room” or fixed teaching sequence evolves in this compatibility file.
