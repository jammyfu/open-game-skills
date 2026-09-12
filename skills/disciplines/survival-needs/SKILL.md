---
name: survival-needs
description: Hunger, thirst, camp. Separate from durability-economy.
---

# Survival needs

Ask: hunger-thirst | camp-rest | none.
Meters tick on the logic clock. Camp is a rest-site column. Wear of tools stays `durability-economy`. Do not drain HP in hitstop.

Accept: the player can name when they last ate and where they can camp. Empty hunger is a published fail, not a silent HP leak.
