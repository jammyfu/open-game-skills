---
name: game-qa
description: >
  How to test a game, not how to play it. Use when a build is "done" but
  unproven, when a fix may have broken last week's verb, or when ship is
  claimed from a debug session. Stacks on gameplay-validation. Does not
  copy a platform TRC.
---

# Game QA

Ask the column. One column per pass. A green functional pass is not a soak.

| Column | Question |
|---|---|
| smoke | does the build boot, start, pause, quit? |
| functional | does this verb do what the row says? |
| regression | does yesterday's pass still pass after the fix? |
| playtest | can a stranger finish without a wiki? (gameplay-validation) |
| soak | does a long idle / grind leak or hitch? |
| device-matrix | does the named hardware class hold the budget? |
| input-matrix | kb / pad / touch / hot-plug / rebind all work together? |
| interrupt | suspend, resume, disconnect, overlay — still a game? |

## Build card (every pass writes one)

```
build id + commit
column
device / input
cheat-flag (lab or story)
result + evidence path
untested remainder
```

No card, no claim. A clip with debug unlock is adjusted-challenge (gameplay-capture).

## Order

```
smoke → functional on the new verb
     → regression on the last green suite
     → playtest / real-input
     → soak + device-matrix before ship talk
```

Do not start ship talk on soak-fail or on a lab-slot clear.

## Iron rules

- Separate: game defect, player strategy, harness failure, tool crash.
- Fixes get a regression row. "Works on my machine" is not a row.
- Save during combat, talk, and zone edges (save-integrity). One slot must not clobber another.
- Interrupt column: controller pull, app background, overlay. Resume on the same verb, not a new game.
- Platform store / console cert is interrupt + save + crash-free on a published matrix. Do not paste a vendor TRC into the skill.
- Automation can own smoke and some functional. It cannot own playtest.

## Accept

A reader can say which column ran, on which build, with which cheat-flag. Remaining holes are listed. Ship is a card, not a feeling.
