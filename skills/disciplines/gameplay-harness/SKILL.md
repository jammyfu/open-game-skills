---
name: gameplay-harness
description: Use when you need an executable runner beside the game that records inputs, steps the logic clock, and writes evidence. Not the repo CI. Not a second combat clock.
---

# Gameplay harness

Ask first: logic | replay | scripted | soak | human.

Stack `gameplay-validation` for what a session may prove. This file is how to *drive* it.

## Do not reuse the pack CI

`tools/skill_test_runner.py` only checks Markdown/JSON contracts. A green GitHub Action is not a clear. The harness lives in the *game* repo.

## Bind six probes (engine adapter)

The game exposes, on the logic tick:

| Probe | Harness uses it for |
|---|---|
| `poll_input(frame)` | inject a tape row or pass through human |
| `now_logical_frame()` | identity of the tick |
| `play_pose` | optional visual; never the pass/fail |
| `query_hits()` | contact log after the tick |
| `apply_knockback` | observe, do not author |
| `juice_hook` | must be off or ignored in logic asserts |

Also publish: seed, save slot, difficulty column, cheat flags, device.

## Tape format

One JSONL row per logic frame:

```json
{"f": 1204, "held": ["jump"], "press": ["light"], "axis": {"x": 0.2, "y": 0}}
```

Rules: frame ids are logical, not wall-clock. Analog is quantized. Do not store rendered pixels in the tape. Video is `gameplay-capture`, linked by session id.

## Modes

| Column | Driver | Cheats | May prove |
|---|---|---|---|
| logic | fixtures / function calls | yes | formulas, flags, save schema |
| replay | tape | off unless labeled | same seed + tape → same hit log |
| scripted | tape + teleport/god | on, named | one arena |
| soak | idle + random legal inputs | off | leak / soft-lock over N minutes |
| human | real device | off | new-player-watch / real-input |

Teleport or phase-skip forces `scripted`. The runner writes that mode into the report even if the operator forgets.

## Session report

```json
{
  "build": "<git sha>",
  "mode": "replay",
  "cheats": [],
  "seed": 7,
  "chain": {
    "boot": "pass",
    "teach": "pass",
    "challenge": "fail",
    "retry": "not-run"
  },
  "bucket": "game",
  "evidence": "sessions/2026-09-13-a/hits.jsonl"
}
```

`bucket` is only `game` | `player` | `setup` | `harness`. A lost browser tab is `harness`. A missed parry is `player` until a tape reproduces a box error — then `game`.

## Implementation sketch

```
game-repo/
  harness/
    adapter.ts      # bind the six probes
    runner.ts       # step frames, write report
    tapes/          # committed golden inputs
    sessions/       # gitignored evidence
```

Loop:

1. Load save + seed + mode.
2. For each tape row: `poll_input` → tick → append `query_hits`.
3. Compare hit log / flags / hp to the golden file.
4. Diff mismatch → fail. Do not "fix" by stretching stun.
5. Human mode: record a new tape instead of asserting.

Determinism check: replay the same tape at two render cadences. Logical rows must match (`custom` accept test).

## Rules

1. Juice, camera, and particles are not oracles.
2. Harness must not own hitstop length.
3. A soak that uses god mode is scripted, not soak.
4. CI in *this* pack stays contract-only. Game CI may call the harness on tapes labeled `replay`.

Accept: one command can replay a named tape and print mode, cheats, and which chain box failed. A stranger can tell harness failure from a game defect.
