---
name: asset-runtime
description: Use when assets load twice, stale callbacks resurrect objects, shared textures disappear on scene exit, or repeated scene changes leak memory or block interaction.
---

# Asset runtime

## Scope

Own resource acquisition, sharing and release, not model authoring, atlas packing or deciding which world cells should exist. Inspect the loader/engine version and current asset manager before adding another. [Model pipeline](../../assets/model-pipeline/SKILL.md) owns export; [performance-budget](../performance-budget/SKILL.md) owns target limits.

## Modes

| Mode | Lifetime |
|---|---|
| scene-owned | handles end when the owning scene ends |
| shared-cache | resources outlive one scene through explicit leases |
| staged-load | request, fetch, decode/upload and activation are distinct gates |

## Procedure

1. Publish stable asset IDs and a versioned manifest: content identity, type, dependencies, estimated budgets and failure fallback. Resolve dependencies and detect cycles before activation. A filename is not a stable gameplay ID.
2. Deduplicate in-flight loads by asset identity/version, but give each consumer its own lease. Record owner and epoch. Releasing one consumer must not cancel another consumer's shared request or dispose its texture. Dispose only when ownership and the explicit cache policy permit it.
3. Publish request states: pending, ready, failed, cancelled and released. Cancel underlying work only when supported and unneeded; always guard result delivery with consumer epoch/liveness. Clean up an orphan result without attaching it to an obsolete scene. Bound retry/backoff and distinguish a missing optional decoration from a required collision asset.
4. Keep fetch/decode readiness separate from instantiation, GPU upload and gameplay activation. Do not block the interaction thread waiting for a pending result. In Godot, check threaded-load status before retrieving a resource that must not block. Respect the engine's main-thread requirements.
5. Release listeners, workers, audio and GPU handles as well as scene nodes. In Three.js, removing a node does not dispose its geometry/material/texture. Track shared texture ownership independently. Context/device loss needs an explicit reload policy, not a promise that disposed resources survive.

## Outputs

Adapt the [resource contract](assets/contract.example.json): manifest, lease/epoch table, loading state machine, failure policy, disposal inventory and measured load/churn trace. A cache budget and eviction policy must name the target device; examples are not measurements.

## Acceptance

Two scenes share one texture: unload one and the other still renders. Leave during a pending load and check that no stale actor appears. Repeat the cycle with failed loads, cancelled consumers and a cache version change. Compare live handles and memory after warm-up and reclamation against a declared tolerance, not an expectation that all caches instantly return to zero. [Cases](assets/evals.json) are not-run until executed on the named adapter/device.

## References

[Three.js cleanup](https://threejs.org/manual/en/cleanup.html) documents explicit GPU-resource disposal. [Godot background loading](https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html) explains why retrieving a pending threaded resource can still block. These APIs are adapter details, not an engine-neutral implementation supplied by this skill.
