---
name: enemy-fire
description: How enemies shoot. Tell, burst, miss, suppress. Not an aimbot. Use for 敌人射击, suppression, burst fire.
---

# Enemy fire

Ask first: burst | suppress | accurate.

Hits are `projectile-hitscan`. Who they aim at is `target-priority`. Shot pattern lives here. `overwatch-fire` is hold-a-lane; this is the burst after a tell.

| Column | Pattern |
|---|---|
| burst | tell → N shots → recover |
| suppress | long spray near last-known, low accuracy |
| accurate | short tell, high accuracy, long recover |

Rules: first shot after spotting has a tell (`attack-tell`). Cover and outer-cone crouch lower accuracy. Reload is a move. Do not steal player i-frames.

Accept: a player can duck a burst they saw start. Same seed repeats the first burst count.
