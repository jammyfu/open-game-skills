---
name: rng-seed
description: Named RNG streams on the logic tick. Use for 种子, replay seed, drop table.
---

# RNG seed

Ask first: run-seed | room-seed | drop-seed.

Rules: combat rolls and drop rolls are different streams. Replay = seed + inputs (`gameplay-validation`). Do not roll on the render thread. Meta unlocks options, not a silent luck buff (`roguelike-run`).

Accept: same seed + same inputs = same first shuffle and same first drop.
