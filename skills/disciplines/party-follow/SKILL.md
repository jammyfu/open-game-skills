---
name: party-follow
description: Generic companion follow. One leader, followers stay on nav. Not a second player clock.
---

# Party follow

Ask: leash | formation | combat-split | off.
Followers use the same locomotion column as the leader, slower accel. They do not steal the lock-on target unless the column is combat-split.
Stuck on geometry: stop and teleport only after a published wait, with a visible pop. A bot that cannot path is a nav bug, not a difficulty proof (`gameplay-validation`).

Accept: the leader can enter a door and the follower arrives without blocking the fight.
