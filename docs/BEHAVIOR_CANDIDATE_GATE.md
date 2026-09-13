# Behavior evaluation: supplied candidates and fixed evidence gates

This is a scoped Three.js r180 specimen, not a claim that all Skills are certified.
The previous HTTP specimen remains intact. The new runner transports the same
reviewed engine bytes through offline Blob modules and passes the real embedded
GLB/PNG bytes to GLTFLoader.parseAsync. It does not replace the renderer or alter
browser network policy. HTTP requests are blocked; service workers are disabled.

## Reproduce

```sh
python -m pip install playwright==1.57.0
python -m playwright install --with-deps chromium
python tests/behavior/acquire_inputs.py --download --root /absolute/runtime
python tests/behavior/run_candidate.py --runtime /absolute/runtime \
  --output /absolute/new-evidence --build-ref "$(git rev-parse HEAD)"
python tests/behavior/evidence_gate.py /absolute/new-evidence
```

On a machine using system Chromium, add `--browser /usr/bin/chromium`.
The supplied Linux environment also uses `xvfb-run -a` when needed.
Each output directory must be new: existing evidence is never overwritten.
Exit 0 means the checks and retained-evidence gate passed. Exit 1 is a failed
execution or observation. Exit 2 means missing/invalid setup or an existing output
directory. An interrupted process may retain `not-run`; that is not a pass.

## Candidate boundary

Supply a directory containing **exactly** `simulation.mjs` and `asset-pool.mjs`:

```sh
python tests/behavior/run_candidate.py --runtime /absolute/runtime \
  --candidate-dir /absolute/candidate --candidate-label unverified-producer-label \
  --output /absolute/new-candidate-evidence
```

`simulation.mjs` exports `CombatWorld`. It has a logical `tick` starting at 0,
`step(inputs)` advancing one tick, `actor(id)` for A/B/C, and ordered `events`.
Actors expose id, x, clock, freeze, hp, move and pending; the specimen's reference
module documents their schema. Inputs use id, actor and action. The reference
scenario owns the 60 Hz project clock, contact distance and four-tick hitstop.

`asset-pool.mjs` exports `AssetPool(load, dispose)`. It provides
`acquire(key, isCurrent)` returning `{ready, release}`, and `stats.loads` and
`stats.disposed`. Ready resolves null for released/stale consumers; failures
reject and permit retries; final release disposes once. Resource ownership policy
comes from the Skill/specimen, not from presentation cadence.

Candidate exports named `replay` or `normalChecks` are ignored. The repository owns
replay driving, state observation, browser driver and both JS/Python oracles.
Explicit mutation controls always use the reference implementation, so supplied
candidates do not need to implement mutant switches. The directory boundary and
source hashes are **not a security sandbox for adversarial code**. Run only
reviewed candidate code in a disposable environment with no secrets.

## What is checked

There are 21 engine/input observations and five reference mutation controls.
The Python gate requires the complete case inventory, 120 contiguous logical
ticks, all six replay traces/events, semantic actor-clock/position/damage rules,
shared resources, eight complete unload cycles, native keyboard hit counts and
actual observations for the designated mutation targets. It does not trust
`status: pass`, `traceEqual: true`, or candidate-owned scoring functions alone.

The artifact gate requires the exact evidence inventory, captured candidate bytes,
current trusted/Skill source hashes, immutable runtime pins, fixture/license bytes,
native traces and a PNG screenshot header/viewport. Hashes establish internal
consistency, not producer identity or tamper-proof authenticity. Visual inspection
is still required; a PNG header check is not visual QA.

Input acquisition now verifies every byte set against a repository-owned Git blob
fingerprint and reviewed metadata. Rewriting `acquisition.json` hashes cannot repin
changed bytes. Existing old acquisition manifests fail closed after a specification
change; re-acquire or explicitly revalidate the unchanged bytes against reviewed
pins, never silently update a golden after a mismatch.

## Evidence and claims

Reports bind `behavior-evaluated-in-pilot` to the five selected Skill hashes and
two candidate source hashes. They do not mutate global review state. The runner
invokes no provider API: provider calls are 0; model IDs, API run IDs, tokens and
cost remain null. `--candidate-label` is user-supplied text, not verified identity.
External-copy and deliberately broken candidate probes test the evaluation
boundary; they are not independent LLM samples or a no-Skill control group.

Independent LLM generation, causal with/without-Skill A/B, human playtesting,
hardware FPS, skeletal animation and cross-engine equivalence remain untested.
Babylon's separately supplied pilot is neither replaced nor certified here.

CI runs original HTTP execution, new offline execution, then the evidence gate.
The candidate-evidence artifact contains report, screenshots, traces and hashes.
No secrets, LLM billing or Marketplace publication is part of this workflow.
