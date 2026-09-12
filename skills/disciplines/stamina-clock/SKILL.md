---
name: stamina-clock
description: Generic stamina / meter spend. Sprint, dodge, charge. One bar, published recover.
---

# Stamina clock

Ask: none | shared-bar | per-verb.
Spend happens on the logic clock (`action-feel`). Empty bar cancels the next sprint / dodge / charge start, not the current hitstop.
Recover starts after a published idle. Hitstun may pause recover; it may not reset the bar unless the column says so.
HUD is one pip or bar (`hud-feedback`). Color is not the only empty-tell (`a11y-controls`).

Accept: a player can empty the bar on purpose and still walk. A dodge that costs more than the bar does not start.
