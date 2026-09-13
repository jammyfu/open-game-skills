---
name: level-teach
description: Use when a specific room or spatial beat must teach, reinforce, test, or remix a mechanic and the player is being asked to perform it before receiving sufficient in-world practice.
---

# Level Teach

This skill owns **spatial teaching beats for a mechanic already defined elsewhere**. `tutorial-design` owns the wider onboarding sequence; `level-design` owns the room/route structure.

## Modes

| Mode | Spatial objective |
|---|---|
| show | expose the mechanic, affordance, or consequence |
| safe-try | allow low-cost practice when the project needs it |
| test | require the mechanic under authored consequence |
| remix | combine known mechanics or add a new constraint |

The project chooses which modes are required and their order. `show → safe-try → test → remix` is a useful pattern, not a universal mandate. Some mechanics are self-evident, optional, discoverable, narrative-only, or intentionally learned through consequence.

Prompts reference semantic actions from `input-design`; they do not create another input mapping. `ability-gate` coordinates which side of a gate exposes/practices a required ability. `attack-tell`, traversal skills, puzzle rules, or other true owners define the mechanic itself.

## Acceptance

For the chosen teaching objective, identify the mechanic, prior knowledge, permitted failure cost and expected demonstration. Observe whether a representative player can perform the intended action afterward without hidden tester guidance. Mark omitted teaching phases explicitly rather than pretending they occurred.
