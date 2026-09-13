---
name: game-localization
description: Use when a game ships or tests multiple locales and string identity, glossary terms, plural/number formatting, glyph fallback, wrapping, layout, key prompts, subtitles, or runtime language switching can become inconsistent.
---

# Game Localization

This skill owns **localized string identity, locale selection/fallback, formatting and language-specific content/layout validation**. UI state/focus remains with UI skills; persistent dialogue facts remain with `dialogue-flags`.

## Modes

| Mode | Locale behavior |
|---|---|
| single-locale | one active shipping/test locale but still uses stable string IDs |
| terms-locked | multiple locales with controlled glossary/terminology |
| live-switch | locale can change without restarting the full application/session |

Every translatable entry has a stable string ID independent from source text, translated text and table order. Dynamic values use locale-aware formatting/plural rules; key/controller glyphs come from the active input mapping rather than baked text.

Publish locale fallback chains and font/glyph fallback behavior. Missing strings/glyphs produce inspectable fallback/error evidence; release severity is determined by the project's shipping criteria, not by this skill alone.

Glossary terms, body/display font roles, subtitle/caption strings and layout constraints are explicit. Test long/short strings, CJK/RTL where supported, plural/number/date cases, text scale and device/aspect matrices relevant to the product.

A live language switch updates localized presentation while preserving stable gameplay/save/entity IDs and current logical state. It must not reset combat, quest progress, focus owner or inventory because labels changed.

## Acceptance

For each supported locale, verify stable string ID coverage, fallback/glyph coverage, representative dynamic formatting and critical UI/subtitle layouts. Switch locale at runtime when supported and confirm gameplay/save/focus state is unchanged. Screenshots match the active locale they claim, but screenshots alone are not string-coverage evidence.
