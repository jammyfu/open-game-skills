---
name: level-blockout
description: Use when a level needs a greybox that proves traversal metrics, encounter footprint, sightlines, gates, and pacing before art production or final set dressing begins.
---

# Level Blockout

This skill owns **greybox implementation and measurable spatial probes** for a level design. It does not require every room to teach a new mechanic.

## Modes

| Mode | Output |
|---|---|
| beat-sheet | ordered spatial beats and transition reasons |
| metric-kit | reusable greybox dimensions and traversal probes |
| greybox-play | playable blockout with temporary collision/markers |

Pull movement/camera metrics from the actual project (`locomotion`, `platform-jump`, `camera-anti-clip`) and design intent from `level-design`. When a room is intended to teach, use `level-teach`; combat, traversal, rest, narrative and connector spaces do not need fake teaching beats merely to justify their existence.

Art may begin when the project-defined blockout exit criteria are met. Those criteria can include navigation readability, traversal fit, encounter space, performance risk, streaming boundary, or stakeholder approval—not a universal “stranger must walk every room first” rule.

## Acceptance

Run the greybox with representative character/camera metrics and no dependency on final textures. Record collisions, unreachable surfaces, camera failures, traversal times and gate behavior. Use `gameplay-validation` for actual playability evidence. Concept art alignment does not override failed spatial metrics.

## Art replacement handoff

Pass movement/camera metrics, protected spawn/door/traversal envelopes and stable collider/gate identities to [scene-assembly](../scene-assembly/SKILL.md). Art replacement must preserve those constraints. Its static room-graph preflight does not replace this skill's runtime spatial probes or progression-aware validation.
