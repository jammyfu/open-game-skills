---
name: gameplay-harness
description: Use when a game needs an executable driver beside the runtime to inject semantic inputs, replay deterministic tapes, step the project's existing logic clock, and collect inspectable evidence. It does not decide what a session proves, replace game QA, or create a second gameplay clock.
---

# Gameplay harness

Use this skill to **drive and observe** a game build. Stack `gameplay-validation` to decide what the resulting session may prove, `game-qa` to decide which QA column is required, and `gameplay-capture` for video/edit provenance.

## Ownership

This skill owns:
- input tape schema and driver mode
- adapter probes into the game runtime
- deterministic replay orchestration
- session/evidence identity
- stable oracle comparison

It does **not** own:
- evidence/claim taxonomy (`gameplay-validation`)
- QA coverage taxonomy (`game-qa`)
- capture/edit truthfulness (`gameplay-capture`)
- hitstop, damage, hitboxes, AI, save rules, or other gameplay semantics
- a new fixed timestep

## Driver modes

Ask for one driver mode:

| Driver mode | Driver | Required classification behavior |
|---|---|---|
| logic | fixture/function inputs | usually supports `logic-regression`; claim still comes from `gameplay-validation` |
| replay | committed semantic tape | supports deterministic regression only for the recorded scope |
| scripted | tape plus explicit setup overrides | forces `scripted-scene` evidence classification |
| soak | idle or random **legal** inputs | may collect stability evidence; cheats reclassify the run as scripted |
| human | real input device | may support `real-input`; only a qualified study is `new-player-watch` |

Driver mode is execution metadata, not a claim. A human driver does not automatically prove new-player usability.

## Adapter contract

Bind the harness to the game's **existing** simulation/update boundary. Do not invent a 60 Hz clock.

| Probe | Purpose |
|---|---|
| `inject_input(frame, actions)` | inject semantic actions/quantized axes for the next project logic frame |
| `now_logical_frame()` | stable identity of the project's current gameplay frame/tick |
| `advance_project_tick()` | request exactly one step through the project's existing simulation boundary |
| `snapshot_state()` | return the versioned state subset used by the oracle |
| `drain_events()` | return ordered gameplay events emitted since the previous step |
| `presentation_marker()` | optional correlation marker for video/visual logs; never the gameplay oracle |

`advance_project_tick()` delegates to the project's clock. Its delta and substep policy come from the engine/project adapter, never from this skill.

Publish adapter version, engine/runtime version, project clock configuration, seed, save identity, difficulty, input profile, device class, and active overrides.

## Tape format

Use a versioned semantic JSONL tape. One row targets one logical frame:

```json
{"schema":1,"f":1204,"held":["jump"],"press":["light"],"axis":{"move_x":0.2,"move_y":0.0}}
```

Rules:
- `f` is a project logical-frame identity, not wall-clock time.
- Store semantic actions, not physical key codes.
- Quantization and axis ranges are versioned.
- The tape never stores rendered pixels as gameplay truth.
- If input schema changes, migrate or version the tape; do not silently reinterpret old rows.
- Video belongs to `gameplay-capture` and is correlated by `session_id`.

## Versioned oracle

A golden file compares only an explicitly versioned, stable subset:
- selected state fields
- ordered gameplay event IDs/payloads
- optional deterministic state/event hash

Do not compare incidental object addresses, unordered containers, presentation particles, camera shake, raw floating-point noise, or timestamps unless the project explicitly canonicalizes them.

A golden update requires a reason and the build/contract change that made the prior expectation obsolete. Never auto-accept a mismatch.

## Session report

Every run writes a stable report:

```json
{
  "session_id": "2026-09-13-a",
  "build": "<git sha>",
  "harness_version": 1,
  "adapter_version": "threejs-v2",
  "driver_mode": "replay",
  "validation_mode": "logic-regression",
  "seed": 7,
  "save_id": "slot-a@rev-42",
  "difficulty": "normal",
  "device": "desktop",
  "input_profile": "pad-default",
  "overrides": [],
  "oracle": "combat-light-v3",
  "chain": {
    "boot": "pass",
    "teach": "not-run",
    "challenge": "fail",
    "retry": "not-run"
  },
  "bucket": "game",
  "evidence": ["sessions/2026-09-13-a/events.jsonl"]
}
```

`bucket` is `game | player | setup | harness` and is an attribution hypothesis backed by reproduction. A browser/session loss starts as `harness` or `setup`; a player miss is `player` until a controlled replay demonstrates a game defect.

## Execution loop

1. Resolve build, adapter/runtime versions, project clock, seed/save, driver mode, validation mode, and overrides.
2. Load the tape/or input source.
3. For each row: inject input → advance one project tick → snapshot stable state → drain ordered events.
4. Compare the declared oracle subset. A mismatch fails and records the first divergent frame/event.
5. Replay the same tape at at least two presentation/render cadences when render/simulation separation is under test. Project logical rows and canonical oracle output must match.
6. Human mode records a tape and observations; it does not automatically assert a golden.
7. If teleport, force-phase, god mode, unlock-all, or equivalent overrides appear, record them and classify the evidence through `gameplay-validation` as scripted.

## Evidence boundaries

- Camera, animation pose, audio, haptics, particles, and juice are presentation evidence unless their own skill is under test; they do not decide gameplay pass/fail.
- The harness never authors hitstop length, knockback, collision, RNG outcomes, grants, save migrations, or AI decisions.
- A soak with gameplay overrides is not clean soak evidence.
- A green pack CI proves only this repository's contract/static tests. It does not prove a game replay succeeded.
- `TheLegendOfTrump` or any other external project may supply **asset samples** when explicitly marked as such; a demo's current runtime implementation is not an oracle.

## Acceptance

A reviewer can run one named tape and identify:
- exact build/session/adapter/oracle versions
- driver mode versus validation claim mode
- overrides and seed/save/input context
- first divergent logical frame or event
- whether the failure belongs to game, player, setup, or harness

The same tape must not silently change meaning when rendering cadence, physical bindings, or unrelated presentation systems change.
