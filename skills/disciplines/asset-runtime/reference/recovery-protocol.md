# Graphics-resource recovery protocol

A context/device failure is not a scene restart and not a purchase/settlement event. `game-state-flow` owns whether gameplay pauses, continues headless or returns to a safe menu. `browser-input` owns transient input reset; online games may not locally pause the authoritative simulation.

## Two identities, two lifetimes

Keep content identity/CPU reconstruction data separate from GPU-generation handles. A live logical lease may survive renderer loss while its old buffers/textures cannot. Track both scene/consumer epoch and device generation. Reject a late upload when either no longer matches; do not attach old-generation handles after recovery or resurrect a scene that exited while recovery was pending.

Retain a bounded reconstruction recipe: content hashes, dependency graph, descriptors, loader/decoder configuration and a policy for retained CPU data versus refetch. Account for peak memory during overlap. A network outage plus discarded CPU data may block recovery; expose that fact instead of spinning indefinitely.

## Ordered recovery

1. Enter a named recovering state, stop invalid GPU submissions, record failure reason/generation and preserve the authoritative game state under its owner's policy.
2. Coalesce repeated loss notifications into one recovery attempt per generation. Bound attempts, backoff and total time. An intentionally destroyed device/session is terminal, not an instruction to recreate it forever.
3. Recreate the adapter context/device and dependency-ordered resources from the declared recipe. WebGL restored resources and WebGPU new-device resources must be treated as new handles; use supported engine restoration hooks rather than racing a second manual restoration manager.
4. Verify required upload/decode resources and one valid rendering probe before activating the recovered view. Optional decoration can use a declared fallback; required collision/gameplay data cannot be replaced with an invisible missing floor.
5. Resume or rejoin through `game-state-flow`. Clear stale held input via `browser-input`, retain lease ownership, and ensure listeners, update loops and one-shot effects are not duplicated. A recovered frame must not replay grants, purchases or settlement.

## Acceptance matrix

Faults: loss while idle, mid-load, after upload, during scene exit and repeatedly during recovery; optional versus required missing resource; offline refetch; explicit device destroy. Verify current-generation attachments only, original state/settlement identity, surviving consumer leases, exactly one active render loop and bounded memory after recovery.

Use a supported real context-loss mechanism when available. A manually dispatched DOM event checks event wiring only, not GPU invalidation. A mocked device promise checks orchestration only. Record actual device/browser/engine, failure mechanism, attempts and resource counters; keep hardware recovery not-run unless executed.

## Primary references

[WebGL restored event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextrestored_event), [WEBGL_lose_context](https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_lose_context/loseContext), and [GPUDevice.lost](https://developer.mozilla.org/en-US/docs/Web/API/GPUDevice/lost). Support and engine-owned restoration behavior must be verified for the target version.
