---
name: visual-novel-ui
description: Use when dialogue presentation needs portraits, nameplates, text advance, auto-play, skip, backlog, choice UI, or read-state behavior and those controls can skip choices, lose line identity, or diverge after localization.
---

# Visual Novel UI

This skill owns **dialogue presentation and reading controls**, not narrative branch facts. `dialogue-flags` owns persistent branch outcomes; `game-localization` owns localized strings; `ui-hud-focus` owns interactive focus.

## Modes

| Mode | Reading control |
|---|---|
| page-click | explicit advance action |
| auto-play | authored auto-advance timing with user stop/pause |
| backlog | read-history viewer |

Every displayed line/choice references stable dialogue/line/choice IDs; localized text and screen position are presentation, not identity. Backlog records the seen line identity plus the locale/text version needed by project policy.

Skip/auto operate only over states marked skippable/read by the narrative system. A pending choice is an interactive state and cannot be auto-accepted or silently skipped. Choice focus/confirm/cancel follows `ui-hud-focus` and `input-design`.

Portrait/nameplate/speaker indicators reference stable speaker/asset IDs and localized labels through `game-localization`. Runtime language changes preserve current line/choice identity and branch state.

## Acceptance

Test manual advance, auto stop/resume, skip into a pending choice, backlog after localization switch, duplicate input edge and save/reload at a choice. The same stable line/choice IDs and `dialogue-flags` state remain intact; auto/skip never commits a choice without the authored action.
