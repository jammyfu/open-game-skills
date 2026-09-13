---
name: target-priority
description: Use when lock-on, aim assist, targeting UI, or attack selection has several valid bodies and the chosen mark flips, disagrees across systems, or changes without a clear rule.
---

# Target Priority

This skill owns the **eligible target set, scoring/pick rule, and switch policy** for player-facing or ability targeting. `lock-on-target` owns camera/facing behavior after a mark is chosen. AI threat selection belongs to `aggro-table`.

## Modes

| Mode | Pick policy |
|---|---|
| nearest-in-cone | score by authored distance/angle inside eligible cone |
| stick-until-dead | retain current mark while its authored validity rule holds |
| threat-first | prefer candidates currently presenting authored threat |
| manual-cycle | player cycles a stable ordered set |

## Deterministic pick

Filter eligibility first using faction/team rules, alive/targetable state and any required occlusion policy. Every candidate has a stable ID. When scores tie, use an authored stable tie-breaker rather than container order.

Publish switch hysteresis or grace where appropriate: score margin, input request, occlusion grace, timeout, target invalidation, or mode-specific rule. Hard/soft lock are presentation/control policies, not reasons to force one universal retention mode.

If camera mark, aim mark and damage target are intentionally different, name that contract explicitly. Accidental disagreement is a bug; intentional separation must be inspectable.

## Acceptance

Replay a multi-target scene with candidate iteration reversed and tiny score changes. The chosen target and switch reason must be stable. Test target death, temporary occlusion, ally filtering and manual cycle order. Debug output names eligible candidates, scores, current mark and switch reason; the highlighted sprite alone is not evidence.
