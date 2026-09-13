---
name: face-morph
description: Use when facial blendshape/morph, viseme, FACS-like, look/blink or stylized expression channels need a stable cross-asset schema, neutral baseline, ranges and LOD/fallback behavior without affecting gameplay collision.
---

# Face morph

Face morphing is **presentation**. Gameplay hurtboxes, targeting and character identity rules do not derive from transient expression weights.

## Compatible schemas

`facs-52` | `viseme-15` | `stylized-few`

These labels describe possible channel sets; the actual exported names and count are project/asset data.

## Morph schema

Publish stable channel IDs/names, **neutral** value/baseline, valid **range**, combination/clamp policy, source mapping (speech/expression/creator), missing-channel fallback and LOD policy.

Evaluation may run at render/audio/presentation rate or another declared face update rate. It must not be forced onto the gameplay logic tick merely to look deterministic. Logical dialogue/speech events can timestamp inputs while interpolation remains presentation-side.

## Rules

1. Stable semantic channel identity survives export/import/LOD even when a lower LOD omits channels.
2. Viseme/expression weights combine through a published clamp/normalization/additive policy rather than uncontrolled summation.
3. Missing channels degrade to neutral/fallback; they do not crash or remap silently to unrelated expressions.
4. Creator sliders (`avatar-create`) may map to persistent base-shape channels, while transient facial animation remains separately identifiable.
5. Expression weights cannot resize combat hurtboxes or sockets unless a separate gameplay/body contract explicitly owns such morphology.

## Accept

Round-trip neutral and representative extremes/combinations across supported assets/LODs, recording stable channel IDs, ranges and fallback. Expression playback may differ in presentation sampling but does not change gameplay collision/state.
