---
name: minimap-pins
description: Use when a minimap needs to present authorized player/system pins, fog, radar or compass information with stable IDs and lifecycle rules. It consumes world/quest/perception truth; it does not author that truth.
---

# Minimap pins

Ask: `off | player-pins | fog-disk | radar-blip`.

## Ownership

`world-map`, quests and perception systems decide what information exists and may be revealed. `minimap-pins` owns minimap selection, deduplication, layout and presentation of that authorized information.

Each presented item records:
- stable `pin_id`
- `source_owner` and source entity/quest ID
- pin type
- visibility predicate/revision
- optional expiry/removal reason

Player pins, quest pins and threat/radar blips may coexist when the project permits them. There is no universal rule that only one active quest hook may be shown.

## Runtime rules

1. Duplicate updates for the same pin/revision are idempotent.
2. A source becoming invalid removes or hides the pin without mutating source state.
3. Occlusion/fog/stealth policies come from their owner and are not bypassed to create extra information.
4. Localization changes labels, not pin identity.
5. Turning the minimap off removes presentation only.

## Acceptance

The same authorized source state yields the same canonical pin set. Stale or unknown source IDs do not become persistent markers, and toggling/minimap layout changes cannot complete quests, reveal source state, or modify travel state.
