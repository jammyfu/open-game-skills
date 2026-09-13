---
name: durability-economy
description: Use when tools or equipment can wear, dull, break, repair, consume charges, or recover condition and the wear transaction, warning policy, replacement flow, or economy pressure is unclear.
---

# Durability Economy

This skill owns **condition state and wear/repair transactions**. It does not author hitstop, cancel windows, inventory capacity, or item progression identity.

## Modes

| Mode | Condition model |
|---|---|
| consume | instance can reach an authored terminal/broken state |
| sharpness | effectiveness changes across condition bands |
| repair | condition is restored by an authored repair transaction |
| unbreakable | no durability state |

## Wear contract

Publish what events spend condition: hit contact, shot fired, block received, elapsed use, environment interaction, charges, or another project rule. Misses, soft targets and hard-target multipliers are project-specific; do not assume one mass/contact formula fits every tool.

Every wear/repair event has a stable cause/transaction identity when duplicate callbacks are possible. Applying the same logical event twice must not double-spend or double-repair condition.

Warnings are authored presentation tied to condition thresholds or predicted remaining uses. The number of warning hits, swap time, break animation and replacement availability are project data.

Economy balance may target replacement abundance, scarcity, field maintenance or permanent gear. A fight does not universally need to refund at least the wear it consumed; validate the selected economy using `inventory-economy`, `loot-roll` and play evidence.

## Acceptance

Test condition at one-before/at/after thresholds, duplicate wear events, interrupted repair, save/load, break or minimum-condition state, and the selected replacement/recovery path. The condition ledger and transaction IDs explain every change. Do not claim balance from the durability formula alone.
