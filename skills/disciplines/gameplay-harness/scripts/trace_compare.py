"""Compare declared stable replay traces without rewriting goldens or claiming engine execution."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

MAX_BYTES = 16 * 1024 * 1024
CONTEXT = {'adapter', 'oracle', 'clock', 'tape_sha256', 'initial_state_sha256', 'rng'}
MISSING = object()


def fields(value, keys, where):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f'{where}: expected fields {sorted(keys)}')


def json_value(value, depth=0):
    if depth > 64: raise ValueError('state/event nesting exceeds 64')
    if value is None or type(value) in (str, bool, int): return
    if type(value) is float and math.isfinite(value): return
    if isinstance(value, list):
        for item in value: json_value(item, depth + 1)
        return
    if isinstance(value, dict) and all(isinstance(k, str) for k in value):
        for item in value.values(): json_value(item, depth + 1)
        return
    raise ValueError('state/events must be finite JSON values')


def validate(data):
    fields(data, ['schema_version', 'build', 'context', 'frames'], 'trace')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('unsupported schema_version')
    if not isinstance(data['build'], str) or not re.fullmatch('[0-9a-f]{40}', data['build']):
        raise ValueError('build must be an immutable 40-character commit SHA declaration')
    context = data['context']; fields(context, CONTEXT, 'context')
    for k, v in context.items():
        if not isinstance(v, str) or not v.strip() or len(v) > 256:
            raise ValueError(f'context.{k} must be nonempty text, maximum 256 characters')
        if k.endswith('_sha256') and not re.fullmatch('[0-9a-f]{64}', v):
            raise ValueError(f'context.{k} must be SHA-256')
    frames = data['frames']
    if not isinstance(frames, list) or not 1 <= len(frames) <= 100000:
        raise ValueError('trace requires 1..100000 frames')
    previous = None
    for row in frames:
        fields(row, ['tick', 'state', 'events'], 'frame')
        tick = row['tick']
        if type(tick) is not int or tick < 0 or (previous is not None and tick != previous + 1):
            raise ValueError('ticks must be nonnegative contiguous integers, not booleans')
        if not isinstance(row['state'], dict) or not isinstance(row['events'], list):
            raise ValueError('frame needs state object and ordered events array')
        if not all(isinstance(e, dict) and isinstance(e.get('id'), str) and e['id'].strip() for e in row['events']):
            raise ValueError('each event needs a nonempty id')
        json_value(row['state']); json_value(row['events']); previous = tick


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def first_difference(expected, observed, path=''):
    if expected is not MISSING and observed is not MISSING and canonical(expected) == canonical(observed): return None
    if type(expected) is dict and type(observed) is dict:
        for key in sorted(set(expected) | set(observed)):
            token = key.replace('~', '~0').replace('/', '~1')
            found = first_difference(expected.get(key, MISSING), observed.get(key, MISSING), path + '/' + token)
            if found is not None: return found
    if type(expected) is list and type(observed) is list:
        for i in range(max(len(expected), len(observed))):
            found = first_difference(expected[i] if i < len(expected) else MISSING,
                                     observed[i] if i < len(observed) else MISSING, path + '/' + str(i))
            if found is not None: return found
    return {'path': path or '/', 'expected_present': expected is not MISSING,
            'observed_present': observed is not MISSING,
            'expected': expected if expected is not MISSING else None,
            'observed': observed if observed is not MISSING else None}


def compare(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    validate(baseline); validate(candidate)
    result = {'schema_version': 1, 'validation_mode': 'offline-trace-comparison',
              'runtime_validation': 'not-run', 'failure_attribution': 'unknown',
              'baseline_build': baseline['build'], 'candidate_build': candidate['build'],
              'frames_compared': 0,
              'limits': ['does not execute a candidate or verify trace authenticity',
                         'compares the entire exported stable state and ordered events exactly',
                         'matching hashes are declarations; generation provenance requires separate verification']}
    mismatch = sorted(k for k in CONTEXT if baseline['context'][k] != candidate['context'][k])
    if mismatch:
        return dict(result, status='blocked', incompatible_context=mismatch)
    a, b = baseline['frames'], candidate['frames']
    for index in range(max(len(a), len(b))):
        x = a[index] if index < len(a) else MISSING
        y = b[index] if index < len(b) else MISSING
        delta = first_difference(x, y)
        if delta is not None:
            # Include the compared divergent frame, but not an absent frame.
            result['frames_compared'] = index + int(x is not MISSING and y is not MISSING)
            delta['tick'] = (x if x is not MISSING else y)['tick']
            return dict(result, status='fail', first_difference=delta)
    return dict(result, status='pass', frames_compared=len(a),
                trace_sha256=hashlib.sha256(canonical(a).encode('utf-8')).hexdigest())


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value): raise ValueError('non-finite JSON constant: ' + value)


def read(path):
    with path.open('rb') as stream: raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES: raise ValueError('trace exceeds 16 MiB limit')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant), hashlib.sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path); parser.add_argument('candidate', type=Path)
    parser.add_argument('--output', type=Path, help='New report only; existing paths are never overwritten')
    args = parser.parse_args()
    try:
        a, ah = read(args.baseline); b, bh = read(args.candidate)
        result = compare(a, b)
        result.update(baseline_sha256=ah, candidate_sha256=bh, tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        output = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream: stream.write(output)
        else: print(output, end='')
        return {'pass': 0, 'fail': 1, 'blocked': 2}[result['status']]
    except (ValueError, OSError, TypeError, OverflowError, RecursionError) as error:
        print(json.dumps({'status': 'blocked', 'reason': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__': raise SystemExit(main())
