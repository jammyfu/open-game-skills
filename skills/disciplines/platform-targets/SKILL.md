---
name: platform-targets
description: Use when one game targets multiple hardware, browser, mobile, console, handheld, input, display, thermal, storage, or lifecycle capability classes and needs explicit per-target budgets and feature fallbacks.
---

# Platform targets

This skill describes target **capability** profiles. `performance-budget` owns measured CPU/GPU/frame/latency budgets; engine adapters own engine/version-specific implementation.

## Target profile

For each target record applicable fields rather than assuming one universal set:

```text
target id + hardware/runtime class
supported input/display modes
performance-budget reference
memory/storage/download constraints
thermal/power constraints when applicable
safe-area/text/accessibility constraints
lifecycle/network capability
feature-quality fallbacks
unsupported capabilities
```

Frame-rate targets, resolution targets, quality modes and thermals are project data. Do not hardcode 30/60, unlocked frame rate, or a particular menu location for displaying budgets.

## Rules

1. Preserve published gameplay invariants across comparable targets; bit-identical simulation is required only when the project/netcode contract requires it.
2. Input availability and remapping follow `input-design`; native target inputs must have a declared path for required actions.
3. Presentation may scale to meet the target's `performance-budget`, but gameplay-rule changes require their own explicit product/design contract.
4. Suspend/dock/browser-tab/device-change behavior delegates to `cert-handoff`/engine lifecycle where applicable.
5. Missing capabilities use declared fallbacks or are marked unsupported; never silently pretend the feature ran.

## Accept

The device/target matrix names measurable budgets and capabilities, verifies the supported interaction path on each target, and records which features degrade, fallback, or remain untested.
