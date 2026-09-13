---
name: cutscene-handoff
description: Use when entering, skipping, interrupting, or leaving a cinematic can leave held input, camera, timescale, combat state, UI, or player control in the wrong state.
---

# Cutscene Handoff

This skill owns **control/state transfer into and out of cinematics**. It does not own tutorial goals, attack warnings, or pause policy.

## Modes

| Mode | Skip policy |
|---|---|
| skippable | immediate authored skip action |
| hold-to-skip | hold gesture with progress/cancel semantics |
| first-play-locked | skip disabled only under an explicit first-play policy |

## Handoff contract

Before takeover, snapshot or explicitly reset the play states the project needs: semantic held inputs, pointer/look capture, camera owner, UI context, timescale/pause source, and any gameplay transition token. Releasing control must not synthesize stale button edges or resume a stuck held action.

If a cinematic request arrives during hitstop, attack resolution, physics transition, save commit, or another unsafe logical boundary, queue it to the project's next safe boundary rather than imposing a universal ban on cinematics during combat.

Skip/complete handlers are idempotent. Duplicate skip, natural-end and scene-unload callbacks may race, but rewards, flags, camera restoration and control restoration happen once.

A cinematic that contains required warning/teaching information coordinates with `attack-tell`/`tutorial-design`; skip behavior must preserve the required gameplay contract by alternate presentation or authored policy.

## Acceptance

Test natural completion, immediate/held skip, duplicate skip+end callbacks, focus loss, scene unload and takeover requested at an unsafe logical boundary. After handoff, one fresh input produces one valid action and camera/UI ownership is correct. Log takeover and restore reasons rather than judging from animation alone.
