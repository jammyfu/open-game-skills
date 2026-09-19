# Low-context fixture acquisition

The agent-facing entry point is `scripts/asset_context.py` (Python 3.10+, standard
library only). It imports the existing matcher, preparation and lock functions;
it does not change their policies, locks, catalog, capabilities or test verdicts.
The original three CLIs remain available with their original output contracts.

## Keep bulk data outside the conversation

Use these defaults for one sourcing task:

| Boundary | Default |
|---|---|
| Agent-facing JSON receipt | At most 4096 UTF-8 bytes, enforced by the new CLI |
| Candidate/decision examples in a receipt | At most 3; totals and omission flag remain visible |
| Saved inventory selection | At most 20 file records; all-match and omitted counts retained |
| JSON inputs to the adapter | At most 8 MiB; reject empty, duplicate-key and oversized input |
| Repeated acquisition attempt | At most 2 per same file/problem unless new evidence changes the route |

The retry budget is an agent policy, not an HTTP-client implementation. Raw direct
connector results are outside the CLI's control. Do not request a huge response
and only then summarize it: the input tokens would already have been consumed.

## Retrieval ladder

1. Revalidate existing matching locks using `select --pinned-only` before any remote
   file acquisition. Cache metadata by repository + immutable ref + path. Revalidate
   bytes on each reuse; never trust an old "verified" label after a file changes.
2. Reuse already returned file IDs, paths, blob SHAs and license evidence. Known
   paths need no search. Otherwise search the named repository with a small result
   limit, or list only the relevant directory/subtree. Do not read the entire pack
   catalog or recursively dump a repository tree into chat.
3. For Git Trees, OMIT `recursive` to avoid recursion: even `recursive=false` or
   `recursive=0` requests recursion. Resolve a fixed commit once, then descend only
   into the required subtree. An empty search is not evidence that an asset is absent.
4. When authorized transport can save responses directly to disk, filter the saved
   subtree locally with `inventory`. `truncated=true` stays blocked; fetch narrower
   subtrees rather than guessing completeness. Inventory rows are discovery leads,
   not license, decoding, skin/clip or import evidence.
5. Download only selected files and their actual dependencies via an available
   authorized binary/file transport. Prefer self-contained GLB only when permitted
   by the test's hard format requirements. Inspect GLB external references too.
   Never route GLB/PNG/audio through Base64 chat, or pour OBJ vertices into context.
6. If a connector only returns text/Base64, switch once to a supported file transport.
   If none can acquire complete bytes, stop at `acquisition-blocked`. Do not stitch
   repeated truncated text responses, bypass access controls, use preview art, or
   replace missing source art with unlabeled generated/procedural substitutes.
7. Run decoding, dependency inspection, transformation and engine checks locally.
   Emit only observed counts, dimensions, clips/dependencies, warnings and artifact
   references. Original bytes/license evidence stay intact; derivatives get their
   own hashes and change records. Do not weaken checks to reduce context.

## Commands

Run from this skill's directory. The directory containing `--report` must exist;
each report path must be NEW. Global arguments precede the subcommand. Commands
never download, decode, run an engine, or execute data embedded in an asset.

```sh
# Example profile. Full data is saved; stdout is a bounded JSON receipt.
python3 scripts/asset_context.py --report /absolute/plan.json \
  prepare --skill model-pipeline

# Hard requirements go in request.json, not only in the query preference.
python3 scripts/asset_context.py --report /absolute/candidates.json \
  match --request /absolute/request.json

# Reuse matching locks first; no remote fallback in pinned-only mode.
python3 scripts/asset_context.py --report /absolute/reuse.json \
  select --root /absolute/fixtures --request /absolute/request.json \
  --locks /absolute/fixture.lock.json --pinned-only

# Pin: --report is the reusable ORIGINAL lock schema, not a summary schema.
python3 scripts/asset_context.py --report /absolute/new-fixture.lock.json \
  pin --root /absolute/fixtures --request /absolute/pin.json
python3 scripts/asset_context.py --report /absolute/verified.json \
  verify --root /absolute/fixtures --lock /absolute/new-fixture.lock.json

# Metadata previously saved by an authorized tool. Prefixes are relative to this
# tree response, not necessarily repository-root paths. Patterns match basenames.
python3 scripts/asset_context.py --report /absolute/selected-files.json \
  inventory --input /absolute/subtree.json --prefix Assets/gltf \
  --pattern '*floor*' --pattern '*wall*' --formats glb gltf --limit 12
```

Attribution opt-in remains explicit: `allow_attribution: true` in match/select
requests; `--allow-attribution` for pin/verify/prepare. Do not translate one into an
implicit global permission. Multi-format capability bindings remain unchanged.

`--max-output-bytes` accepts 1024..16384. The receipt includes full-report SHA-256,
size/path, exact top-level status, skill totals/status counts, invalid-lock
occurrences, blocker totals, and bounded examples. All raw rejections, unmatched
requirements and inspection notes stay in the full report. Large examples are
omitted as whole fields, never by truncating JSON. Read a specific blocked role or
candidate from that report only when needed; do not echo the whole report back.

Exit 0 means the operation completed (possibly `needs-acquisition` or inventory
`candidates-only`), 2 means blocked/unmatched/incomplete requirements, and 1 means
invalid input/I/O. No success receipt is printed if writing the report fails.
A valid lock/receipt is not decoding, dependency completeness or gameplay proof.
The stdout byte budget is not a billed-token counter or a guarantee of total task
cost savings. Measure real usage only when provider usage telemetry is available.

## Focused regression check

From the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_asset_context.py'
```

Tests use synthetic integrity fixtures, not provenance or engine assertions.
Additional live engine/import checks remain owned by their existing skills.

## Primary API reference

GitHub Git Trees documentation (retrieval semantics, `truncated` and subtree
fallback): https://docs.github.com/en/rest/git/trees#get-a-tree
