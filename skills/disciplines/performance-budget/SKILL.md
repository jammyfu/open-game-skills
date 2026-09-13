---
name: performance-budget
description: Use when a project needs explicit frame-time, memory, latency, loading, or frame-pacing targets per platform before optimization decisions can be judged.
---

# Performance budget

This skill owns **targets and measurement contracts**. `performance-optimization` owns diagnosis and changes used to meet them.

## Budget columns

Do not hardcode one simulation rate for every project. Publish the actual project clocks and presentation targets.

| Example mode | Presentation target | Simulation contract |
|---|---|---|
| stable-60 | 60 Hz target | project-selected fixed/variable simulation documented separately |
| stable-30 | 30 Hz target | simulation rate remains an explicit project decision |
| unlocked-floor | uncapped/VRR with floor | simulation contract unchanged by display refresh |
| multi-profile | per-device quality profiles | same gameplay rules; clocks listed explicitly |

## Metrics

A useful budget includes more than average FPS:

- CPU main-thread and worker critical-path time;
- GPU frame time at a named resolution/settings profile;
- frame-time **p50 / p95 / p99** (or published percentile set) and worst hitches;
- frame pacing / missed-present rate;
- input-to-visible-response latency when feel is latency-sensitive;
- allocation/GC stalls, memory resident peak and memory trend;
- streaming/IO latency and loading hitches.

CPU and GPU work may overlap, so do not add independent CPU/GPU numbers as if they were automatically serial. Name the critical path and presentation cadence.

A fixed gameplay tick can preserve logical timing while 30 Hz and 60 Hz rendering still differ in presentation latency, visual sampling and frame pacing. Do not claim identical feel solely because logical state is identical.

## Measurement contract

Pin device, build configuration, scene/route, resolution, quality settings, backend/API, capture duration and warm-up. Report percentiles and sample count/window. Compare like with like; a one-scene gain is not a global budget result.

## Acceptance

Run the representative route on every shipping performance profile. Confirm published percentile/frame-pacing/latency/memory targets and record the specific failing bucket when a target misses. Logic outcomes may remain deterministic across render profiles, but presentation latency differences are reported rather than hidden. Unmeasured platforms remain `not-run`.
