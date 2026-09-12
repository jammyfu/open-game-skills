---
name: game-localization
description: >
  In-game language, fonts, and layout. Use when a build works in one
  language and breaks in another, when glyphs tofu, or when a long string
  eats a button. Not a marketing brief.
---

# Game localization

## Trigger

More than one language ships, or title-font is already mixed into body text.

## Mode

| Column | Scope |
|---|---|
| terms-only | item / move / resource names |
| ui-layout | buttons, HUD, menus × language |
| runtime-switch | change language mid-session |
| full-pass | terms + layout + switch + docs |

## Inputs

Glossary seed. Font files. Target devices from platform-targets. Screenshot folder per language.

## Procedure

1. One glossary: equipment, moves, resources, interact prompts. Same word in HUD, menu, tutorial.
2. Fonts: display face for titles, coverage face for body. Fallback chain published. Tofu check on every shipped language.
3. Dynamic bits: numbers, key glyphs, plurals, long translations, runtime switch.
4. Matrix: language × desktop/phone × landscape/portrait.
5. README / help / shots match the language they claim.

## Constraints

- Key glyphs follow kb-mouse-map jobs, not letters baked into art.
- Runtime switch does not drop input or stack audio beds.
- Overflow wraps or scales; it does not cover Confirm.
- Size thresholds are per device, not one magic point size.

## Outputs

Glossary. Font coverage list. Matrix with pass/fail. Screenshots labeled by language.

## Accept

In combat the prompt is readable. Buttons do not overflow. A screenshot matches the language on screen.
