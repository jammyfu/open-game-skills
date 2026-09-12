---
name: status-ailment
description: Generic status effects. Burn, slow, stun. Data on the actor, not a second clock.
---

# Status ailment

Ask: none | timed-dot | crowd-control | mixed.
Each status has start, tick, end, and cleanse. Ticks use the logic clock (`action-feel`). Stun may freeze pose; it may not freeze input parse unless the column says so.
HUD uses icon + timer, not color alone (`a11y-controls`, `hud-feedback`).
Do not stack two stuns into a lock the player cannot mash or wait out.

Accept: a player can name what is on them and when it ends. Cleanse or timeout returns a legal idle.
