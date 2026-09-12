---
name: netcode-feel
description: Online is a feel column. Ask delay-based vs rollback vs lockstep vs server-auth. Fighting prefers rollback. Kart items may be server-auth. Do not add a second clock to hide latency.
---

# Netcode feel

Ask the column:

| Column | Who is right |
|---|---|
| delay-based | both wait N frames |
| rollback | predict, rewind, resimulate |
| lockstep | both sims, pause on stall |
| server-auth | server pose wins |

## Rules

1. Fighting-design prefers rollback. Racing cars can rollback; items may be server-auth.
2. Publish input delay. Do not stack delay on top of rollback error.
3. Resimulate from the logic step. Camera must survive a rewind without a pop.
4. Hitstop stays on ActorClocks. Do not freeze the network clock.
5. Prefer a short freeze or a correction over a teleport unless the column is server-auth shooting.

## Accept

- Training mode and a 2-frame delay lobby feel like the same game
- A rollback correction does not cancel a move the player already saw connect
