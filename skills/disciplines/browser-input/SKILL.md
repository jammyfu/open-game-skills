---
name: browser-input
description: Use when a browser or embedded web game must survive Pointer Lock changes, tab visibility, pointer cancellation, touch, focus loss, or gamepad connect/disconnect without stuck actions.
---

# Browser input

This skill adapts browser/device events into the semantic actions defined by `input-design`. It does not redefine the action grammar.

## Pointer and focus lifecycle

1. Pointer Lock is state, not an assumption. Observe `pointerlockchange`; handle `pointerlockerror`; publish a usable non-lock fallback when core look needs one.
2. On `visibilitychange` to hidden and on relevant window focus loss, synthesize semantic releases/reset for held transient actions. On return, require fresh input edges rather than replaying stale key/pointer state.
3. Treat `pointercancel` and lost pointer capture as termination of the affected pointer gesture. Mobile browser scrolling, app switching, orientation changes or palm rejection can cancel a pointer without `pointerup`.
4. Menu/modal transitions release gameplay look/gesture ownership before widgets consume input.

## Touch and gamepad

5. Track touch/pointer IDs so movement and look can coexist; one canceled pointer must not erase unrelated active pointers unless the platform/browser cancels them too.
6. Handle `gamepadconnected` and `gamepaddisconnected`, but also poll current pads through the runtime's supported Gamepad API path because availability can depend on page focus/user interaction. A disconnected pad releases its held semantic actions.
7. Gamepad button/axis indices are device data. Map through an explicit profile/deadzone layer; do not assume one controller layout for every device.
8. A runtime may not support every browser API equally. Missing Pointer Lock, touch, gamepad or haptics becomes a capability/fallback decision in `platform-targets`, not silent failure.

## Accept

Desktop: deny Pointer Lock, acquire it, press Escape to lose it, alt-tab/hide/return, and disconnect/reconnect a gamepad; no action stays held and look has a declared fallback. Touch: move and look simultaneously, then force `pointercancel` for one pointer and verify the other action remains correct. Record actual browser/device combinations; static event wiring alone is not a behavioral pass.
