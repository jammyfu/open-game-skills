---
name: combo-design
description: Strings, links, cancels, juggles. Ask which graph you are shipping. Use for fighters, character-action, and brawlers.
---

# Combo design

Ask the column:

| Column | What connects |
|---|---|
| strict-link | next button during a tight post-hit window |
| cancel-chain | cancel graph on whiff or hit, authored windows |
| launcher-juggle | air state + gravity + priority |
| action-string | style / rank, long cancel into guns and jumps |
| lock-on-brawler | target magnet, few true links |

## Rules

1. Write a directed graph. Nodes are moves. Edges are windows + conditions (hit, block, whiff, jump, instrument).
2. Damage falls off with length. An infinite that does not fall off is a bug unless the column is a training toy.
3. Starter, confirm, ender. If a route has no ender, the opponent never gets a turn.
4. Hitstun and launch height are data on the attack, not a side effect of animation length.
5. Dropping a combo must look like a drop. Hidden magnets that finish the route after a miss belong only to lock-on-brawler.
6. Stack under action-feel. Combo-design does not own the clock.
7. Charge edges (start / full / hold-cost / release / cancel) are named nodes, not a side animation.
8. After hitstun, weapon swap, or lost focus, the graph re-enters idle or a published recover. It does not keep a phantom confirm.

## Accept

- Designer can draw the graph on one page
- A dropped combo returns turn to the opponent inside the published recovery
- Changing one edge does not require rewriting every character
- Pose, box, and SFX share the same logical frame on every node
