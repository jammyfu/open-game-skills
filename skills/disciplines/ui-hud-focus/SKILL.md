---
name: ui-hud-focus
description: Use when HUD, menus, dialogs, virtual cursors, keyboard focus, pointer focus, or safe-area layout can lose focus, hide the focused control, leak gameplay input, or restore to the wrong element after a UI transition.
---

# UI HUD Focus

This skill owns **focus/input ownership handoff and focus restoration**. `ui-flow` owns screen state; `input-design` owns semantic actions/bindings; `browser-input` owns browser lifecycle events.

## Modes

| Mode | Focus model |
|---|---|
| play-hud | gameplay owns actions; HUD is non-interactive presentation |
| pause-stack | top interactive modal/screen owns UI actions |
| pad-cursor | virtual pointer/cursor participates in the focus model |
| safe-area | focusable/critical HUD stays in the published visible region |

## Focus contract

On transition into an interactive UI state, record the prior focus owner/element when restoration is meaningful, release or suspend gameplay action reads according to the input context, then establish one explicit focus target. On close, restore to the recorded valid target or an authored fallback; do not dump held/buffered gameplay actions.

Keyboard/D-pad focus must be visible and not obscured by authored UI. Pointer, virtual cursor and keyboard focus may be unified or distinct by project policy, but simultaneous indicators must represent real owners rather than accidental duplicate highlight state.

If the focused element disappears, becomes disabled, or a modal closes, resolve focus deterministically to a valid authored fallback. Localization/layout changes must not strand focus off-screen.

## Acceptance

Test keyboard, controller and applicable pointer navigation through nested modals, focus target removal, resolution/aspect changes and language switch. Close/reopen restores the intended target or fallback, focused controls remain visible, and one UI action produces one transition without triggering gameplay. Record focus owner/element IDs, not only screenshots.
