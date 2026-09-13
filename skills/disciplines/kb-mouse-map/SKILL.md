---
name: kb-mouse-map
description: Use when a project needs a keyboard/mouse role preset for movement, look, aiming, menus or genre conventions. It maps semantic actions from input-design to device controls; it does not own gameplay verbs or require one universal WASD/LMB/RMB layout.
---

# Keyboard × mouse map

Choose a project preset such as `fighter-plane | fps-look | tps-orbit | twin-stick-kb | click-world | race-line | platform-side | menu-heavy | build-sim`, or define a project-specific mapping.

## Ownership

`input-design` owns semantic actions, contexts, conflicts and rebinding rules. `kb-mouse-map` is a device/preset layer that proposes default physical bindings and mouse roles for those actions.

## Contract

Publish:
- stable `input_preset_id` + revision
- device capabilities detected/required
- semantic action → physical binding map
- pointer role: look / aim / select / camera / unused / project-defined
- context-specific conflicts and fallback actions
- optional accessibility alternatives

WASD, Space, LMB, RMB, Esc, extra mouse buttons and cursor capture are conventions, not mandatory universal core controls. One physical control may participate in different non-overlapping contexts when `input-design` explicitly permits it.

## Runtime rules

1. Rebinding changes physical bindings, not semantic action identity.
2. Device loss/hot-plug is handled by the runtime/device layer; this preset supplies valid fallback mappings where authored.
3. Pointer/cursor behavior for browsers delegates lifecycle details to `browser-input`.
4. A preset never changes hitboxes, cancel windows, camera collision or gameplay time.
5. Conflicts are validated per active input context rather than by a blanket one-button-one-job rule.

## Acceptance

For a selected preset revision and active context, every required semantic action has an authored supported binding or an explicit unsupported result. Remapping or switching device presets changes controls without changing gameplay action IDs or timing semantics.
