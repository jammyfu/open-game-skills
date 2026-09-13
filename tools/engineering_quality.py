"""Validate engineering contracts and imported evidence; never run or judge a model."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

IDENT = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
STATUSES = ('pass', 'fail', 'blocked', 'not-run')
KINDS = {'normal', 'boundary', 'adversarial'}
MAX_JSON_BYTES = 2 * 1024 * 1024


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def shape(value: object, fields: set[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == fields, f'{label}: expected fields {sorted(fields)}')


def unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path: Path) -> object:
    require(path.stat().st_size <= MAX_JSON_BYTES, f'{path}: JSON exceeds size limit')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def contained_file(base: Path, relative: object) -> Path:
    require(text(relative), 'file path must be a nonempty relative POSIX path')
    require('\\' not in relative and ':' not in relative, 'file path must be local and use POSIX separators')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and '..' not in path.parts, f'unsafe file path: {relative}')
    resolved = (base / str(path)).resolve()
    require(resolved.is_relative_to(base.resolve()) and resolved.is_file(), f'missing or out-of-bound file: {relative}')
    return resolved


def string_list(value: object, label: str, *, allow_empty: bool = False) -> list[str]:
    require(isinstance(value, list) and (allow_empty or bool(value)), f'{label}: expected list')
    require(all(isinstance(v, str) and IDENT.fullmatch(v) for v in value), f'{label}: invalid identifier')
    require(len(set(value)) == len(value), f'{label}: duplicate identifier')
    return value


def table_modes(body: str) -> list[str]:
    # Deliberately supports the project's simple, unescaped two-column Modes tables.
    sections = re.findall(r'^## Modes\s*\n(.*?)(?=^## |\Z)', body, re.M | re.S)
    require(len(sections) == 1, 'exactly one Modes section is required')
    modes = re.findall(r'^\| ([a-z0-9]+(?:-[a-z0-9]+)*) \|', sections[0], re.M)
    return string_list(modes, 'Modes table')


def fingerprint(pack: Path) -> str:
    """Bind evidence to the pack's Markdown and JSON, not just unchanged prompts."""
    digest = hashlib.sha256()
    paths = sorted(set(pack.rglob('*.md')) | set(pack.rglob('*.json')))
    for path in paths:
        relative = path.relative_to(pack).as_posix()
        source = contained_file(pack, relative)
        digest.update(relative.encode('utf-8') + b'\0')
        digest.update(hashlib.sha256(source.read_bytes()).digest())
    return digest.hexdigest()


def load_suite(root: Path) -> dict:
    pack = root.resolve() / 'skills'
    registry = read_json(contained_file(pack, 'engineering-registry.json'))
    shape(registry, {'schema_version', 'scope', 'entries'}, 'registry')
    require(type(registry['schema_version']) is int and registry['schema_version'] == 1, 'unsupported registry version')
    require(registry['scope'] == 'engineering-core-v1', 'unsupported registry scope')
    entries = registry['entries']
    require(isinstance(entries, dict) and bool(entries), 'registry entries must be a nonempty object')
    available = {'open-game-skills' if p == pack / 'SKILL.md' else p.parent.name for p in pack.rglob('SKILL.md')}
    cases = {}
    for name, entry in entries.items():
        require(isinstance(name, str) and IDENT.fullmatch(name), 'invalid registry skill name')
        shape(entry, {'owner', 'modes', 'optional_dependencies'}, name)
        require(entry['owner'] == name, f'{name}: this registry requires an explicit self-owned contract')
        modes = string_list(entry['modes'], f'{name} modes')
        dependencies = string_list(entry['optional_dependencies'], f'{name} optional_dependencies', allow_empty=True)
        require(set(dependencies) <= available and name not in dependencies, f'{name}: unknown or self dependency')
        folder = f'disciplines/{name}'
        body = contained_file(pack, f'{folder}/SKILL.md').read_text(encoding='utf-8')
        require(re.search(r'^name: ' + re.escape(name) + r'\s*$', body, re.M) is not None, f'{name}: frontmatter name mismatch')
        require(table_modes(body) == modes, f'{name}: registry and actual Modes table differ')
        example = read_json(contained_file(pack, f'{folder}/assets/contract.example.json'))
        require(isinstance(example, dict), f'{name}: example must be an object')
        require(type(example.get('schema_version')) is int and example['schema_version'] == 1, f'{name}: invalid example version')
        require(example.get('skill') == name and example.get('mode') in modes and example.get('status') == 'not-run', f'{name}: invalid example mode/skill/status')
        rows = read_json(contained_file(pack, f'{folder}/assets/evals.json'))
        require(isinstance(rows, list) and bool(rows), f'{name}: missing evaluation cases')
        kinds = set()
        for row in rows:
            shape(row, {'id', 'skill', 'kind', 'prompt', 'criteria'}, f'{name} case')
            cid = row['id']
            require(isinstance(cid, str) and IDENT.fullmatch(cid) and cid not in cases, f'{name}: invalid or duplicate case ID')
            require(row['skill'] == name and isinstance(row['kind'], str) and row['kind'] in KINDS, f'{cid}: invalid skill or kind')
            require(text(row['prompt']), f'{cid}: empty prompt')
            criteria = row['criteria']
            require(isinstance(criteria, dict) and bool(criteria), f'{cid}: criteria must be nonempty')
            require(all(isinstance(k, str) and IDENT.fullmatch(k) and text(v) for k, v in criteria.items()), f'{cid}: invalid criterion')
            kinds.add(row['kind'])
            cases[cid] = row
        require(kinds == KINDS, f'{name}: missing normal, boundary or adversarial case')
    return {'entries': entries, 'cases': cases, 'sha256': fingerprint(pack)}


