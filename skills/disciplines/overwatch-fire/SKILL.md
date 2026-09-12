---
name: overwatch-fire
description: Hold a cone and fire when a hostile enters. Ally shooting design. Not aim-assist.
---

# Overwatch fire

Ask: cone-hold | suppress-lane | none.

The body aims a published cone. First hostile that enters and is visible (`collision-layers`, `target-priority`) eats one fire row (`projectile-hitscan`). Recover after the shot. Friendly filter is mandatory.
Enemy overwatch uses the same row. Player can read the cone (`stealth-info`). Do not let overwatch ignore walls.

Accept: a dummy walking into the cone is hit on the enter tick. A teammate in the cone is not.
