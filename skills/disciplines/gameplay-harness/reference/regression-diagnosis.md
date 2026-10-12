# Replay regression diagnosis

## Comparable experiment first

Pin candidate build, adapter, oracle, clock configuration, input tape, initial-state/save digest and RNG algorithm/state identity. Keep uncontrolled device/runtime differences in the full session manifest. Split logic, render, native-input and human observations. Do not infer no-skill model performance from an intentionally broken implementation.

The [offline comparator](../scripts/trace_compare.py) consumes a **normalized export**, not arbitrary existing harness reports. An adapter must export the declared stable state and ordered events to [trace v1](../assets/trace.example.json). This does not change a project's clock or add a production adapter automatically.

```sh
python skills/disciplines/gameplay-harness/scripts/trace_compare.py baseline.trace.json candidate.trace.json --output /new/comparison.json
```

Python 3.10+, standard library only. The example has synthetic commit/hash declarations; it is not executed engine evidence. An output parent must exist and be trusted. Existing outputs are refused; baseline and candidate are read-only.

Exact top-level keys: `schema_version: 1`, `build` (40-character lowercase commit SHA declaration), `context`, `frames`. Context has exactly six nonempty strings: `adapter`, `oracle`, `clock`, `tape_sha256`, `initial_state_sha256`, `rng`. Hash fields are lowercase SHA-256. Include clock substep/overflow policy in the clock identity and RNG algorithm/version/stream state in the RNG identity. No RNG uses the explicit string `none`.

Frames have exactly `tick`, `state` object, and ordered `events` array. Event objects require a nonempty `id` and may carry payloads. Ticks are contiguous nonnegative integers; choose an adapter boundary that provides them. Export only the project's stable oracle subset. Quantize/canonicalize unstable floats in that versioned adapter, not through a hidden tolerance in this comparator. Map-key order is irrelevant; event/array order, missing versus null, boolean versus number, and numeric representation are significant. NaN, duplicate keys and over-deep JSON are rejected. Limits: 16 MiB per file, 100000 frames, 64 nested state/event levels.

Different builds are expected. Different compatibility context blocks comparison before any frame is compared. A shortened trace fails; it is not a shorter passing test. A failure records the first tick and JSON-pointer field with expected/observed values and presence flags. Context equality and input hashes do not prove authenticity: this script does not open the tape/state artifacts, authenticate commits, execute candidates, or certify provenance.

Exit codes: 0 = exported traces match; 1 = comparable mismatch; 2 = incompatible, malformed or I/O-blocked. `runtime_validation` stays `not-run` for this offline invocation. `failure_attribution` stays `unknown`; an assertion mismatch alone cannot identify game versus harness.

## Turn failures into reusable cases

Retain the original failing tape and raw evidence. Create a reduction copy and remove chunks of **semantic input** only when the same oracle violation reproduces. Preserve required setup and fresh input edges; deleting arbitrary intermediate state snapshots is not a valid reproduction. Bound the reduction budget. This is a documented workflow, not an implemented reducer.

Use one known-bad mutation per invariant (double grant, frame-driven logic, stale callback, premature shared disposal). Require the intended assertion to fail while setup still succeeds. Record repeated runs and the full denominator; timeouts and blocked cases are not passes. Add metamorphic cases only with a justified invariant, such as changed render cadence or irrelevant actor iteration order. Do not assume changed difficulty, physics backend or random seed should be identical.

Update a golden only with an explicit behavior-change reason and review. Archive old evidence against old source hashes. A revised Skill remains unevaluated in its changed scope until a real model/engine run uses that exact context.
