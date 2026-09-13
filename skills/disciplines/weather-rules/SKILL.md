---
name: weather-rules
description: Use when weather changes world state or gameplay-relevant conditions and the project needs stable weather identity, transition rules and delegated effects separate from visual particles.
---

# Weather rules

Ask the mode: cosmetic, authored-state, stochastic-state, region-driven, hybrid, or existing.

## Contract

Publish:
- stable `weather_state_id` and `weather_revision`
- source/transition policy and duration semantics
- affected regions or scope
- canonical properties exposed to consumers
- effect owner for each gameplay consequence
- persistence/replay behavior and RNG stream when stochastic

## Ownership

This skill owns canonical weather state and transitions. Traction, stealth, chemistry, navigation, audio and VFX consume weather properties through their own systems. Presentation is not the rule oracle.

## Rules

1. Visual density/quality may scale independently without changing canonical weather state.
2. A weather transition has stable identity and cannot apply the same gameplay consequence twice after resume/replay.
3. Stochastic selection uses `rng-seed`; renderer order or particle count never chooses gameplay state.
4. Cross-system effects are explicit mappings to an effect owner, not ad-hoc mutations from the weather renderer.

## Acceptance

Given the same weather revision, state source and deterministic inputs, consumers receive the same canonical properties and transition identity even when particles, lighting quality or camera presentation differ.
