---
name: poise-stagger
description: A poise pool that breaks into stagger. Not hyper-armor, not hitstun. Use for 韧性, poise, stagger.
---

# Poise stagger

Ask first: hidden-bar | visible-bar | none.

| Nearby skill | What it is |
|---|---|
| hyper-armor | this swing ignores flinch |
| hitstop | both clocks freeze |
| hitstun-recover | victim cannot act after unfreeze |
| poise-stagger | a pool; at 0 play stagger recover |

Rules: publish refill. Hits that do not break the bar still deal damage and hitstop. Throws ignore poise unless published (`throw-tech`). Do not steal player i-frames to fake a break (`enemy-kit-balance`).

Accept: a player can tell this-swing armor from this-bar poise.
