# Evidence-led design review

## Inspiration and provenance

Reviewed [kociden/sakurai-skill](https://github.com/kociden/sakurai-skill) at commit `913dc46b9dedc5e0b12e3834d25d684cf8213f87` on 2026-11-15. Its useful organizational ideas are task-specific review entry points, conditional reference reading, and an example mapping design decisions to their sources. The repository describes itself as an unofficial AI summary of automatic video subtitles. Its summaries are not quotations or independently verified statements by Masahiro Sakurai. No LICENSE file was present in the inspected tree; no text, tools, images or subtitle collection is vendored here.

The procedure below is an original adaptation for this repository's bounded skills and evidence contract. It is not an imported list of Sakurai principles. Link a cited observation to its exact file/commit; an upstream ordinal alone is not a canonical video identifier. Attribute claims to the summary unless the original video and relevant passage have actually been checked.

## Choose one review question

Start with an observed problem and the intended audience. “It feels slow” is a report, not yet an explanation. Capture a concrete sequence and separate input latency, authored commitment, unreadable feedback, repeated waiting and failed recovery. A deliberate slow action can be appropriate. Do not infer that every game needs hitstop, fast retries, explicit rewards or combat.

Before reading more references, identify the existing owner and select at most three specialized skills plus an engine adapter if necessary. This reference does not activate additional skills recursively.

| Question | Existing owner | Useful measurement or observation |
|---|---|---|
| What does the player decide, and why? | game-planning | Observable choice and consequence in one slice |
| Does the opening deliver the promise? | first-session-value | Entry to first meaningful outcome; setup burden |
| Where does action timing fail? | action-feel | Input, state transition, contact and feedback trace |
| Does feedback explain what happened? | hud-feedback | Authoritative event and corresponding cue |
| Is the challenge appropriate? | difficulty-design | Intended cohort, failure cause and retry context |
| Does the claimed result hold? | game-qa | Correct pass type, exact build and evidence |

## Proposal card

Record these fields in a project review, not as new Agent Skills frontmatter:

```text
review_id / build / target / driver
observed sequence and artifact timestamps
intended experience and audience
hypothesis and competing explanation
source note: external summary | checked primary source | project observation
owning skill and relevant project contract
smallest proposed change and parameter units
expected visible consequence
acceptance scenario and counterexample
result: pass | fail | blocked | not-run
evidence, tradeoff and untested remainder
```

Prefer a few justified changes over a checklist that adds every effect. For one change, keep the same scenario and inputs in baseline and candidate. Observe the intended consequence as well as regressions: stronger feedback may hide danger, or a shorter retry may remove information the player needs. An attractive capture demonstrates presentation; it does not establish player comprehension or natural completion.

For new concepts, write a one-line loop and a small choice/consequence table before features. A risk/reward tradeoff is one useful lens when applicable; a peaceful creation or narrative game can use expression, discovery or interpretation instead. Treat all numeric examples as project tuning seeds with units, not universal constants.

## Close the review

Each finding pairs evidence with a bounded next action, owner and validation plan. An independent reviewer, when available, records the inspected build and their own observations. Never invent independent or human review. Keep rejected recommendations and reasons, so later reviewers know which differences are deliberate. Recheck only affected contracts after a change; mark unexecuted player/engine work not-run. The QA owner retains the pass taxonomy and evidence card.

For all 14 source topics, their existing owners and project deliverables, consult the [full design and production lenses](game-design-lenses.md). Use only the relevant lenses per phase.
