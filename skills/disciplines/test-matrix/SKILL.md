---
name: test-matrix
description: What kind of test this build needs. Ask smoke vs functional vs regression vs combo vs playtest. A green unit test is not a stranger-clear. Combinations beat single-button taps.
---

# Test matrix

Ask the column:

| Column | Question it answers |
|---|---|
| smoke | Does this build boot and reach play? |
| functional | Does this verb do what the row says? |
| regression | Did yesterday's green stay green? |
| combo | Do two legal inputs still work together? |
| playtest | Can a stranger finish the slice? |

Smoke ≤ 10 min. Playtest is gameplay-validation / real-input. Do not file a smoke pass as a clear.

## Rules

1. Write build, platform, input, difficulty, debug-on/off on every row. See debug-slate.
2. Regression is a published list of last week's accepts, not "click around."
3. Combo rows beat isolated buttons. Move+look, attack+menu, pad-unplug mid-swing. See input-combo-test.
4. Fail closed: a crash in smoke stops playtest. A playtest fail does not rewrite the combat clock.
5. Telemetry-events may count starts. They do not prove a clear.

## Accept

A report names the column, the devices, and what was not run. "Tests passed" without a column is not an accept.
