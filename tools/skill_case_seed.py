"""Seed deterministic per-skill evaluation cases without claiming behavioral results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import yaml


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'{path}: missing YAML frontmatter')
    end = text.find('\n---\n', 4)
    if end < 0:
        raise ValueError(f'{path}: unterminated YAML frontmatter')
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError(f'{path}: frontmatter is not an object')
    return data


def category_for(skill_path: str) -> str:
    parts = Path(skill_path).parts
    return 'root' if len(parts) == 1 else parts[0]


def case_relpath(name: str, skill_path: str) -> str:
    return f'tests/skills/cases/{category_for(skill_path)}/{name}.json'


def trigger_text(description: str, name: str) -> str:
    text = ' '.join(description.split()).strip()
    if text.lower().startswith('use when '):
        text = text[9:].rstrip('.')
    if not text:
        return f'the project explicitly needs the documented responsibility of {name}'
    return text[0].lower() + text[1:]


def seeded_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        'schema_version': 1,
        'skill': row['skill'],
        'skill_path': row['skill_path'],
        'category': row['category'],
        'review_state': 'seeded',
        'scenario_profile': 'default-v1',
    }


def seed_cases(root: Path) -> dict[str, Any]:
    root = root.resolve()
    skills_root = root / 'skills'
    catalog = json.loads((skills_root / 'catalog.json').read_text(encoding='utf-8'))
    entries = []
    for row in catalog:
        name = row['name']
        skill_path = row['path']
        source = skills_root / skill_path
        meta = frontmatter(source)
        description = meta.get('description')
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f'{skill_path}: missing description')
        category = category_for(skill_path)
        case_path = case_relpath(name, skill_path)
        entries.append({
            'skill': name,
            'skill_path': skill_path,
            'category': category,
            'case_path': case_path,
        })
    entries.sort(key=lambda row: row['skill_path'])
    return {'schema_version': 1, 'entries': entries}


def write_cases(root: Path, *, overwrite_seeded: bool = False) -> dict[str, Any]:
    root = root.resolve()
    coverage = seed_cases(root)
    for row in coverage['entries']:
        case_path = root / row['case_path']
        case_path.parent.mkdir(parents=True, exist_ok=True)
        payload = seeded_payload(row)
        if case_path.exists():
            current = json.loads(case_path.read_text(encoding='utf-8'))
            if current.get('review_state') == 'reviewed':
                continue
            if not overwrite_seeded:
                continue
        case_path.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    corpus = root / 'tests' / 'skills'
    corpus.mkdir(parents=True, exist_ok=True)
    compact = {'schema_version': 1, 'skills': [row['skill'] for row in coverage['entries']]}
    (corpus / 'coverage.json').write_text(json.dumps(compact, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--overwrite-seeded', action='store_true')
    args = parser.parse_args()
    coverage = write_cases(args.root, overwrite_seeded=args.overwrite_seeded) if args.write else seed_cases(args.root)
    print(json.dumps({'skills': len(coverage['entries']), 'write': args.write}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
