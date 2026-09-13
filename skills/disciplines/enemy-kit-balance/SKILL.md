---
name: enemy-kit-balance
description: Use when an enemy moveset has unreadable pressure, weak punish opportunities, repetitive loops, excessive overlap with nearby enemies, or balance changes are leaking into unrelated player timing systems.
---

# Enemy Kit Balance

This skill owns **individual enemy move budgets and kit trade-offs**. `attack-tell` owns warning channels, `group-tactics` owns multi-enemy concurrency, and `difficulty-design` owns difficulty scaling policy.

## Modes

| Mode | Kit emphasis |
|---|---|
| poke-guard | frequent low-commitment pressure with authored gaps |
| burst-duelist | higher commitment burst and punish windows |
| swarm-chaff | simple low-cost moves intended for groups |
| artillery | range pressure with authored close-range weaknesses |

## Move budget

For every move publish logical startup/tell handoff, active interval, recovery, repeat/cooldown resource, damage/reaction, range and any armor/guard interaction. Values are project data; clip length does not substitute for the logical table.

A kit may have one or several high-impact moves depending on encounter role. What matters is that their combined frequency, overlap, coverage and counterplay fit the encounter budget. Do not impose a universal “one scary move” law.

Punishability is defined by the selected game's legal response windows: movement escape, block/parry, interrupt, reposition, resource response, single hit, combo, and so on. Do not require every whiffed heavy to permit a universal two-hit confirm.

## Encounter interaction

When multiple enemies can pressure simultaneously, combine the kit table with `group-tactics` concurrency limits. A move that is fair in a duel may be invalid when several copies overlap. Tune the enemy or encounter budget before secretly shrinking player dodge, input buffer, hitstop or recovery contracts.

## Acceptance

Record move-table data and the intended counter for each high-impact action. Test the kit alone and in representative encounter compositions from `group-tactics`. Measure warning-to-activation, punish windows, repeat cadence and overlapping unavoidable threat. A patch should be explainable as kit/encounter data changes rather than hidden edits to unrelated player timing.
