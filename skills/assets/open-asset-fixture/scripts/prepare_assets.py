"""Prepare offline library-first fixture plans; no download, decode, model or engine run.

Exit 0: a complete plan (may still need acquisition), 2: blocked or missing
requirements, 1: invalid input. Inspect the JSON status before starting a game test.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Any

from asset_fixture import PACK, load_catalog, plan_for_skill, read_json, strings
from fixture_lock import select_assets

STATES = ('ready-for-import', 'needs-acquisition', 'not-needed', 'needs-requirements', 'blocked')


def prepare(catalog: dict[str, Any], skills: list[str], *, root: Path | None = None,
            locks: list[Path] | None = None, pinned_only: bool = False,
            allow_attribution: bool = False) -> dict[str, Any]:
    """Keep every requested skill in the denominator; missing profiles are not passes."""
    strings(skills, 'skills', nonempty=True)
    if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) for name in skills):
        raise ValueError('skill names must be lowercase hyphenated identifiers')
    if type(pinned_only) is not bool or type(allow_attribution) is not bool:
        raise ValueError('policy flags must be booleans')
    if locks and root is None:
        raise ValueError('an explicit fixture root is required when using local locks')
    rows = []
    for name in skills:
        initial = plan_for_skill(catalog, name, allow_attribution)
        if initial['status'] in {'not-needed', 'needs-requirements'}:
            rows.append(initial)
            continue
        roles = []
        for role in initial['roles']:
            selection = select_assets(catalog, root or Path.cwd(), locks or [], role['request'],
                                      pinned_only=pinned_only)
            local = any(a['status'] == 'local-integrity-verified' for a in selection['matches'])
            state = ('ready-for-import' if local else 'needs-acquisition') if selection['status'] == 'matched' else 'blocked'
            roles.append({'role': role['role'], 'request': role['request'], 'status': state,
                          'selection': selection})
        state = ('blocked' if any(r['status'] == 'blocked' for r in roles) else
                 'ready-for-import' if all(r['status'] == 'ready-for-import' for r in roles) else
                 'needs-acquisition')
        rows.append({'skill': name, 'status': state, 'roles': roles, 'runtime_validation': 'not-run'})
    counts = Counter(row['status'] for row in rows)
    state = ('blocked' if counts['blocked'] or counts['needs-requirements'] else
             'needs-acquisition' if counts['needs-acquisition'] else
             'ready-for-import' if counts['ready-for-import'] else 'not-needed')
    return {'schema_version': 1, 'catalog_revision': catalog['revision'],
            'mode': 'pinned-only' if pinned_only else 'library-first', 'status': state,
            'total_skills': len(rows), 'summary': {s: counts[s] for s in STATES}, 'skills': rows,
            'decoding_validation': 'not-run', 'runtime_validation': 'not-run',
            'scope': 'Fixture selection and local byte consistency only; import, dependency, visual and gameplay checks are separate.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=PACK / 'assets/catalog.json')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--skill', nargs='+', help='One or more explicit skill names')
    group.add_argument('--all-skills', type=Path, help='Pack path catalog JSON; every entry stays in the report')
    parser.add_argument('--root', type=Path, help='Read-only local fixture directory')
    parser.add_argument('--locks', nargs='*', type=Path, default=[])
    parser.add_argument('--pinned-only', action='store_true', help='No unpinned discovery fallback; intended for CI')
    parser.add_argument('--allow-attribution', action='store_true')
    parser.add_argument('--output', type=Path, help='Write a new report; existing files are never overwritten')
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.catalog)
        names = args.skill
        if args.all_skills:
            inventory = read_json(args.all_skills)
            if not isinstance(inventory, list) or any(not isinstance(r, dict) for r in inventory):
                raise ValueError('all-skills must be a path catalog array')
            names = [r.get('name') for r in inventory]
        report = prepare(catalog, names, root=args.root, locks=args.locks,
                         pinned_only=args.pinned_only, allow_attribution=args.allow_attribution)
        text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as f:
                f.write(text)
        else:
            print(text, end='')
        return 2 if report['status'] == 'blocked' else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Asset preparation failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
