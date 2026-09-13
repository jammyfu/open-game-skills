---
name: wakeup-oki
description: Use when knockdown, wakeup timing, rise options, wakeup invulnerability, reversal eligibility or post-knockdown pressure need a named option/state contract.
---

# Wakeup oki

Knockdown/recovery timing starts from `hitstun-recover`; this skill owns the **wakeup option set and transition policy**.

## Compatible directions

`quick-rise` | `delayed-rise` | `both`

A project may publish other option sets instead of assuming stand/roll/attack.

## Option contract

Each wakeup **option ID** publishes availability conditions, input/action, start/commit/return states, displacement if any, **invulnerability** or armor/throw eligibility windows when applicable, resource cost and interruption/cancel policy.

## Rules

1. Knockdown end/actionable timing comes from `hitstun-recover`; this skill selects which wakeup transitions are legal around that boundary.
2. Invulnerability/eligibility is explicit per interaction class and logical interval; presentation pose does not grant it.
3. Pressure/meaty/reversal balance is project data. Do not require every meaty to lose to some wakeup option or every defender to have a reversal.
4. Repeated knockdown loops are evaluated against combo/escape/resource rules rather than declared invalid solely by repetition.
5. Training observability may draw wakeup states/windows through `training-mode`, but training does not author stronger options.

## Accept

Replay before/on/after actionable boundaries for every published option and relevant attack/grab class. Logs identify knockdown state, option ID, eligibility/invulnerability and resulting legal state deterministically.
