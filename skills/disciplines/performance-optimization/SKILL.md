---
name: performance-optimization
description: Use when measured CPU, GPU, memory, allocation, streaming, or frame-pacing data misses an existing performance budget and the bottleneck must be isolated before changing quality or gameplay code.
---

# Performance optimization

Consume the targets and measurement setup from `performance-budget`; this skill does not invent a second budget.

## Diagnose the critical path

1. Reproduce the miss with the same device/build/scene/settings used by the budget.
2. Inspect p50/p95/p99 frame-time and hitch traces, not only averages.
3. Determine whether the present interval is CPU-bound, GPU-bound, synchronized/stalled, allocation/GC-bound, streaming/IO-bound, or memory-pressure-driven.
4. Within the failing side, find the dominant critical-path bucket before selecting a lever.
5. Change one bounded cause, rerun the identical capture, and compare both the target metric and guardrails.

CPU and GPU timings overlap; optimize the path that gates presentation rather than summing unrelated buckets. A GPU reduction does not improve frame time when the frame is still CPU-bound, and vice versa.

## Levers

Typical levers include culling/off-screen work, batching/submit cost, overdraw, shadow/reflection cost, particle counts, simulation/AI frequency where design permits, allocation removal, streaming scheduling, LOD/impostors, texture/resolution policy and shader/material complexity. Pick based on evidence, not a universal order.

Do not change hitstop, input windows, acceleration, cooldowns or other gameplay timing to disguise a performance miss. Quality reductions are named costs and must still satisfy readability/accessibility guardrails.

## Acceptance

For every claimed optimization, report before/after p50/p95/p99 (or the project's percentile set), critical-path bucket, scene/device/settings, and relevant guardrails such as memory or image/readability quality. A speedup is accepted only when the original budget miss improves under the same measurement contract without moving the problem into another critical bucket.
