# Public example patterns: inspect before adopting

Use examples to study construction, not to replace the approved character model or its native action reference. Inspect exported source and record the commit and file hash. A directory called `8.x`, a live GIF or a valid parser result is not evidence of target-runtime compatibility.

## Spineboy: mixed attachment construction and planted feet

Primary sources: [official setup explanation](https://esotericsoftware.com/spine-examples-spineboy), [public export](https://github.com/EsotericSoftware/spine-runtimes/blob/e7dc1435fa4a0083ab431f1b28e083c14a1f5c68/examples/spineboy/export/spineboy-pro.json).

The inspected 4.2.22 export has 67 bones and 52 slots. Front/rear thighs and upper arms are region attachments. Front shin is an unweighted mesh; head, torso and feet include weighted meshes. Front fist has open/closed region alternatives. This is a useful construction example: not every surface needs multi-bone weights. Its head deformation is not a requirement for a character with a fixed face/proportion lock.

Keep the hip independent from foot controls. Spineboy's two-bone leg IK evaluates before the single-bone foot constraint. Adapt that dependency structure to the game's fixed contacts; preserve reviewed limb lengths and knee bend direction. Evaluate soles in rendered pixels as well as control coordinates.

## DragonBones: slots and IK, with a compatibility check

Primary sources: [repository](https://github.com/DragonBones/DragonBonesJS), [IK demo](https://github.com/DragonBones/DragonBonesJS/blob/64b6c69ae35777c2404be68c9192e2c56906079e/Pixi/Demos/8.x/src/InverseKinematics.ts), [slot replacement](https://github.com/DragonBones/DragonBonesJS/blob/64b6c69ae35777c2404be68c9192e2c56906079e/Pixi/Demos/8.x/src/ReplaceSlotDisplay.ts).

Study explicit foot targets, aim overlays and slot replacement. The inspected `8.x` files still refer to `PIXI.interaction.InteractionEvent` and `event.data.global`; do not import them as verified Pixi 8 adapters. The repository's MIT licence applies to its code; inspect asset-specific provenance before redistribution. Spine examples/runtimes have separate terms described in [tool-adapters.md](tool-adapters.md).

## Distinguish stretch demonstrations from fixed anatomy

[Stretchyman](https://esotericsoftware.com/spine-examples-stretchyman) explicitly enables IK Stretch and uses a path-driven chain to make elastic limbs. Do not transfer that setup to a locked-proportion fighter. Use authored alternate drawings for foreshortening and large angle changes; keep a deformation experiment visibly separate from accepted art.

## Apply to a layered fighter

1. Prepare all required elements at one density, with named ownership, full contours and hidden joint overlaps. Inspect the complete static assembly before binding. Equal colours cannot distinguish adjacent hair/clothing or crossing legs.
2. Keep face, fists and limb cores rigid where the approved model requires it. Limit weighted transitions to reviewed joint regions. Roots of hair follow the head; add secondary motion only where the painted overlap supports it.
3. Author attachment/view alternatives and their switch times for fist shape, turns and foreshortening. Declare near/far slot order per view. A fixed setup slot list alone does not solve every action's occlusion.
4. Review isolated parts and assembled contours on light/dark backgrounds, at game scale and source detail. Check texture filtering seams, knee/hip holes and unintended neighbouring material. Static source equality does not prove moving seams are closed.
5. Validate fixed proportions, surface strain, planted contacts, switch continuity, normal/slow playback and native timing separately. Keep source inspection, target-runtime verification and visual acceptance as separate statuses.
