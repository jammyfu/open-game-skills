---
name: hud-feedback
description: Use when important gameplay state, action failure, danger, resource condition, objectives, or status changes are invisible, ambiguous, color-only, or buried behind menus.
---

# HUD Feedback

This skill owns **player-facing state communication**, not the underlying gameplay state or thresholds.

## Modes

| Mode | Information density |
|---|---|
| minimal | only project-defined critical state |
| combat-full | combat/resource/status state needed during action |
| sim-dials | denser simulation/management state |

Each HUD element names the authoritative source field/event and presentation priority. Thresholds such as low health, durability warning, ammo, heat or timer boundaries come from their owner (`durability-economy`, combat/resource systems, etc.); this skill does not hardcode them.

When an action fails, show an authored reason when useful: unavailable resource, cooldown, invalid target, blocked interaction, or another project state. Do not infer logic from animation alone.

Critical information is not encoded by color/hue alone when another distinguishable channel is required; use shape, icon, text, pattern, position, audio/haptic or another project-appropriate alternative. `a11y-controls` owns user preferences; `ui-hud-focus` owns interactive focus.

## Acceptance

Test critical states at their real source boundaries with color-reduced/no-audio/reduced-flash settings that the project supports. A player can identify the state and reason without opening an unrelated menu. Log source event/value and rendered indicator state; a screenshot alone does not prove timing correctness.
