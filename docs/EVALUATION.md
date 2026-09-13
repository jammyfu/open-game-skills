# Engineering skill evaluation records

The six new engineering skills each ship a normal, boundary and adversarial case: **18 authored cases, not 18 measured passes**. The offline tool validates the registry and evidence record consistency. It does not invoke a model, run an engine, score answers, authenticate a claimed invocation or replace independent review.

## Static scope

[engineering-registry.json](../skills/engineering-registry.json) is a repository extension covering the six engineering contracts only, not the Agent Skills specification or a complete semantic registry for the whole catalog. Each entry owns its contract and lists its actual Modes table in order. Optional dependencies are known skill names; they are loaded only when needed, never recursively by this registry. Examples stay `not-run` and select a declared mode. Each case defines its own criteria.

```bash
python3 tools/engineering_quality.py
```

Exit 0 here means the suite is structurally valid. With no imported results the report shows `pass: 0`, `not-run: 18`. CI intentionally checks that structure; it does not pretend to pass the unexecuted model-evaluation gate.

## Prepare and execute a real evaluation

Create the record outside `skills/` (for example in an existing `eval-run/` directory). The template command refuses to overwrite a file.

```bash
mkdir -p eval-run
python3 tools/engineering_quality.py --write-template eval-run/results.json
```

Use a real, authorized model runner with the relevant case prompt and skill context. Record exact model ID, configuration/context, driver, an immutable repository commit and a timezone-qualified execution timestamp in `subject`. Keep API keys and user-private data out of the record. Preserve the raw UTF-8 response in the record directory or a child directory. Responses are limited to 2 MiB by this lightweight validator; store larger runtime artifacts separately and cite them during review.

Have a human or separately identified judge assess **every** criterion against the real response, with a reason locating the relevant output or omission. This is an assessment record, not automatic semantic scoring. Compare baseline/no-skill, current and revised contexts as separate runs. Never copy one outcome into another run or model merely because their prompt text matches.

## Executed result shape

The generated top-level record already includes a suite fingerprint and all case IDs. Replace a row only after execution. The following is a structural example with placeholders, **not a valid passing record**:

```json
{
  "case_id": "asset-runtime-normal",
  "status": "pass",
  "response": {"path": "responses/asset-runtime-normal.txt", "sha256": "<actual lowercase SHA-256 of response bytes>"},
  "judgment": {
    "reviewer": "<human or exact judge model and review run ID>",
    "method": "human-review",
    "criteria": {
      "c1": {"status": "pass", "reason": "<evidence location and explanation>"},
      "c2": {"status": "pass", "reason": "<evidence location and explanation>"},
      "c3": {"status": "pass", "reason": "<evidence location and explanation>"}
    }
  }
}
```

`method` is `human-review` or `model-judge`. `pass` requires every criterion to be recorded as pass; `fail` requires at least one failing criterion. Both require a nonempty response with a matching hash and full subject metadata. The validator cannot tell whether an evaluator lied or judged incorrectly. A recorded pass is not an authenticity certificate, engine test or gameplay pass.

Blocked and unrun rows use only `case_id`, `status` and a nonempty `reason`. Omitted cases remain `not-run` in the denominator. An incomplete assessment remains blocked rather than inventing scores. Duplicate/unknown cases, extra or missing criteria, inconsistent outcomes, missing files, path traversal, external symlinks and changed hashes are rejected.

## Validate a record and enforce coverage

```bash
python3 tools/engineering_quality.py --results eval-run/results.json
python3 tools/engineering_quality.py --results eval-run/results.json --require-passed
```

Exit codes: **0** = consistent record (and all cases recorded pass when the gate is requested); **1** = a valid record fails the all-passed coverage gate; **2** = malformed/inconsistent inputs or I/O failure. A new not-run template must return 1 with `--require-passed`.

The fingerprint binds all Markdown/JSON under `skills/`, including the registry, examples and prompts. Changes invalidate old records; preserve them against their original checkout, do not relabel them with a new fingerprint. The subject commit is declared metadata: the offline tool validates hash format, not remote commit authenticity. Binary assets, code, timing and engine behavior require their own evidence. Keep evaluation outputs outside `skills/` so they do not alter the suite being evaluated.
