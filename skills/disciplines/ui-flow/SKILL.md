---
name: ui-flow
description: Use when pause, inventory, map, shop, settings, radial, or other screens need an explicit state graph and world-time policy and opening/closing screens causes invalid transitions or gameplay leakage.
---

# UI Flow

This skill owns **screen/page state, navigation transitions, modal stacking, and each screen's world-time policy**. `ui-hud-focus` owns focus/input handoff; `input-design` owns semantic actions and physical bindings.

## Modes

| Mode | World-time policy |
|---|---|
| diegetic | gameplay continues according to project rules |
| pause-pages | the selected pause source suspends the configured simulation scope |
| hotbar-only | no full page transition |
| radial | authored slow/freeze/live policy |

Each screen has a stable screen/state ID, legal incoming/outgoing transitions, parent/modal relationship, resume target, and pause/timescale source if any. Do not key navigation state by localized labels.

Confirm/Cancel/Back are semantic actions owned by `input-design`; this skill only declares which navigation actions are valid in a UI state. Physical-key conflicts are resolved by active input contexts, not hardcoded here.

Shop state delegates to `shop-price`; inventory to `inventory-economy`; map to `world-map`; rebinding UI edits `input-design` mappings. Critical gameplay information must remain available according to `hud-feedback`/`attack-tell` while a live-world UI is open.

## Acceptance

Replay open/navigate/modal/back/close transitions, duplicate open/close requests, and scene/session handoff. The same logical UI state and resume target result. Opening or closing a page never synthesizes a stale gameplay action; focus correctness is verified through `ui-hud-focus`.
