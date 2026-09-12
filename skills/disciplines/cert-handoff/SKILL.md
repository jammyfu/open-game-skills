---
name: cert-handoff
description: Platform interrupts the game must survive. Ask none vs suspend-resume vs pad-lost vs save-corrupt. Do not paste a first-party checklist. Write the events your slice actually gets.
---

# Cert handoff

Ask the column:

| Column | Event |
|---|---|
| none | no store cert |
| suspend-resume | OS sleeps the process |
| pad-lost | device unplugs |
| save-corrupt | slot bytes are junk |

## Rules

1. On resume: restore look, kill held keys, do not fire a buffered special. Same spirit as cutscene-handoff.
2. Pad-lost is a menu. Play does not keep reading a dead device.
3. Corrupt save fails to a published recover path. It does not wipe other slots. See save-integrity.
4. Docked vs handheld is platform-targets, not a second clock.
5. Store names (TRC / XR / Lotcheck) are labels for your own event list. Do not copy a private matrix into the repo.

## Accept

A forced suspend mid-swing comes back to a legal idle. A junk save offers retry or new slot, never a silent story-flag rewrite.
