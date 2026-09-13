---
name: soak-stability
description: Use when long-running play, idle/resume, repeated loading, saving, audio, networking, or content cycles may reveal leaks, hitch growth, corruption, or cumulative state drift that short tests miss.
---

# Soak stability

Choose duration and workload from the product risk, not a universal hour count.

| Mode | Example workload |
|---|---|
| active-loop | repeat representative gameplay/content cycles |
| overnight | long mixed active/idle run |
| idle-resume | suspend, background/tab-out, resume repeatedly |

## Measurement

Pin build/device/scene route/settings. Sample memory/resident resources, object/resource counts, frame-time p50/p95/p99 (or the project's percentiles), hitch counts, load/save outcomes and subsystem-specific counters over time.

Judge **trend/slope**, not only start-versus-end. Warm-up/cache growth may plateau; a persistent positive memory/resource slope or increasing hitch percentile after repeated cycles needs investigation.

Repeat save/load against the selected test slot/profile from `save-integrity`/`save-systems`; do not hardcode slot 0. Preserve the previous good generation when injecting failures. Repeated audio/network/listener setup must not accumulate duplicate handlers or loops.

Automation may drive the soak, but label it as automation and do not equate endurance with a human usability/clear test.

## Acceptance

Publish duration, workload count, restart/resume events, memory/resource trend, p95/p99 frame-time or hitch trend, save/load success/failure and any recovery actions. Resume must restore valid input/lifecycle state. A run passes only the measured stability contract; it does not prove unrelated gameplay quality.
