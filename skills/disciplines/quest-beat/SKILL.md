---
name: quest-beat
description: Accept, fail, turn-in, soft-lock detect. Map pins are not a quest machine.
---

# Quest beat

Ask: one-hook | hub-board | fail-forward.
A beat has give / do / turn-in / fail. `world-map` pins are player notes. `dialogue-flags` write the flag. `quest-graph` is the node list — this file owns stuck detection: spent key + closed door is a bug.
Do not paint full-map arrows.

Accept: a tester can name the current hook and the fail state.
