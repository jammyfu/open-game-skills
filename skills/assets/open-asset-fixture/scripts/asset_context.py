"""Bounded agent-facing receipts over the unchanged offline fixture operations.

Full JSON (or the original lock schema for pin) is exclusively written to --report.
No network, extraction, decoder or engine is invoked. Exit 2 means unavailable or
incomplete input; exit 1 means invalid input/I/O. Exit 0 is NOT an engine pass.
"""
from __future__ import annotations

import argparse
from collections import Counter
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

from asset_fixture import PACK, match_assets, unique_object, validate_catalog
from fixture_lock import DATA, make_lock, select_assets, verify_lock
from prepare_assets import prepare

MAX_INPUT = 8 * 1024 * 1024
BLOCKED = {'blocked', 'unmatched', 'needs-requirements'}
SCOPE = 'Selection/local byte consistency only; no download, decoding, dependency or engine validation.'


def read_bounded(path: Path, limit: int = MAX_INPUT) -> Any:
    """Read at most limit+1 bytes, including when an input grows after stat()."""
    if type(limit) is not int or not 1 <= limit <= MAX_INPUT:
        raise ValueError('input byte limit must be between 1 and 8388608')
    with path.open('rb') as handle:
        raw = handle.read(limit + 1)
    if not raw or len(raw) > limit:
        raise ValueError('empty or oversized JSON input')
    return json.loads(raw, object_pairs_hook=unique_object)


def valid_path(value: Any) -> bool:
    return (isinstance(value, str) and bool(value) and len(value) <= 2048
            and not any(ord(c) < 32 for c in value) and ':' not in value and '\\' not in value
            and all(p not in {'', '.', '..'} for p in value.split('/')))


def inventory(data: Any, *, prefix: str, patterns: list[str], formats: list[str], limit: int) -> dict:
    """Filter saved Git Trees metadata; never treat inventory as an inspected asset."""
    if not prefix and not patterns:
        raise ValueError('an explicit prefix or filename pattern is required')
    if prefix and not valid_path(prefix):
        raise ValueError('prefix must be a clean relative directory path without a trailing slash')
    if not 1 <= limit <= 20 or not formats or not set(formats) <= DATA:
        raise ValueError('limit must be 1..20 and formats must be supported lowercase data extensions')
    if (not isinstance(data, dict) or type(data.get('truncated')) is not bool
            or not isinstance(data.get('tree'), list)
            or not re.fullmatch('[0-9a-f]{40}', str(data.get('sha', '')))):
        raise ValueError('a raw Git Trees response with explicit sha/tree/truncated is required')
    found, seen, excluded = [], set(), 0
    for row in data['tree']:
        if not isinstance(row, dict) or not valid_path(row.get('path')):
            raise ValueError('invalid inventory entry/path')
        path = row['path']
        if path in seen:
            raise ValueError('duplicate inventory path')
        seen.add(path)
        if not re.fullmatch('[0-9a-f]{40}', str(row.get('sha', ''))):
            raise ValueError('invalid inventory blob/tree SHA')
        if row.get('type') != 'blob' or row.get('mode') != '100644':
            excluded += 1
            continue
        size = row.get('size')
        if type(size) is not int or size <= 0:
            raise ValueError('regular blob needs a positive byte size')
        if prefix and not path.startswith(prefix + '/'):
            continue
        if PurePosixPath(path).suffix.lstrip('.').lower() not in formats:
            continue
        if patterns and not any(fnmatch.fnmatchcase(PurePosixPath(path).name.casefold(), p.casefold()) for p in patterns):
            continue
        found.append({k: row[k] for k in ('path', 'sha', 'size')})
    found.sort(key=lambda r: r['path'])
    return {'schema_version': 1, 'status': 'blocked' if data['truncated'] else
            'candidates-only' if found else 'unmatched', 'tree_sha': data['sha'],
            'source_truncated': data['truncated'], 'total_entries': len(data['tree']),
            'excluded_entries': excluded, 'matched_count': len(found),
            'omitted_matches': max(0, len(found) - limit), 'matches': found[:limit],
            'filters': {'prefix': prefix, 'patterns': patterns, 'formats': formats},
            'runtime_validation': 'not-run', 'decoding_validation': 'not-run',
            'scope': 'Metadata candidates only; no file bytes, license review or import evidence.'}


def compact(report: dict, command: str) -> dict:
    """Retain aggregate blockers and only bounded, allowlisted example details."""
    small = {k: report[k] for k in ('status', 'mode', 'catalog_revision', 'summary', 'total_skills',
             'asset_id', 'source_truncated', 'total_entries', 'excluded_entries',
             'matched_count', 'omitted_matches') if k in report}
    if command == 'pin':
        small['status'] = 'lock-created'
        small['file_count'] = len(report['files'])
    small.update(runtime_validation='not-run', decoding_validation='not-run', scope=SCOPE,
                 details_omitted=True)
    selections = [report] if 'matches' in report else []
    decisions = []
    for skill in report.get('skills', []):
        if not skill.get('roles'):
            decisions.append({'skill': skill['skill'], 'status': skill['status']})
        for role in skill.get('roles', []):
            selections.append(role['selection'])
            decisions.append({'skill': skill['skill'], 'role': role['role'], 'status': role['status'],
                              'requires': role['request'].get('requires', []),
                              'formats': role['request'].get('formats', [])})
    reasons = Counter()
    choices, invalid = [], 0
    for selection in selections:
        invalid += len(selection.get('invalid_locks', []))
        for rejection in selection.get('rejected', selection.get('catalog_rejections', [])):
            reasons.update(rejection['reasons'])
        choices.extend(selection.get('matches', []))
    small['invalid_lock_occurrences'] = invalid
    small['rejection_reason_counts'] = dict(sorted(reasons.items()))
    small['choice_count'] = len(choices)
    fields = ('id', 'path', 'sha', 'size', 'status', 'license', 'edition', 'source_url')
    small['choices'] = [{k: r[k] for k in fields if k in r} for r in choices[:3]]
    small['decision_count'] = len(decisions)
    small['blocked_decision_count'] = sum(r['status'] in BLOCKED for r in decisions)
    # Put blocked/unknown requirements first, not after a long list of ready rows.
    decisions.sort(key=lambda r: r['status'] not in BLOCKED)
    small['decisions'] = decisions[:3]
    return small


