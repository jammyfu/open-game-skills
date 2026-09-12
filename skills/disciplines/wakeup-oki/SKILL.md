---
name: wakeup-oki
description: >
  Knockdown and get-up options. Use when a knock-down is a cutscene with
  no reply, or when every jab knocks down. Stacks on hitstun-recover and
  fighting-design.
---

# Wakeup / okizeme

Ask the column.

| Column | Knockdown | Get-up |
|---|---|---|
| rare-down | only dedicated moves | auto stand |
| soft-down | many heavies | quick-rise / late-rise |
| oki-mix | down is a turn | roll / stand / invuln rise |
| none | no grounded down | — |

footsie-tight defaults rare-down. brawler-juggle may skip down for air state.

## Clock

Down is a state after hitstun if the row says so. Get-up has startup / invuln / recover like any move.
A meaty is the attacker's plus on the opponent's first actionable frame. It is authored, not an accident of animation length.

## Iron rules

- Wakeup invuln, if any, is on the row. Do not hide it in a flash.
- Throw and strike answers on wakeup are different jobs (throw-tech if stacked).
- Infinite knockdown loops are a combo-design bug unless the column is a training toy.
- Enemies use the same down rules. A boss that never stands is a phase, named in boss-design.

## Accept

A player can stand without guessing a 50/50 every time on rare-down. Training-mode can set down state and show first actionable frame.
