---
name: adventure-tool
description: Use when a signature traversal/combat/puzzle tool needs a small verb kit, target-capability contract and interruption rules across swing, yank, grapple or optional weapon use. It does not impose one genre's ammo or puzzle philosophy.
---

# Adventure tool

Ask: `tool-swing | tool-yank | tool-and-gun`.

## Ownership

This skill composes a signature tool's verbs. Grapple physics may delegate to `grapple-swing` / `physics-interaction`; ranged fire to `projectile-hitscan`; puzzle teaching to `puzzle-design` / `level-teach`; bindings to `input-design`.

## Contract

Define stable:
- `tool_action_id`
- required target capability/tag
- startup/active/recovery or interaction phases from the project's action clock
- resource/cooldown owner if any
- interruption/cancel policy
- authoritative success/failure event

Do not assume guns are scarce, puzzles come first, or the tool must clear a gap without a weapon. Those are project design choices.

A target may advertise pullable, swingable, cuttable, shootable or another project capability. Presentation cannot make an unsupported target legal.

## Acceptance

The same tool action against the same target capability/state produces the same authoritative result. Interrupted actions cannot double-apply, stale targets fail closed, and optional ranged/ammo policy remains owned by its dedicated system rather than this skill.
