---
name: fps-feel
description: Use when first-person weapon handling needs explicit hip/ADS/recoil/readiness profiles and presentation feedback while shot queries, ammo transactions, weapon swaps and bindings remain owned by their dedicated systems.
---

# FPS feel

Ask: `hip-fire | ads | recoil-pattern | swap-holster`.

## Ownership

`fps-feel` owns the weapon-handling state and presentation transform used to form a shot request. `projectile-hitscan` owns hit resolution, `ammo-reload` owns reload/ammo transfer, `weapon-swap` owns inventory weapon handoff, `input-design` owns actions/bindings, and `aim-assist` owns assist transforms.

## Contract

Publish:
- stable `handling_profile_id` + revision
- weapon state: hip / ADS / ready / recovering
- authored raise/lower/recovery transitions
- recoil/spread intent state and RNG stream when stochastic
- raw and handled aim/fire direction passed to the shot owner
- presentation-only camera/view offsets separately

ADS is not universally narrower, slower-moving, or slower-looking than hip fire; those are project data. Recoil need not update on a universal logic cadence, but any gameplay-affecting aim state must use the project's declared gameplay timebase and be replayable.

Presentation view kick occurs after/alongside the authoritative fire event and cannot retroactively change an already committed shot query.

## Acceptance

Given the same handling profile, input/aim state, gameplay timebase and RNG state, the same handled shot intent is emitted. Changing only camera/view feedback cannot change the authoritative hit result, and reload/swap interruptions delegate to their owners without duplicating a shot.
