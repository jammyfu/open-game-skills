# Design and production decisions

## Slice and audience

`lantern-grove/r1`: desktop single-screen timing prototype, one-button hold/release, target 8 light, failure on overload, R restarts. Intended audience is a player willing to experiment with short timing windows; no audience comprehension result is available. Content excludes enemies, combat, inventory, purchasing, story progression and platform certification.

## Visual revision after review

The initial scene used repeated standalone tree sprites and a small courier, making the world read as a test fixture. User feedback rejected that scene. The revised brief called for an asymmetrical moonlit canopy, a cool waterfall vista, a warm shrine focal point, an open terrace and clearly larger character. GPT generated new environmental art; the actual engine places the character feet on the terrace and directs gathering light toward the shrine's socket. Capture comparison and rule regression are separate acceptance tasks. The revised screenshot demonstrates implementation, not universal aesthetic approval.

## Parameter and response contract

60 logical ticks/s. Reward intervals are [1,29], [30,47], [48,65] charged ticks, with gains 1/2/3. At 66, fail. Recovery is 18 ticks. These ranges encode the chosen risk/reward curve; they are not source-prescribed constants. Release creates authoritative events consumed by pose, HUD, audio and sparks. The pose accent does not pause rules or the world. R resets progress intentionally; restart is one tick after the R input, not one tick after failure without player input.

## Collaboration and decision handoff

One editing agent implements runtime, materials, evidence and the final topic mapping. Review candidates must name the relevant owner and artifact. No independent playtester has participated. A new mechanic needs a small proposal, excluded scope, implementation owner and reproducible acceptance before joining this slice. A visual revision can improve composition without changing reward rules; changes to those rules require a new slice revision.

## Publicity claim card

Claim: “Generated-art Godot timing prototype with a scripted engine demonstration.” Evidence: `docs/gameplay.mp4`, `docs/engine-report.json`, exact source hashes. Do not promise mobile play, human-proven fun, runtime forest parallax, combat hitstop or native-grid source generation. GIF is silent; MP4 includes captured sound. A still image is not an animation test. Store copy or thumbnails should use captures from this build, or clearly label concept art.

## Retrospective and next experiment

Early evidence in this task was too weak: first a static illustration, then a procedural fixture, then an offline generated-tree render. Each answered a narrower question than a running game. This scene adds genuine engine integration and can be played, while still lacking human gameplay evidence. Next experiment: give a new player the build without explanation, record whether they discover safe release, understand overload, choose to retry and recognize the goal. Record observations rather than predicting the player's enjoyment.
