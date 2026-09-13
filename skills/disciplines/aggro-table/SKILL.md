---
name: aggro-table
description: Use when an AI must rank multiple hostile or support targets and target changes feel arbitrary, oscillate, ignore threat history, or cannot be explained in debug output.
---

# Aggro Table

This skill owns **AI threat scores and AI target-switch policy**. `enemy-perception` decides who is currently observable/eligible; `enemy-ai` consumes the selected target state. Player lock-on selection belongs to `target-priority`.

## Modes

| Mode | Score source |
|---|---|
| nearest | distance or authored proximity score |
| damage-table | accumulated authored threat events such as damage/support |
| scripted | phase/script supplies target or score override |
| none | actor does not use a threat table |

There is no universal default. Preserve the project's existing target policy when one already exists.

## Stable selection

Each candidate has a stable entity ID, eligibility state, score components and last-selection metadata. Publish deterministic tie-breaking when scores are equal.

Publish switch hysteresis: for example minimum score advantage, minimum hold time, explicit taunt/phase override, or immediate invalidation on death. Do not switch merely because floating-point noise changes rank by an insignificant amount.

Stealth/death/disconnect/phase changes remove or decay candidates according to authored rules. Line of sight can be an eligibility or score input, but the geometry query itself belongs to `enemy-perception`/collision systems.

## Acceptance

For two or more candidates, log score components, stable IDs, winner and switch reason. Reorder candidate containers and replay equal-score/tiny-delta cases; the selected target must remain deterministic. Test target death, stealth/ineligibility and explicit scripted override. A boss turn animation is not enough evidence; the reason must be inspectable.
