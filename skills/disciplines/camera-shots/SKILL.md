---
name: camera-shots
description: Use when gameplay or cinematic states need authored camera framing, follow/orbit/rail/lock/first-person shot presentation and transitions without changing gameplay targeting, collision or simulation rules.
---

# Camera shots

This skill owns camera **presentation grammar**. `camera-anti-clip` owns collision safety; `camera-modesty` owns dignity/modesty framing; targeting/lock eligibility remains with gameplay owners such as `lock-on-target`.

## Compatible modes

`side-plane` | `orbit-third` | `first-person` | `rail` | `lock-follow`

A mode may compose authored sub-shots/transitions when the project requires it; one label is not a ban on stateful framing.

## Contract

Publish shot/state ID, trigger/owner, anchor/look target for framing, transition policy, FOV/offset references, player-control allowance, interruption/return rule and camera-collision requirement.

## Rules

1. Shot transitions consume authoritative state/events; they do not decide hits, target eligibility, facing or movement unless a separate gameplay contract explicitly does so.
2. Hitstop/pause/cutscene behavior is project policy: freeze, blend, continue or hand off according to the owning state rather than a universal “never change shot” rule.
3. Final framing/offsets remain collision-safe through `camera-anti-clip`, respect `fov-comfort` / accessibility settings, and remain modest through `camera-modesty` unless the project explicitly opts into authored adult or medical-exam intent.
4. Presentation target/anchor and gameplay lock target may be related but are distinct identities; camera framing cannot silently acquire a gameplay target.
5. Transition duration/easing and input takeover are authored per mode/state, not universal constants.

## Boom-sweep presentation check

Validate authored boom-arm plans with [boom_sweep.py](scripts/boom_sweep.py) and the [example plan](assets/boom-sweep.example.json). The CLI samples boom length, elevation and azimuth into discrete presentation poses (`position` + `look`). `pass` is geometric presentation only: it does not solve `camera-anti-clip` world collision, does not replace `camera-modesty` dignity framing, does not acquire a gameplay lock target, and does not replace `fov-comfort`. When a plan also names a gameplay lock identity, that id must stay distinct from the presentation anchor/look identities. Poses that declare `camera_collision_required` are flagged for a later anti-clip validation that this tool does not run.

```sh
python skills/disciplines/camera-shots/scripts/boom_sweep.py skills/disciplines/camera-shots/assets/boom-sweep.example.json
```

Exit 0 = presentation plan pass, 1 = valid plan with failed geometric/identity checks, 2 = invalid/unsupported input or I/O failure. Reports include input/tool SHA-256 and refuse to overwrite an existing `--output` path.

## Accept

Replay entry/exit/interruption/target-loss/collision cases and log shot ID, owner, anchor/visual target and final safe pose. Changing camera presentation alone does not alter gameplay target, hit or movement results. The bundled boom-sweep CLI is not collision, comfort, modesty or runtime evidence.
