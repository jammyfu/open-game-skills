---
name: enemy-perception
description: Use when NPC detection, line of sight, hearing, last-known position, alert sharing, or chase acquisition/drop behavior is unstable, omniscient, or inconsistent with stealth feedback.
---

# Enemy Perception

This skill owns **evidence that an NPC can perceive**. `enemy-ai` consumes that evidence; `stealth-info` presents player-facing awareness; `collision-layers` owns collision/filter policy.

## Modes

| Mode | Evidence |
|---|---|
| cone-sight | origin + FOV/range + line of sight query |
| hear-ring | authored noise event + propagation/range rule |
| last-known | timestamped last confirmed position/evidence |
| alert-share | bounded ally notification with source and expiry |

Modes may be combined when the project requires it; do not infer omniscience from combination.

## Acquisition and release

Publish sample cadence, acquire threshold/delay, release threshold/delay, and any hysteresis. Hysteresis prevents one noisy ray or one threshold-crossing frame from flipping combat state every tick.

A sight query declares sensor origin(s), target sample point(s), range/FOV policy and line of sight geometry. Use the project's collision query filtered by `collision-layers`; do not use visibility of the render mesh as gameplay truth. Multiple sample points, partial cover, smoke, portals or special sensors are project-specific policies.

Chase persistence is also project data. Some games drop after a timer, some search a last-known point, and some encounters intentionally keep engagement until another rule ends it. Do not label long pursuit a bug without the chosen policy.

Alert sharing carries source, evidence type and expiry. It must not silently grant perfect target position forever.

## Acceptance

Record raw perception evidence and the derived acquire/release state. Test line of sight at edge angles/ranges, brief occlusion around hysteresis thresholds, stale last-known evidence, and alert-share expiry. Repeat at different render rates; results on the logical perception clock must match. A debug cone alone is not proof that acquisition/drop behavior is correct.