def result_template(suite: dict) -> dict:
    return {
        'schema_version': 1,
        'suite_sha256': suite['sha256'],
        'subject': {key: None for key in ('commit', 'model', 'driver', 'configuration', 'evaluated_at')},
        'results': [{'case_id': cid, 'status': 'not-run', 'reason': 'No invocation recorded.'} for cid in sorted(suite['cases'])],
    }


def validate_results(data: object, suite: dict, evidence_root: Path) -> dict[str, int]:
    shape(data, {'schema_version', 'suite_sha256', 'subject', 'results'}, 'evaluation record')
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'unsupported result version')
    require(data['suite_sha256'] == suite['sha256'], 'stale suite fingerprint; do not relabel old results')
    subject = data['subject']
    shape(subject, {'commit', 'model', 'driver', 'configuration', 'evaluated_at'}, 'subject')
    rows = data['results']
    require(isinstance(rows, list), 'results must be a list')
    counts = {status: 0 for status in STATUSES}
    seen = set()
    executed = False
    for row in rows:
        require(isinstance(row, dict), 'result row must be an object')
        cid, status = row.get('case_id'), row.get('status')
        require(isinstance(cid, str) and cid in suite['cases'] and cid not in seen, 'unknown or duplicate result case')
        require(isinstance(status, str) and status in STATUSES, f'{cid}: invalid status')
        seen.add(cid)
        counts[status] += 1
        if status in ('blocked', 'not-run'):
            shape(row, {'case_id', 'status', 'reason'}, cid)
            require(text(row['reason']), f'{cid}: reason is required')
            continue
        executed = True
        shape(row, {'case_id', 'status', 'response', 'judgment'}, cid)
        response = row['response']
        shape(response, {'path', 'sha256'}, f'{cid} response')
        artifact = contained_file(evidence_root, response['path'])
        require(0 < artifact.stat().st_size <= MAX_JSON_BYTES, f'{cid}: response must be nonempty and at most 2 MiB')
        raw = artifact.read_bytes()
        require(text(raw.decode('utf-8')), f'{cid}: response must contain UTF-8 text')
        require(isinstance(response['sha256'], str) and re.fullmatch(r'[a-f0-9]{64}', response['sha256']), f'{cid}: invalid response hash')
        require(hashlib.sha256(raw).hexdigest() == response['sha256'], f'{cid}: response hash mismatch')
        judgment = row['judgment']
        shape(judgment, {'reviewer', 'method', 'criteria'}, f'{cid} judgment')
        require(text(judgment['reviewer']) and judgment['method'] in ('human-review', 'model-judge'), f'{cid}: reviewer and method required')
        criteria = judgment['criteria']
        require(isinstance(criteria, dict) and set(criteria) == set(suite['cases'][cid]['criteria']), f'{cid}: all and only the case criteria must be assessed')
        assessments = []
        for key, assessment in criteria.items():
            shape(assessment, {'status', 'reason'}, f'{cid}/{key}')
            require(assessment['status'] in ('pass', 'fail') and text(assessment['reason']), f'{cid}/{key}: judgment and evidence reason required')
            assessments.append(assessment['status'])
        expected = 'pass' if all(s == 'pass' for s in assessments) else 'fail'
        require(status == expected, f'{cid}: overall result disagrees with criteria')
    if executed:
        require(all(text(v) for v in subject.values()), 'executed results require full subject metadata')
        require(re.fullmatch(r'[a-f0-9]{40}|[a-f0-9]{64}', subject['commit']) is not None, 'subject commit must be a full immutable hash, not a branch')
        stamp = datetime.fromisoformat(subject['evaluated_at'].replace('Z', '+00:00'))
        require(stamp.tzinfo is not None and stamp.utcoffset() is not None, 'evaluated_at needs a timezone')
    counts['not-run'] += len(suite['cases']) - len(seen)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--results', type=Path, help='Imported record; local response paths resolve beside this file')
    group.add_argument('--write-template', type=Path, help='Create a not-run template; never overwrite')
    parser.add_argument('--require-passed', action='store_true', help='Exit 1 unless every authored case is recorded as passed')
    args = parser.parse_args()
    try:
        suite = load_suite(args.root)
        data = read_json(args.results) if args.results else result_template(suite)
        base = args.results.resolve().parent if args.results else args.root
        counts = validate_results(data, suite, base)
        if args.write_template:
            with args.write_template.open('x', encoding='utf-8') as handle:
                handle.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'registered_skills': len(suite['entries']), 'cases': len(suite['cases']), 'suite_sha256': suite['sha256'], **counts, 'validation': 'record consistency, not authenticity or semantic correctness; no model/engine executed'}, ensure_ascii=False, indent=2))
        return 1 if args.require_passed and counts['pass'] != len(suite['cases']) else 0
    except (OSError, ValueError, UnicodeError) as exc:
        print(f'Engineering validation failed: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
