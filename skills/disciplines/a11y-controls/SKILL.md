---
name: a11y-controls
description: Use when input, text, color, audio, flashing, motion, holds, repeated presses, timing, or UI presentation can exclude players and accessibility preferences need explicit behavior without changing hidden gameplay rules.
---

# A11y Controls

This skill owns **accessibility preference semantics and assistive input/presentation transforms**. `input-design` owns core actions/mappings; `hud-feedback`/UI skills own presentation surfaces; gameplay skills own hitboxes, damage and timing rules.

## Capability set

Project-selected options may include action remap, hold↔toggle/tap alternatives, digital alternatives for analog-required functions, adjustable sensitivity/deadzone, text scale, subtitle/caption presentation, mono audio, color + non-color cues, reduced flash, reduced motion/camera effects, timing assists, or other documented accommodations.

Prefer remapping semantic **actions** rather than only swapping physical controls. When a function normally requires hold/repetition/analog motion, provide an alternative or configurable behavior when the project/platform targets it. Update hints/prompts to reflect the active mapping.

Accessibility presentation preferences must not silently rewrite unrelated hitboxes, collision, hidden cancel graphs, or entitlement state. If an assist intentionally changes gameplay timing/difficulty, name that assist and its scope explicitly rather than disguising it as a display option.

Color-critical state uses another distinguishable channel. Reduced-flash/motion settings retain required warning meaning through another supported channel. Subtitle/caption settings coordinate with localized text and significant audio cues through `game-localization`/HUD owners.

## Acceptance

Build a capability matrix by supported device/input and preference. Test remapped actions, toggle alternatives, digital alternatives where supported, text scaling, non-color critical cues, reduced-flash/motion, and preference persistence. Record unsupported combinations as not-run/unsupported rather than claiming universal accessibility.

## References

For applicable targets, verify current platform guidance before shipping (for example Xbox Accessibility Guidelines for input/captions and WCAG 2.2 for web UI focus/visibility).
