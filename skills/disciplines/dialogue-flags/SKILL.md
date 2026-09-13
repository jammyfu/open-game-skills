---
name: dialogue-flags
description: Use when dialogue choices, conditional lines, relationship facts, shop/gate reactions, or conversation outcomes need persistent branch state without duplicating the quest graph.
---

# Dialogue Flags

This skill owns **namespaced dialogue/conversation facts and branch conditions**. `quest-graph` owns quest structure; `save-systems` owns persistence format/versioning; `game-localization` owns localized text.

## Modes

| Mode | Effect scope |
|---|---|
| flavor-only | changes later dialogue/presentation only |
| flag-alters-shop | changes shop/reward/availability policy |
| flag-alters-gate | participates in an authored access condition |

Each flag has a stable namespaced ID such as `dialogue.vendorA.met` or a project equivalent. Do not key save state by localized line text, choice index, or transient UI order. Persist through `save-systems` with schema/migration rules.

Flags can be read by quest/shop/gate systems when explicitly referenced, but they do not become a second hidden quest graph. Effects are authored and inspectable.

Replay/alternate-choice viewing is a project feature, not a universal requirement. If conversations can be replayed, define whether flags are preview-only, rewound, forked in a lab slot, or permanently committed.

## Acceptance

Save/reload after representative choices and verify stable flag IDs and dependent outcomes. Reorder/localize choices and confirm persisted meaning does not change. A branch that affects progression must name the consuming system and migration behavior.
