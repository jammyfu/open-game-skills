---
name: input-design
description: Use when gameplay needs a semantic action grammar, context priority, tap/hold/release behavior, rebinding rules, or clean ownership across play and menu contexts.
---

# Input design

Define **semantic actions first**, then map devices to them.

Choose a grammar:

| Column | Grammar |
|---|---|
| few-buttons-context | context action resolves from an explicit priority list |
| orthogonal-fight | attack actions map to distinct move classes |
| hotbar-abilities | slot actions; queue/GCD timing remains in action-feel |

## Rules

1. Tap/hold/release semantics are action-specific data. Do not universally declare every tap a commitment or every hold a charge.
2. Physical buttons may be reused across mutually exclusive contexts when the action map makes the transition unambiguous. Within one active context, conflicting semantic actions require an explicit priority/chord rule rather than an accidental duplicate bind.
3. A context action publishes resolution priority (for example interact/grab/talk/mount) and the candidate evidence used to choose it.
4. Rebinding preserves semantic actions, required chords, accessibility alternatives and conflict detection; labels alone are insufficient.
5. Buffer/cancel timing belongs to `action-feel`; jump forgiveness belongs to `jump-leniency`.
6. Opening a menu transfers ownership from gameplay actions to `menu-flow`, releases transient look/pointer-lock state through the runtime adapter, and prevents held verbs from leaking across contexts.
7. Focus/device loss produces semantic releases/reset, not a stuck hold. Browser-specific lifecycle events belong to `browser-input`.
8. Multi-touch/gamepad/keyboard layouts are device adapters for the same semantic grammar; a platform may expose different physical mappings without changing the action meaning.

## Accept

For every supported device/context, print the active semantic action map and conflict report. Test tap/hold/release, context-priority ties, rebind collisions, menu transition, focus/device loss and simultaneous touch move/look when applicable. Returning from a context change does not synthesize a stale press or hold.
