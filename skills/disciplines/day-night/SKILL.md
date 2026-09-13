---
name: day-night
description: Use when world time changes lighting, schedules, availability, stealth, spawning or other systems and the project needs one versioned clock contract with explicit consumers.
---

# Day night

Ask the mode: cosmetic, scheduled-world, gameplay-linked, externally-driven, hybrid, or existing.

## Contract

Publish:
- stable `time_cycle_id` and revision
- clock source and time scale/pause policy
- canonical time state and boundary definitions
- stable transition identity for dawn/day/dusk/night or project equivalents
- persistence/suspend behavior
- list of authorized effect consumers

## Ownership

`day-night` owns canonical world-time state and transition events. Lighting, spawn schedules, stealth, weather, quests and audio consume that state through their own skills. It does not rewrite combat clocks or save bytes.

## Rules

1. A transition is emitted once for a given state boundary/revision; resume or duplicate callbacks cannot replay it accidentally.
2. Time skips, sleeps and scripted jumps declare source and resulting transition sequence.
3. Save/load restores canonical time plus policy revision; presentation interpolations are not the source of truth.
4. Systems may ignore world time or depend on it according to project policy; neither choice is universal.

## Acceptance

Given the same `time_cycle_id`, revision, clock source and start state, the same canonical time and transition identities result. Consumers can change presentation or schedules without becoming a second time owner.
