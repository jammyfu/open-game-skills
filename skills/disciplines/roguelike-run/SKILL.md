---
name: roguelike-run
description: Generic run contract. Death resets the run, not the account. Meta unlocks are starters, not mid-fight power.
---

# Roguelike run

Ask: full-reset | meta-unlock | daily-seed | none.
A run starts clean. Meta unlocks may add starters. They may not change hitboxes mid-run.
Death is run-reset (`death-carry` if present). Debug stays lab (`save-integrity`).
Seed is published if daily-seed.

Accept: a player can say what survives a death. A slated debug run is not a natural clear.
