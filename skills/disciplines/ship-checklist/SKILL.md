---
name: ship-checklist
description: Use when a candidate build needs a release-readiness decision that assembles QA, platform, lifecycle, save, localization, capture/store, migration, rollback, and known-risk evidence without copying private vendor checklists.
---

# Ship checklist

This skill is an evidence aggregator, not a second QA taxonomy or store API manual.

## Release manifest

A release candidate records:

```text
release/build ID + commit/version
target(s) and distribution channel/config
artifact identity
required game-qa evidence card references
platform-targets / cert-handoff evidence
save/migration/rollback status when applicable
localization/accessibility/store/capture evidence when applicable
open blocker list + explicitly accepted risks
untested remainder
release decision + approver/source
```

## Rules

1. `game-qa` owns QA passes; this checklist consumes their evidence rather than restating “tests passed.”
2. Required first-run experience is project-defined. Do not assume every game must finish one particular teach room.
3. `cert-handoff` owns lifecycle event behavior; current vendor/store requirements stay in authorized external sources and are referenced by version, not copied here.
4. Store/media assets use `game-localization` and `gameplay-capture` provenance for the exact build/language represented.
5. A blocker is closed by evidence tied to this build or is explicitly accepted/deferred; it does not disappear because another target passed.
6. Release/rollback compatibility follows `patch-cadence`, saves and entitlement migrations follow their domain owners.

## Accept

The **release manifest** lets an independent reviewer identify the exact build, every target, evidence used, remaining blockers/risks, untested areas and the basis for the release decision.
