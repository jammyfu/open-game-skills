# Playtest lessons (cases, not rules)

Project names, map pins, and one-off percentages live here. Skill bodies stay portable.

## What a layered test is allowed to claim

Logic tests, teleports, cleared rooms, and forced boss phases prove a *unit* works. They do not prove a new player can start → learn → fight → reward → next hook → fail → ending.

If a recording used debug unlock flags, label it **challenge clip with altered unlocks**, not a natural clear.

## Split the blame

| Bucket | Examples |
|---|---|
| Game defect | combo does not recover after hitstun, look and lock disagree |
| Player / strategy | died because they stood in the paint |
| Test setup | session lost, pointer lock missing, wrong save |
| Automation | auto-play lock target flipped, navmesh blocked the bot |

Auto-play lock inconsistency, path blocks, and a dropped browser session do **not** prove the difficulty column is wrong.

## Measure one bucket

A collision-candidate cull that cuts *sim CPU on one scene* is a real method. Do not expand it to “the whole game is 59% faster”. Report scene, resolution, backend, and which clock you timed.

## Browser input is a combination

Move working on a phone does not prove look works. A menu hotkey that the game eats is a menu-flow bug. Pointer Lock missing needs a published fallback (`input-design`).

## Capture honesty

Keep the source take. If you cut a load or speed up a walk, say so on the clip. Ending and difficulty claims need a frame that shows them.
