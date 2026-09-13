Implement a dependency-free JavaScript ES module exporting `AssetPool` for a browser game's asynchronous resource manager. Return only the requested JSON object containing the complete source as `asset_pool_mjs`. Do not generate tests, harnesses, other files, imports, or explanatory prose.

Public interface:
- `new AssetPool(load, dispose)`, where `load(key)` may return a value or a promise or throw; `dispose(value)` synchronously releases the loaded resource.
- `pool.acquire(key, isCurrent = () => true)` returns `{ready, release}`. `ready` is a Promise. `release()` is synchronous and may be called repeatedly.
- `pool.stats` exposes numeric counters `loads`, `disposed`, and `stale`, initially zero. Count actual loader invocations, actual disposer invocations, and deliveries rejected because the consumer was released or became stale, respectively.

Functional requirements:
The key identifies an asset and its version. Concurrent consumers of that key should share one in-flight load and the same resolved object. Every acquisition has independent lifetime. Releasing one consumer must not invalidate another; the last release disposes the resolved resource exactly once. There is no long-term retention policy: an unused resolved entry is evicted. A later acquisition after eviction starts a fresh load.

A consumer can be released while loading or its `isCurrent()` callback can become false before delivery. Its `ready` must then resolve null, never a stale object. Other current consumers must remain unaffected. An orphan successful result must be reclaimed. Loading errors must reject waiting consumers and must not permanently poison future attempts for that key. Keep this non-blocking. Assume keys are strings, successful resources are non-null objects, and the liveness/disposal callbacks do not throw.

The module is instantiated by an external browser engine adapter. Do not read or modify the DOM, globals, network, process, filesystem, scoring functions, or engine state. Correctness should come from resource ownership and asynchronous lifecycle handling, not test-specific special cases.
