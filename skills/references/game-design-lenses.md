# Game design and production: all 14 source topics

## Scope and provenance

This is an original, engine-neutral working guide informed by the topic structure of [kociden/sakurai-skill](https://github.com/kociden/sakurai-skill/tree/913dc46b9dedc5e0b12e3834d25d684cf8213f87/skills/sakurai), inspected on 2026-11-15. It covers all 14 reference categories, not just the review procedure. The upstream collection is an unofficial AI summary of automatic subtitles. No source prose, tools, screenshots or subtitle corpus is copied. These are project decision lenses and acceptance tasks, not quotations, endorsements or universal prescriptions from Masahiro Sakurai. Original-video verification remains not-run.

Use the [evidence-led review](design-review.md) for proposal/result records. Select only the topics relevant to the current phase: at most three specialized skills and one engine adapter, not all owners below at once. Conditional references do not activate skills recursively. An index entry means a source topic is mapped, not that an individual video has been faithfully reproduced or tested.

The [pinned source inventory](design-source-index.json) accounts for all 257 summary entries across 14 categories using upstream IDs and file hashes. It provides navigation without copying the summaries.

## 1. Gameplay: choices and consequences

Owner: [game-planning](../disciplines/game-planning/SKILL.md), with [balance-design](../disciplines/balance-design/SKILL.md) when tuning alternatives.

Ask what the player chooses, what information permits that choice, what is gained or given up, and why more than one approach is worth considering. Risk/reward is useful for uncertain actions, but expression and discovery can be valid goals without punishment. Publish an alternatives table with costs, outcomes and feedback, including what happens when the player does nothing.

Acceptance: replay the alternatives against a declared goal and intended cohort. Check for an unintentionally dominant option and for failure causes the player could not perceive. Avoid treating higher difficulty or more punishment as automatic improvement.

## 2. Planning: first value, scope and milestones

Owner: [game-planning](../disciplines/game-planning/SKILL.md); onboarding uses [first-session-value](../disciplines/first-session-value/SKILL.md).

Define the promised experience in one sentence, then the smallest start-to-outcome slice that demonstrates it. List dependencies, excluded systems, entry friction and the next decision the prototype should inform. Keep narrative and noncompetitive projects valid.

Acceptance: a target player encounters the intended decision and recognizes its consequence. Time-to-value is observed in a specific build, not prescribed as a universal number of minutes. Do not add content volume before the core question has evidence.

## 3. Concepts: coherent identity and originality

Owner: [game-planning](../disciplines/game-planning/SKILL.md), or [art-bible](../assets/art-bible/SKILL.md) for visual identity.

Separate references into the player need they serve, the mechanism that serves it, and a new combination appropriate to this project. Describe what makes the game's experience distinctive beyond resemblance to another title. Specify a few coherent pillars and use them to reject contradictory additions.

Acceptance: a proposal explains how its mechanic serves a pillar and what tradeoff it introduces. Compare alternatives with the same prototype budget. Do not equate novelty, polish or asset count with proven value; do not imitate a source creator's persona.

## 4. Specifications: explicit tunable contracts

Owner: [action-feel](../disciplines/action-feel/SKILL.md) for action clocks; [input-design](../disciplines/input-design/SKILL.md) for input semantics.

Publish units, state ownership, timing boundaries, legal transitions, failure responses, retry and interruption behavior. Put tunable values in one named data location. Distinguish simulation time, actor-local clocks and presentation time. A button can acknowledge rejection without executing an illegal action.

Acceptance: boundary tests cover the ticks immediately before, at and after each transition. Test duplicate inputs and interruption/reset. Do not import example frame counts or assume display refresh is the logical clock.

## 5. Motion: readable action phases

Owner: [animation-graph](../disciplines/animation-graph/SKILL.md), with [pixel-animation](../2d/pixel-animation/SKILL.md) for sprite timing.

Author an intentional initial response, action/contact pose, follow-through and return. Review silhouettes at actual gameplay scale. Decide whether squash, stretch or pose holds communicate effort without moving authoritative hit volumes. Specify attachment and foot contacts before exaggeration.

Acceptance: frame stepping agrees with published action states; pose holds do not skip gameplay events. Review distant/small sprites and transitions into cancellation or interruption. Do not use automatic smoothing as a substitute for an authored response or mistake visual holds for combat hitstop.

## 6. Effects: purposeful event accents

Owner: [juice-vfx](../disciplines/juice-vfx/SKILL.md).

For every effect, name the event, anchor, lifetime, priority, instance cap and reduction behavior. Separate required information from optional decoration. Use contrast and shape appropriate to both bright and dark backgrounds; protect important poses and HUD reads.

Acceptance: normal/reduced runs preserve logical results and required cues. Capture exact offsets after events, check expiration/retry cleanup and verify limits under bursts. Stronger effects are not always better, and a screen flash is not mandatory.

## 7. Graphics: composition and shared art constraints

Owner: [art-bible](../assets/art-bible/SKILL.md), [materials](../assets/materials/SKILL.md) for surface/color contracts.

Publish palette, scale, silhouette hierarchy, focal area and asset provenance. Place a generated asset in the actual scene before accepting it. Separate attractive concept imagery from registered layers, imported sprites and running scenes. Test whether the background supports the player instead of competing with them.

Acceptance: inspect captures at target resolution, including foreground overlap and reduced-color conditions. Check consistent apparent scale, placement and imported transparency. A beautiful source image alone cannot prove runtime readability or animation quality.

## 8. UI: consequences the player can understand

Owner: [hud-feedback](../disciplines/hud-feedback/SKILL.md), [ui-hud-focus](../disciplines/ui-hud-focus/SKILL.md) for interaction.

Show the current goal, the meaning of an action, why a request failed and what can happen next. Prefer concise contextual cues over instructions that must be memorized before play. Avoid color-only critical information; preserve the user's presentation settings.

Acceptance: use real authoritative state boundaries, supported input methods, focus changes and localization extremes. A player should identify both state and recovery route. A screenshot can demonstrate placement but not response latency or comprehension.

## 9. Sound: action-linked cues and mix hierarchy

Owner: [audio-feel](../disciplines/audio-feel/SKILL.md), [audio-buses](../disciplines/audio-buses/SKILL.md).

Map cues to authoritative events, distinguish confirmation/failure/reward, and set priorities, gain limits and retrigger policies. Keep critical meaning available without sound. Maintain a source and rights record for generated or supplied audio.

Acceptance: capture actual nonzero output, exercise rapid retriggers and confirm cleanup. Listening review, output-device behavior and accessibility are separate checks. A WAV with nonzero samples proves sound exists, not that the mix feels good.

## 10. Technology: iteration and reliable measurement

Owner: [debug-slate](../disciplines/debug-slate/SKILL.md), [performance-budget](../disciplines/performance-budget/SKILL.md), [game-qa](../disciplines/game-qa/SKILL.md).

Expose the smallest useful state/parameter inspection and deterministic reproduction hooks. Retain production-like behavior when debug UI is off. Name build, device, configuration, input driver and clock for every result. Use source hashes or commits to connect captures to code.

Acceptance: repeat a case without hidden setup; inject an invalid parameter or interruption to confirm detection. Separate rule tests, engine integration, performance and playtests. Movie capture and offscreen runs cannot establish natural frame pacing.

## 11. Team: decisions and handoffs

Owner: [game-planning](../disciplines/game-planning/SKILL.md) for scope/decisions; [game-qa](../disciplines/game-qa/SKILL.md) for acceptance.

Use a decision card: problem, options, decision owner, selected approach, rejected alternative, dependency, acceptance owner and revisit trigger. Request feedback using a concrete build and question. Record disagreement and rationale without inventing consensus.

Acceptance: another contributor can implement or verify the handoff without reconstructing private conversation. A team of one still benefits from explicit decisions, but it must not claim independent review. Communication templates do not prove team effectiveness.

## 12. Mindset: hypothesis, observation and learning

Owner: [game-planning](../disciplines/game-planning/SKILL.md).

Turn preferences into hypotheses and choose a small experiment. Keep a learning log: prediction, evidence, surprise, decision and next question. Account for the developer's familiarity; watch new players when onboarding or perceived difficulty is the question.

Acceptance: a changed decision is traceable to evidence, including a result that contradicts the initial preference. Respect working limits and individual methods. Personal routines, anecdotes or motivational advice are optional context, not employee policy or scientific findings.

## 13. Public relations: demonstrate what the build does

Owner: [gameplay-capture](../disciplines/gameplay-capture/SKILL.md) for footage, [ship-checklist](../disciplines/ship-checklist/SKILL.md) for readiness claims.

Create a claim card: audience, promise, exact build, supporting capture, edit/automation disclosure, rights, limitation and publication owner. Show the distinguishing interaction promptly. Use implemented scenes for gameplay claims; label mockups and scripted footage explicitly.

Acceptance: every public claim has an artifact of the appropriate evidence class. Check thumbnail readability, text localization and capture provenance. Views, a polished trailer or a store listing do not prove playability, quality or retention.

## 14. Miscellaneous: context without accidental mandates

Owner: [game-planning](../disciplines/game-planning/SKILL.md); cross-domain checks follow the [shared contract](../CONTRACT.md).

Keep historical examples, anecdotes and working preferences as contextual references. Extract an explicit project question before applying one. Record genre, scale, audience and technical assumptions that differ from the source. Route a cross-domain idea to an existing owner rather than creating a catch-all authority.

Acceptance: each adopted idea has a reason and a testable consequence; each unadopted idea can remain intentionally deferred. Do not force all source lessons into every game or treat a collection of summaries as a verified original-video curriculum.

## Deliverables and evidence ledger

A comprehensive adoption produces: topic/owner map, project decision cards, named parameters and units, a playable slice where appropriate, art/audio provenance, real captures, test results and a separate untested list. Team and publicity topics can produce concrete documents; they are not validated by a gameplay GIF. A source inventory is navigation, not evidence that every original video was watched.
