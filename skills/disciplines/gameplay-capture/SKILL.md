---
name: gameplay-capture
description: Use when gameplay video, screenshots, store/trailer footage, QA evidence, or completion claims need capture provenance that distinguishes natural play, assisted/debug setup, and edited presentation.
---

# Gameplay capture

Capture is evidence/presentation plumbing; it does not decide whether gameplay is correct.

## Capture record

Assign a stable **capture ID** and record:

```text
capture ID
build ID + commit/version
target/device/input
claim type: natural-play | assisted/QA | feature-demo | presentation-only
configuration/difficulty/loadout
QA/debug session ID when applicable
source take references
edit manifest: cuts, retimes, overlays, compositing, audio replacement
export artifact + format
```

## Flow

1. State the claim the capture is allowed to support before recording.
2. Use `debug-slate`/`save-integrity` provenance for modified state instead of inferring legitimacy from the picture.
3. Preflight picture/audio/resolution/storage and capture-device capability.
4. Preserve source take references. Recorder control may be integrated or separate; do not hardcode one button/control topology.
5. Record every material edit. An edited promotional sequence is valid presentation evidence but is not silently reused as an unedited gameplay-clear claim.

Automation, navigation, session or recorder failures are capture/setup failures unless a different owner proves a gameplay defect.

## Accept

A reviewer can trace the exported artifact back to capture ID, exact build, source take(s), state provenance and edits, and can tell which claims the artifact does and does not support.
