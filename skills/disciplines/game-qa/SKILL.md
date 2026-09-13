---
name: game-qa
description: Use when a game build, feature, regression, device/input combination, interruption path, soak run, or release claim needs a named QA pass with inspectable evidence.
---

# Game QA

This skill **owns the QA pass taxonomy** and the evidence card used by QA-oriented compatibility entries such as `test-matrix`. It does not own gameplay success criteria (`gameplay-validation`), performance budgets (`performance-budget`), or vendor certification requirements.

## Pass taxonomy

| Pass | Question |
|---|---|
| smoke | Can this exact build boot and reach the intended entry path? |
| functional | Does the named feature satisfy its published contract? |
| regression | Do selected previously-green contracts remain green? |
| combination | Do interacting features/inputs/lifecycle events still compose? |
| playtest | Can the intended player complete the target experience? |
| soak | Does the build remain stable over the published duration/workload? |
| device-matrix | Does the target device/capability class meet its published contracts? |
| input-matrix | Do supported devices, remaps, hot-plug and context changes behave correctly? |
| interrupt | Does suspend/resume, focus loss, device loss, overlay or equivalent lifecycle recover legally? |

A project may add passes, but each pass gets a unique name and acceptance contract rather than redefining another pass silently.

## Evidence card

Every executed row records at least:

```text
case/pass id
build id + commit/version
platform/target + device/input
configuration/difficulty + QA/debug state
result: pass | fail | blocked | not-run
artifact/evidence reference
known deviations + untested remainder
```

`pass` means the stated row ran and met its criteria. A unit/static check, screenshot, capture, or telemetry counter cannot be substituted for a different evidence class.

## Rules

1. Separate product defect, expected design, player strategy, harness failure, environment/setup failure and tool failure.
2. A fix gets a stable regression case ID when recurrence would matter.
3. Combination coverage is selected from real interaction risk, not an assertion that every pair must be tested.
4. `gameplay-validation` owns human/agent completion claims; automation may support them but does not silently convert functional evidence into playtest evidence.
5. `cert-handoff` provides lifecycle/cert-relevant event contracts; platform/vendor requirement sources remain external and versioned.
6. Release decisions consume these cards through `ship-checklist`; QA itself does not claim “ship” because one pass is green.

## Accept

A reviewer can identify the exact build, target, pass, configuration, result, evidence and untested remainder. Re-running the same case against another build creates another evidence record rather than overwriting history.
