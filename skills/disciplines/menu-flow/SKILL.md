---
name: menu-flow
description: Use when older routes, prompts, or project notes refer to menu-flow and need the current UI screen-state and focus contracts without maintaining a second menu ruleset.
---

# Menu Flow

Compatibility entry. Delegate screen/page transitions and pause policy to [`ui-flow`](../ui-flow/SKILL.md), focus/input handoff to [`ui-hud-focus`](../ui-hud-focus/SKILL.md), semantic controls to [`input-design`](../input-design/SKILL.md), and browser lifecycle details to [`browser-input`](../browser-input/SKILL.md) when applicable.

Do not maintain independent physical key, Pointer Lock, multi-touch, hitstop, shop, or inventory rules here. Preserve legacy intent only long enough to select the real owner:

| Legacy intent | Delegate |
|---|---|
| pause/shop/inventory page | `ui-flow` + `ui-hud-focus` |
| confirm/cancel/back binding | `input-design` |
| pointer/focus-loss browser behavior | `browser-input` |

## Acceptance

A request routed through `menu-flow` resolves to the same project screen/focus/input data as a direct request to the true owners. No second pause/input grammar evolves in this compatibility file.
