---
name: vehicle-mount
description: Use when entering, controlling, transforming or exiting a mount/vehicle needs one ownership handoff, stable mount session, input/camera transfer and a safe exit search across the project's valid locomotion surfaces.
---

# Vehicle mount

Ask: `ride-follow | drive-cabin | transform-morph`.

## Ownership

This skill owns rider-to-vehicle control handoff and mount session state. `input-design` owns bindings, camera skills own camera behavior, physics owns body simulation, and `racing-feel` is used only when its vehicle-response model is actually relevant.

## Contract

Publish:
- stable `vehicle_id`
- `mount_session_id`
- rider/controller owner before and after transition
- enter/exit/abort phases
- input and camera handoff points
- collision/attachment policy
- safe-exit query policy

Exactly one authority controls rider locomotion at a time. Duplicate enter/exit requests for the same session are idempotent.

A safe dismount target is not universally navmesh. It may be authored ground, water, air, platform or another locomotion surface; the project query must validate clearance and the next movement mode.

## Acceptance

Enter/exit under interruption, unavailable vehicle, streaming change or blocked exit leaves one legal control owner and one valid rider state. No duplicate inventory/grant/state transfer occurs, and failed exit reports why no safe target was found instead of clipping or teleporting silently.
