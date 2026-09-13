---
name: test-matrix
description: Use when an existing prompt or workflow asks for a test matrix and needs to be routed to the canonical QA pass taxonomy and combination coverage without maintaining a second QA rule set.
---

# Test matrix

This is a **compatibility entry**. `game-qa` owns smoke, functional, regression, combination, playtest, soak, device/input and interrupt pass semantics.

## Map legacy requests

| Legacy request | Canonical owner |
|---|---|
| smoke / functional / regression / playtest | `game-qa` matching pass |
| combo / interaction matrix | `game-qa` combination pass + `input-combo-test` when input-specific |
| devices / platforms | `game-qa` device-matrix + `platform-targets` |
| real completion | `gameplay-validation` evidence consumed by `game-qa` |

Do not invent fixed pass durations, universal device sets, or a second result format here. Preserve the caller's named build, target, configuration and risk boundaries when delegating.

## Accept

A matrix request resolves to `game-qa` evidence rows with stable case IDs and an explicit untested remainder. This compatibility entry adds no conflicting QA taxonomy.
