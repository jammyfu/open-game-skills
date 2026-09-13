---
name: training-mode
description: Use when a practice room, training sandbox, dummy behavior, input/frame display, record/replay, reset flow, or repeatable combat lab setup is needed without changing live gameplay rules.
---

# Training mode

This skill **owns the practice-room contract**. Combat timing, boxes, damage, movement and netcode stay with their live owners.

## Modes

| Mode | Dummy behavior | Typical observability |
|---|---|---|
| dummy-block | authored guard/stance response | input/history or outcome log as requested |
| dummy-wakeup | authored wakeup/tech response | wakeup timing/state evidence |
| dummy-record | record and replay a bounded response/input trace | recording/playback identity |
| lab-full | project-selected combination of dummy, reset and observability tools | project-defined overlays |

Modes are capabilities, not mandatory shipping requirements or defaults. A project may expose a smaller/larger training surface.

## Rules

1. Training consumes the same logical move, hitbox/hurtbox, hitstun, resource and movement contracts as live play. It may pause/reset/reposition for lab workflow, but does not author stronger moves or longer cancels.
2. Record/replay stores an input/action trace plus relevant configuration/seed/state identity. Playback cannot read future player input unless the project is explicitly testing an adaptive agent.
3. Reset publishes target state: position, facing, resources, dummy behavior, RNG/recording state and any stage state that must be restored. Reset is a training action, not inherently a menu or reload.
4. Frame/input/box displays are observability. Their numbers come from authoritative logical events and clocks; presentation delay does not rewrite them.
5. Leaving/restarting training clears or restores training-only overrides explicitly. Online practice, when supported, keeps the project network contract rather than silently hiding latency.

## Accept

Repeat the same configured lab case after reset/reload and obtain the same logical setup. A verified punish/string/interaction uses the same live gameplay contracts outside training, while training-only observability and reset tools do not leak into normal play.
