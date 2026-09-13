"""Fail-closed, repository-owned observation and evidence consistency gate.

A consistent report is not authenticated proof of a model, human, or Skill uplift.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPLAYS = {f'replay-{hz}-{order}': hz for hz in (30, 60, 144) for order in ('forward', 'reversed')}
CLEAN = {'geometries': 2, 'textures': 0}
EXPECTED = {
    'GLB-and-texture-decode': {'meshes': 1, 'vertices': 205, 'triangles': 97, 'dimensions': [[1024, 1024]]},
    'unrelated-actor-progress': 120, 'one-hit-per-attack-victim': 2,
    'simultaneous-trade': ['A>B', 'B>A'], 'four-tick-local-stop': 4,
    'buffered-cancel-once': {'count': 1, 'tick': 7}, 'showcase-cleanup': CLEAN,
    'shared-lease-survives': {'loads': 1, 'same': True, 'disposed': 0, 'memory': {'geometries': 3, 'textures': 1}},
    'last-lease-disposes-once': {'disposed': 1, 'memory': CLEAN},
    'stale-session-rejected': {'attached': False, 'disposed': 1},
    'cancel-one-shared-load': {'cancelled': True, 'otherReady': True, 'loads': 1, 'disposed': 0},
    'failure-retry': {'failure': True, 'retried': True, 'attempts': 2},
    'eight-load-unload-cycles': {'baseline': CLEAN, 'samples': [CLEAN] * 8},
    'native-keyboard-edge-deduplication': [1, 2],
    **{key: {'ticks': 120, 'presentationFrames': hz * 2, 'traceEqual': True} for key, hz in REPLAYS.items()},
}
CASE_IDS = set(EXPECTED) | {'WebGL-draw'}
MUTANTS = {'global-freeze', 'repeat-contact', 'sequential-trade', 'stale-attach', 'premature-dispose'}
TRUSTED_FILES = ('acquire_inputs.py', 'inputs.json', 'run_browser.py', 'run_candidate.py',
                 'offline_transport.py', 'oracle.mjs', 'evidence_gate.py', 'browser.mjs',
                 'index.html', 'simulation.mjs', 'asset-pool.mjs')
SKILLS = ('disciplines/action-feel', 'disciplines/asset-runtime', 'disciplines/gameplay-harness',
          'engines/threejs', 'assets/open-asset-fixture')
ARTIFACTS = {'report.json', 'engine-screenshot.png', 'native-input-trace.json',
             'asset-preparation.json', 'fixture.lock.json', 'generation-request.json',
             'candidate-simulation.mjs', 'candidate-asset-pool.mjs', 'runtime-inputs.json',
             'fixture.glb', 'fixture-license.txt'}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def combat_checks(replay: dict) -> dict[str, bool]:
    trace, events = replay['trace'], replay['events']
    if len(trace) != 120 or [row['tick'] for row in trace] != list(range(120)):
        raise ValueError('trace must contain each of the 120 logical ticks exactly once')
    actors = [{a['id']: a for a in row['actors']} for row in trace]
    if any(len(row['actors']) != 3 or set(a) != {'A', 'B', 'C'} for row, a in zip(trace, actors)):
        raise ValueError('invalid actor set')
    hits = [e for e in events if e['type'] == 'hit']
    return {
        'unrelated-actor-progress': all(a['C']['clock'] == t+1 and a['C']['x'] == 301+t and a['C']['freeze'] == 0 for t, a in enumerate(actors)),
        'one-hit-per-attack-victim': len(hits) == 2 and len({e['id'] for e in hits}) == 2,
        'simultaneous-trade': sorted((e['actor'], e['victim'], e['tick']) for e in hits) == [('A', 'B', 2), ('B', 'A', 2)],
        'four-tick-local-stop': all(a[id]['clock'] == t+1-min(max(t-2, 0), 4)
            and a[id]['freeze'] == (max(0, 6-t) if t >= 2 else 0)
            and a[id]['hp'] == (100 if t < 2 else 90)
            for t, a in enumerate(actors) for id in ('A', 'B')),
    }


def evaluate_runtime(runtime) -> list[str]:
    errors = []
    def need(ok, message):
        if not ok: errors.append(message)
    try:
        canonical(runtime)  # Reject NaN/Infinity, even in otherwise unused observations.
        need(runtime['status'] == 'pass', 'runtime did not pass')
        engine = runtime['engine']
        need(engine['name'] == 'three.js' and engine['revision'] == '180' and engine['webgl'].startswith('WebGL 2.0'), 'unreviewed engine or missing WebGL 2')
        rows = runtime['scenarios']
        need(len(rows) == len(CASE_IDS) and {r['id'] for r in rows} == CASE_IDS, 'missing, duplicate or unknown scenarios')
        for row in rows:
            id, got = row['id'], row['observed']
            need(row['status'] == 'pass', 'unpassed scenario: ' + id)
            if id in EXPECTED: need(canonical(got) == canonical(EXPECTED[id]), 'observation rejected: ' + id)
            elif id == 'WebGL-draw':
                need(type(got['calls']) is int and got['calls'] >= 5 and got['triangles'] >= 293 and got['error'] == 0, 'draw observation rejected')
        traces = runtime['traces']; base = traces['replay-60-forward']
        for key, hz in REPLAYS.items():
            replay = traces[key]
            need(replay['ticks'] == 120 and replay['frames'] == hz * 2, 'wrong replay length: ' + key)
            need(canonical(replay['trace']) == canonical(base['trace']) and canonical(replay['events']) == canonical(base['events']), 'trace/event divergence: ' + key)
            for name, ok in combat_checks(replay).items(): need(ok, key + ': ' + name)
        cancelled = traces['cancel-during-freeze']; events = cancelled['events']
        cancels = [e for e in events if e['type'] == 'cancel']
        need(canonical([{key: e[key] for key in ('tick', 'id', 'actor')} for e in cancels])
             == canonical([{'tick': 7, 'id': 'cancel-a', 'actor': 'A'}]),
             'cancel event identity/timing mismatch')
        a_hits = [e for e in events if e['type'] == 'hit' and e['actor'] == 'A']
        # This fixed tape owns press-a and cancel-a, with two ticks of startup.
        # Counting distinct hits alone also accepts an unrelated PRE-cancel hit.
        # Canonical JSON comparison preserves integer tick types (9.0 is not 9).
        need(canonical([{key: e[key] for key in ('tick', 'id', 'victim')} for e in a_hits])
             == canonical([{'tick': 2, 'id': 'press-a:B', 'victim': 'B'},
                           {'tick': 9, 'id': 'cancel-a:B', 'victim': 'B'}]),
             'on-hit cancel fresh attack identity/timing mismatch')
        cancel_positions = [i for i, e in enumerate(events) if e['type'] == 'cancel']
        hit_positions = [i for i, e in enumerate(events)
                         if e['type'] == 'hit' and e['actor'] == 'A']
        need(len(cancel_positions) == 1 and len(hit_positions) == 2
             and hit_positions[0] < cancel_positions[0] < hit_positions[1],
             'cancel event must precede its fresh hit in the ordered log')
        controls = runtime['negative_controls']
        need(len(controls) == len(MUTANTS) and {c['mutant'] for c in controls} == MUTANTS, 'missing/duplicate/unknown controls')
        targets = {'global-freeze': 'unrelated-actor-progress', 'repeat-contact': 'one-hit-per-attack-victim', 'sequential-trade': 'simultaneous-trade'}
        for row in controls:
            mutant = row['mutant']
            need(row['status'] == 'detected' and 'infrastructure_error' not in row, 'control did not detect a behavioral defect: ' + mutant)
            if mutant in targets: need(not combat_checks(traces[mutant])[targets[mutant]], 'claimed control detection not reproduced: ' + mutant)
            elif mutant == 'stale-attach': need(row['observed'] is True, 'stale control survived')
            elif mutant == 'premature-dispose': need(type(row['observed']) is int and row['observed'] > 0, 'disposal control survived')
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError) as exc:
        errors.append('invalid observations: ' + str(exc))
    return errors


def scoped_assessments(report: dict) -> list[dict]:
    if report.get('status') != 'pass': return []
    return [{'skill': row['path'], 'skill_sha256': row['sha256'],
             'state': 'behavior-evaluated-in-pilot', 'suite': report['suite'],
             'candidate_sha256': report['candidate_sources'],
             'scope': 'Selected requirements of this specimen only; not all Skill clauses or causal LLM uplift.'}
            for row in report['skill_sources']]


def verify(directory: Path) -> list[str]:
    errors = []
    def need(ok, message):
        if not ok: errors.append(message)
    try:
        directory = Path(directory)
        manifest = json.loads((directory / 'artifact-hashes.json').read_text())
        need(isinstance(manifest, dict) and set(manifest) == ARTIFACTS, 'required artifact inventory differs')
        for name in ARTIFACTS:
            path = directory / name
            need(path.is_file() and not path.is_symlink(), 'missing/linked artifact: ' + name)
            if path.is_file() and not path.is_symlink(): need(digest(path) == manifest.get(name), 'artifact changed: ' + name)
        report = json.loads((directory / 'report.json').read_text())
        need(report['schema_version'] == 2 and report['suite'] == 'combat-and-asset-lifetime-v2', 'wrong report schema/suite')
        need(report['status'] == 'pass', 'run did not pass')
        need(report['llm_comparison'] == 'not-run' and report['human_playtest'] == 'not-run', 'unsupported LLM or human claim')
        need(report['network_requests'] == [] and report['browser_errors'] == [], 'network or browser errors')
        need(not any(m['type'] == 'error' for m in report['console']), 'console errors')
        generator = report['generator']
        need(type(generator['provider_call_count']) is int and generator['provider_call_count'] == 0, 'unattested external provider invocation')
        need(generator['kind'] in {'supplied-candidate-unattributed', 'repository-reference-specimen'}, 'unsupported producer claim')
        need(all(generator.get(key) is None for key in ('model_api_id', 'provider_run_id', 'token_usage', 'cost')), 'unobserved model metadata')
        image = (directory / 'engine-screenshot.png').read_bytes()
        need(len(image) >= 24 and image[:8] == b'\x89PNG\r\n\x1a\n' and image[12:16] == b'IHDR', 'missing PNG screenshot header')
        if len(image) >= 24:
            width, height = struct.unpack('>II', image[16:24])
            need(width >= 1280 and height >= 1000, 'screenshot dimensions below declared viewport')
        errors.extend(evaluate_runtime(report['runtime']))
        need(set(report['trusted_sources']) == set(TRUSTED_FILES), 'incomplete trusted source inventory')
        for name in TRUSTED_FILES: need(report['trusted_sources'].get(name) == digest(HERE / name), 'stale trusted source: ' + name)
        need(set(report['candidate_sources']) == {'simulation.mjs', 'asset-pool.mjs'}, 'wrong candidate inventory')
        for name in ('simulation.mjs', 'asset-pool.mjs'):
            need(report['candidate_sources'].get(name) == digest(directory / ('candidate-' + name)), 'candidate bytes changed: ' + name)
        sources = report['skill_sources']
        need(len(sources) == len(SKILLS) and {r['path'] for r in sources} == {'skills/' + s + '/SKILL.md' for s in SKILLS}, 'incomplete skill provenance')
        for row in sources:
            rel = row['path']
            if rel in {'skills/' + s + '/SKILL.md' for s in SKILLS}:
                need(row['sha256'] == digest(ROOT / rel), 'stale skill source: ' + rel)
        acquisition = json.loads((directory / 'runtime-inputs.json').read_text())
        spec = json.loads((HERE / 'inputs.json').read_text())
        need(acquisition['spec_sha256'] == digest(HERE / 'inputs.json'), 'runtime specification changed')
        pins = spec['files']; rows = acquisition['files']
        need(len(rows) == len(pins) and {r['path'] for r in rows} == {p['path'] for p in pins}, 'runtime inventory differs')
        indexed = {r['path']: r for r in rows}
        for pin in pins: need(all(indexed[pin['path']].get(k) == v for k, v in pin.items()), 'runtime pin changed: ' + pin['path'])
        for name, rel in [('fixture.glb', 'fixtures/banner_blue.gltf.glb'), ('fixture-license.txt', 'fixtures/LICENSE.txt')]:
            data = (directory / name).read_bytes()
            git_sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            need(git_sha == next(p['git_blob_sha'] for p in pins if p['path'] == rel), 'fixture differs from reviewed pin')
        asset = json.loads((directory / 'asset-preparation.json').read_text())
        need(asset == report['asset_preparation'] and asset['status'] == 'pass', 'asset preparation differs or failed')
        need(asset['negative_controls'] == {'tampered_bytes_rejected': True, 'static_model_not_accepted_as_rig': True}, 'asset negative controls failed')
        native = json.loads((directory / 'native-input-trace.json').read_text())
        need([len([e for e in native[k]['events'] if e['type'] == 'hit']) for k in ('first', 'second')] == [1, 2], 'native input artifact disagrees')
        need(report['skill_assessments'] == scoped_assessments(report), 'scoped assessments differ')
    except (OSError, KeyError, TypeError, ValueError, IndexError, AttributeError, StopIteration) as exc:
        errors.append('invalid evidence: ' + str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    errors = verify(args.directory)
    print(json.dumps({'status': 'rejected' if errors else 'consistent', 'errors': errors,
        'scope': 'Evidence consistency only; not authenticated identity, all-Skill certification, or causal model uplift.'}, indent=2))
    return int(bool(errors))


if __name__ == '__main__': raise SystemExit(main())
