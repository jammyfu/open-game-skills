---
name: interact-prompt
description: Use when the HUD must present currently legal world interactions, semantic actions and current bindings without owning interaction truth, target priority, localization identity or gameplay execution.
---

# Interact prompt

Ask: `context-one | listed-verbs | no-prompt`.

## Ownership

The interaction/gameplay resolver supplies eligible actions, target IDs and authored priority. `input-design` supplies semantic action bindings. `game-localization` supplies stable string IDs/text. This skill only chooses and presents the authorized prompt set.

## Contract

For every prompt resolve:
- stable `target_id`
- stable semantic `action_id`
- source resolver revision
- current binding glyph/text
- stable localization string ID
- visibility/occlusion eligibility

Do not hardcode a universal interaction ordering. If multiple interactions are legal, use the project's authored priority/tie-break.

## Runtime rules

1. A stale, removed or occluded target invalidates its prompt before activation.
2. Prompt updates are idempotent by target/action/revision.
3. Focus/target churn uses project hysteresis or tie-break data; render frame order is not authority.
4. Changing language or physical binding updates presentation without changing `action_id`.
5. Executing an action belongs to the gameplay owner; showing a prompt never commits it.

## Acceptance

Before activation, the UI can identify the exact target/action/revision it is presenting. If the target disappears or a newer resolver revision wins, the stale prompt cannot fire, and remapping/localization changes never alter the underlying gameplay verb.
