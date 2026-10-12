# Independent Skill A/B pilot: asset-runtime-ab-v1

This runs model inference, not two answers written by the coordinating assistant.
A successful collection is not a successful candidate. A completed experiment is
not a claim of a positive treatment effect. Missing credentials are `blocked`,
not 0% success and never substituted with reference or synthetic model outputs.

## Preregistration

`tests/behavior/experiments/asset-runtime-ab-v1/plan.json` fixes the task, one
`asset-runtime` Skill, source hashes, 6 temporal pairs / 12 independent calls,
`gpt-4.1-mini-2025-04-14`, temperature 0.5, and 4096 output tokens per call.
Within each pair order is randomized using a fixed allocation seed; this is NOT
a model RNG seed. A pair does not share a conversation or a completion.

The only input difference is the complete asset-runtime SKILL.md appended to the
same task. The control still gets the actual functional requirements, not a
weakened task. Neither arm sees repository implementations, engine oracles, test
outputs or this chat history. No tools, conversation ID or previous-response ID
are sent. Responses use `store:false` and strict JSON output. Linked references
inside the Skill are not fetched. Extra context length is part of the treatment;
this does not isolate wording from added information/token effects.

Only `asset-pool.mjs` is generated. The combat module is a pinned common reference,
not attributed to the model. The browser driver gets opaque candidate labels,
not arm/pair labels. This is scorer blinding, not a fully blinded human study;
comments in generated source may reveal provenance. All planned rows, refusals,
truncations, invalid JSON, provider errors and setup blocks remain in the report.
There are no API retries, manual source repairs, best-of-N selection or swaps.

## Execute

Local collection (requires an already authorized OPENAI_API_KEY in the environment):

```sh
python tests/behavior/ab_experiment.py generate --execute --output /absolute/ab-collection
```

Without `--execute`, this writes the exact allocation and both prompts but makes
zero network requests. Existing output directories are never overwritten.

Evaluate on a separate credential-free machine/process:

```sh
python -m pip install playwright==1.57.0
python -m playwright install --with-deps chromium
python tests/behavior/acquire_inputs.py --download --root /absolute/runtime
python tests/behavior/ab_experiment.py evaluate \
  --collection /absolute/ab-collection --runtime /absolute/runtime \
  --output /absolute/ab-evaluation
```

For this container's system Chromium, use `xvfb-run -a` and add
`--browser /usr/bin/chromium`; the baseline cannot create WebGL without Xvfb here.
A fresh same-machine reference run must pass before attributing a candidate
failure. Each candidate runs in its own bounded subprocess / browser. Child
processes receive only a minimal non-secret environment; browser HTTP is blocked
by the existing runner. This is not a general malicious-code security sandbox.

## GitHub Actions

The new **Skill A-B experiment** workflow runs when this specific plan is added
or intentionally changed on main, or via manual workflow_dispatch with explicit
confirmation. Ordinary Skill/source edits do NOT launch more paid API calls.
Only the generation step receives the repository secret `OPENAI_API_KEY`. A
second job on a fresh runner downloads the generated artifacts and executes them
without that secret. Checkout does not persist credentials. No permission or
billing settings are enabled/modified and no secret is created by this change.

If the secret is absent, collection exits 2, uploads a blocked report retaining
all 12 not-run slots, and evaluation does not start. Configure the secret in
GitHub's encrypted Actions secrets interface, never in code or chat, then use
manual Run workflow. Deliberate reruns are NEW billed experiments with different
run IDs; do not combine them or replace first-attempt results silently.

At the checked model rate of $0.40/M input and $1.60/M output, the preflight uses
request-byte counts plus framing reserve and output caps to reject a configured
estimate above $0.50. This is an estimate, not a provider invoice guarantee or
account spending control. The invariant limits are 12 calls and 4096 output
tokens each. Token usage and response IDs come from actual responses; transport
errors leave cost unknown rather than reporting zero.

## Reading results

Primary endpoint: first-shot generated AssetPool satisfies the complete fixed
engine/evidence gate. Invalid/refused/truncated generations are observed failures;
transport/provider/setup blocks remain unobserved. The report shows planned,
passed, failed and unobserved counts for each arm. Rates use only observed
pass/fail outputs and expose the missing denominator; no observed samples means
null, not zero. The paired difference and exact two-sided McNemar calculation
use only complete pairs. With six pairs on one task, conclusions are exploratory.
No multiple-task generalization, all-Skill certification, production readiness,
human playtest or causal attribution to unrelated engine/fixture Skills follows.

The common engine reports still carry their narrowly scoped specimen assessments;
this wrapper attributes the A/B contrast ONLY to the generated AssetPool task.
Provider JSON and decoded module bytes are retained and rechecked. No transformed
or repaired output can be evaluated under the original provider record. Hashes
support consistency, not cryptographic provider attestation.

## Official references checked for this implementation

- https://developers.openai.com/api/docs/models/gpt-4.1-mini
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/reference/cli/resources/responses/methods/create
- https://docs.github.com/en/github-models — this service retired July 30, 2026;
  old tutorials using `models:read`/GITHUB_TOKEN for free inference are not used.

Unit fixtures in `tests/test_behavior_ab.py` are explicitly synthetic. Passing
those tests proves runner behavior, not that any independent LLM was called.