def encode(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + '\n').encode('utf-8')


def receipt(report: dict, command: str, path: Path, budget: int) -> bytes:
    """Write the full evidence first; never emit a ready/success receipt on write failure."""
    if not 1024 <= budget <= 16384:
        raise ValueError('output byte budget must be between 1024 and 16384')
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    small = compact(report, command)
    report_path = str(path.absolute())
    if len(report_path.encode('utf-8')) > 400:
        raise ValueError('report path too long for a bounded receipt; choose a shorter path')
    small.update(report=report_path, report_bytes=len(raw), report_sha256=hashlib.sha256(raw).hexdigest())
    # Do not truncate serialized JSON. Drop examples, then optional counts; retain status,
    # all-skill denominator/status totals, invalid-lock count and a full-report reference.
    if len(encode(small)) > budget:
        small.pop('choices', None); small.pop('decisions', None)
    if len(encode(small)) > budget:
        small.pop('rejection_reason_counts', None); small.pop('scope', None)
    if len(encode(small)) > budget:
        raise ValueError('receipt exceeds output budget; choose a shorter path or larger budget')
    with path.open('xb') as handle:
        handle.write(raw)
    return encode(small)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True, help='New full JSON file; pin writes a reusable lock here')
    parser.add_argument('--max-output-bytes', type=int, default=4096, help='UTF-8 stdout limit: 1024..16384, default 4096')
    parser.add_argument('--catalog', type=Path, default=PACK / 'assets/catalog.json')
    sub = parser.add_subparsers(dest='command', required=True)
    match = sub.add_parser('match'); match.add_argument('--request', type=Path, required=True)
    select = sub.add_parser('select'); select.add_argument('--request', type=Path, required=True)
    select.add_argument('--root', type=Path, required=True)
    select.add_argument('--locks', nargs='*', type=Path, default=[])
    select.add_argument('--pinned-only', action='store_true')
    prep = sub.add_parser('prepare'); group = prep.add_mutually_exclusive_group(required=True)
    group.add_argument('--skill', nargs='+'); group.add_argument('--all-skills', type=Path)
    prep.add_argument('--root', type=Path); prep.add_argument('--locks', nargs='*', type=Path, default=[])
    prep.add_argument('--pinned-only', action='store_true'); prep.add_argument('--allow-attribution', action='store_true')
    for name in ('pin', 'verify'):
        p = sub.add_parser(name); p.add_argument('--root', type=Path, required=True)
        p.add_argument('--request' if name == 'pin' else '--lock', type=Path, required=True)
        p.add_argument('--allow-attribution', action='store_true')
    inv = sub.add_parser('inventory'); inv.add_argument('--input', type=Path, required=True)
    inv.add_argument('--prefix', default=''); inv.add_argument('--pattern', action='append', default=[])
    inv.add_argument('--formats', nargs='+', default=['glb', 'gltf'])
    inv.add_argument('--limit', type=int, default=20); inv.add_argument('--max-input-bytes', type=int, default=MAX_INPUT)
    args = parser.parse_args()
    try:
        if args.command == 'inventory':
            result = inventory(read_bounded(args.input, args.max_input_bytes), prefix=args.prefix,
                               patterns=args.pattern, formats=args.formats, limit=args.limit)
        else:
            catalog = validate_catalog(read_bounded(args.catalog))
            if args.command == 'match':
                result = match_assets(catalog, read_bounded(args.request))
            elif args.command == 'select':
                result = select_assets(catalog, args.root, args.locks, read_bounded(args.request), pinned_only=args.pinned_only)
            elif args.command == 'prepare':
                names = args.skill
                if args.all_skills:
                    rows = read_bounded(args.all_skills)
                    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
                        raise ValueError('all-skills must be a path catalog array')
                    names = [r.get('name') for r in rows]
                result = prepare(catalog, names, root=args.root, locks=args.locks,
                                 pinned_only=args.pinned_only, allow_attribution=args.allow_attribution)
            elif args.command == 'pin':
                result = make_lock(catalog, args.root, read_bounded(args.request), allow_attribution=args.allow_attribution)
            else:
                result = verify_lock(catalog, args.root, read_bounded(args.lock), allow_attribution=args.allow_attribution)
        output = receipt(result, args.command, args.report, args.max_output_bytes)
        sys.stdout.buffer.write(output)
        return 2 if result.get('status') in BLOCKED else 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        # No unbounded payload/traceback dump into agent context.
        print('Asset context failed: ' + str(exc).replace('\n', ' ')[:240], file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
