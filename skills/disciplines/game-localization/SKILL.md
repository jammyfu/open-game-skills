---
name: game-localization
description: Generic game i18n. Terms, fonts, wrapping, runtime language switch. Use when the player must read combat prompts in more than one language.
---

# Game localization

## Trigger

Ship or test more than one language. Screenshots, help, and HUD must match the active locale.

## Inputs / columns

Ask: single-locale | terms-locked | live-switch.
Need: string table, font files, device class (`platform-targets`).

## Flow

1. Lock a glossary: gear, moves, resources, interact prompts. One term per thing.
2. Split fonts: display titles may be decorative; body and HUD must cover the locale and a fallback.
3. Check dynamic bits: numbers, key glyphs, plurals, long translations, live language switch mid-fight.
4. Layout matrix: locale × desktop/phone × landscape/portrait. Buttons must not clip.
5. Sync README / help / maker notes / store shots to the same locale.

## Constraints

Do not bake English into textures a locale must replace. A missing glyph is a ship blocker. Live-switch must not reset the fight.

## Output

Glossary + font coverage list + layout matrix + unmatched screenshots.

## Accept

A player can read a combat prompt. Buttons do not overflow. A screenshot matches the language it claims. Type size is set per device class.

## Cases

`docs/cases/playtest-lessons.md`
