"""Deterministic per-skill contract checks; never executes or judges an LLM/game runtime."""
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any
import yaml

import skill_quality

ACCEPTANCE = re.compile(r'(?im)^#{1,3}\s*(?:accept|acceptance|verification|verify|evidence|done|test)\b|^\s*Accept\s*:')


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8')
    parts = re.split(r'^---\s*$', text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('missing or unclosed YAML frontmatter')
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    return data


def trigger_text(description: str, name: str) -> str:
    text = ' '.join(description.split()).strip()
    if text.lower().startswith('use when '):
        text = text[9:].rstrip('.')
    return text or f'the project explicitly needs the documented responsibility of {name}'


def materialize_scenarios(root: Path, case: dict[str, Any]) -> list[dict[str, Any]]:
    if case.get('review_state') == 'reviewed':
        rows = case.get('scenarios')
        if not isinstance(rows, list):
            raise ValueError(f"{case.get('skill')}: reviewed case is missing scenarios")
        return rows
    profile_id = case.get('scenario_profile')
    if not isinstance(profile_id, str) or not profile_id:
        raise ValueError(f"{case.get('skill')}: seeded case is missing scenario_profile")
    profile_path = root / 'tests' / 'skills' / 'profiles' / f'{profile_id}.json'
    profile = read_json(profile_path)
    if profile.get('id') != profile_id:
        raise ValueError(f'{profile_id}: profile id mismatch')
    meta = frontmatter(root / 'skills' / case['skill_path'])
    description = meta.get('description')
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{case.get('skill')}: missing description")
    values = {'skill': case['skill'], 'trigger': trigger_text(description, case['skill'])}
    rows = []
    for kind in profile.get('scenario_kinds', []):
        template = profile.get('templates', {}).get(kind)
        if not isinstance(template, str):
            raise ValueError(f'{profile_id}: missing template {kind}')
        criteria = profile.get('criteria')
        if not isinstance(criteria, dict) or len(criteria) < 3:
            raise ValueError(f'{profile_id}: insufficient criteria')
        rows.append({
            'id': f"{case['skill']}-{kind}",
            'kind': kind,
            'prompt': template.format(**values),
            'criteria': {key: value.format(**values) for key, value in criteria.items()},
        })
    return rows


def fixture_ids(root: Path) -> set[str]:
    folder = root / 'tests' / 'skills' / 'fixtures'
    result = set()
    if not folder.is_dir():
        return result
    for path in folder.glob('*.json'):
        data = read_json(path)
        value = data.get('id')
        if isinstance(value, str):
            result.add(value)
    return result


def check_case(root: Path, case_path: Path, catalog: dict[str, str], fixtures: set[str]) -> tuple[list[str], dict[str, list[str]]]:
    hard: list[str] = []
    candidates: dict[str, list[str]] = {'description_trigger': [], 'acceptance_signal': [], 'seeded_case': []}
    rel_case = case_path.relative_to(root).as_posix()
    try:
        case = read_json(case_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f'{rel_case}: invalid JSON: {exc}'], candidates
    skill = case.get('skill')
    skill_path = case.get('skill_path')
    if not isinstance(skill, str) or skill not in catalog:
        return [f'{rel_case}: unknown skill {skill!r}'], candidates
    if catalog[skill] != skill_path:
        hard.append(f'{skill}: case path {skill_path!r} does not match catalog {catalog[skill]!r}')
    expected_case = f"tests/skills/cases/{case.get('category')}/{skill}.json"
    if rel_case != expected_case:
        hard.append(f'{skill}: case file is at {rel_case}, expected {expected_case}')
    source = root / 'skills' / catalog[skill]
    if not source.is_file():
        hard.append(f'{skill}: missing skill source {catalog[skill]}')
        return hard, candidates
    try:
        meta = frontmatter(source)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        hard.append(f'{skill}: frontmatter error: {exc}')
        return hard, candidates
    if meta.get('name') != skill:
        hard.append(f'{skill}: frontmatter name mismatch')
    description = meta.get('description')
    if not isinstance(description, str) or not description.strip():
        hard.append(f'{skill}: missing description')
    elif not description.strip().lower().startswith('use when '):
        candidates['description_trigger'].append(skill)
    body = source.read_text(encoding='utf-8')
    if not ACCEPTANCE.search(body):
        candidates['acceptance_signal'].append(skill)
    hard.extend(skill_quality.markdown_errors(source, body, root / 'skills'))
    try:
        scenarios = materialize_scenarios(root, case)
        kinds = [row.get('kind') for row in scenarios]
        if kinds != ['normal', 'boundary', 'adversarial']:
            hard.append(f'{skill}: scenarios must be ordered normal/boundary/adversarial')
        for row in scenarios:
            if not isinstance(row.get('prompt'), str) or not row['prompt'].strip():
                hard.append(f"{skill}/{row.get('kind')}: empty prompt")
            criteria = row.get('criteria')
            if not isinstance(criteria, dict) or len(criteria) < 3 or not all(isinstance(v, str) and v.strip() for v in criteria.values()):
                hard.append(f"{skill}/{row.get('kind')}: invalid criteria")
            if 'result' in row or 'status' in row:
                hard.append(f"{skill}/{row.get('kind')}: case definition may not contain measured results")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        hard.append(f'{skill}: scenario error: {exc}')
    refs = case.get('fixtures', [])
    if refs is not None:
        if not isinstance(refs, list) or not all(isinstance(v, str) for v in refs):
            hard.append(f'{skill}: fixtures must be a string list')
        else:
            for fixture in refs:
                if fixture not in fixtures:
                    hard.append(f'{skill}: unknown fixture {fixture}')
    if case.get('review_state') == 'seeded':
        candidates['seeded_case'].append(skill)
    elif case.get('review_state') != 'reviewed':
        hard.append(f'{skill}: invalid review_state')
    return hard, candidates


def check_all(root: Path) -> dict[str, Any]:
    root = root.resolve()
    catalog_rows = read_json(root / 'skills' / 'catalog.json')
    catalog = {row['name']: row['path'] for row in catalog_rows}
    hard: list[str] = []
    candidates = {'description_trigger': [], 'acceptance_signal': [], 'seeded_case': []}
    if len(catalog) != len(catalog_rows):
        hard.append('catalog contains duplicate skill names')
    cases = sorted((root / 'tests' / 'skills' / 'cases').rglob('*.json'))
    if len(cases) != len(catalog):
        hard.append(f'case count {len(cases)} != catalog count {len(catalog)}')
    fixtures = fixture_ids(root)
    for path in cases:
        errors, found = check_case(root, path, catalog, fixtures)
        hard.extend(errors)
        for key, values in found.items():
            candidates[key].extend(values)
    root_entry = (root / 'skills' / 'SKILL.md').read_text(encoding='utf-8')
    if 'catalog.json' not in root_entry:
        hard.append('root skill does not expose catalog fallback for explicit skill names')
    return {
        'skills': len(catalog),
        'hard_errors': sorted(set(hard)),
        'review_candidates': {key: sorted(set(values)) for key, values in candidates.items()},
        'behavioral_validation': 'not-run unless separate evidence records exist',
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = check_all(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['hard_errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
