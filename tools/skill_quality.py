"""Static checks for this skill pack; not an agent or game-runtime evaluator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently accepting the last one."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('YAML mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
ALLOWED = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
LINK = re.compile(r'\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)')


def cells(line: str) -> list[str]:
    return re.split(r'(?<!\\)\|', line.strip().strip('|'))


def markdown_errors(path: Path, text: str, root: Path, *, generated_files: set[Path] | None = None) -> list[str]:
    """Check common tables and inline file links, ignoring fenced examples.

    This intentionally is not a complete CommonMark parser or an HTTP checker.
    Anchors, reference-style links and arbitrary prose skill names are not checked.
    """
    errors, visible = [], []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            visible.append((number, ''))
            continue
        visible.append((number, '' if fence else line))
    for index, (number, line) in enumerate(visible):
        for match in LINK.finditer(line):
            target = match.group(1).strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not (resolved.exists() or resolved in (generated_files or set())):
                errors.append(f'{path}:{number}: missing or out-of-pack link: {target}')
        if not line.lstrip().startswith('|'):
            continue
        parts = cells(line)
        if not all(re.fullmatch(r'\s*:?-{3,}:?\s*', part) for part in parts):
            continue
        if index == 0 or not visible[index - 1][1].lstrip().startswith('|'):
            errors.append(f'{path}:{number}: table separator has no header')
            continue
        width = len(cells(visible[index - 1][1]))
        if len(parts) != width:
            errors.append(f'{path}:{number}: table separator has {len(parts)} cells; expected {width}')
        for row_number, row in visible[index + 1:]:
            if not row.lstrip().startswith('|'):
                break
            if len(cells(row)) != width:
                errors.append(f'{path}:{row_number}: table row has {len(cells(row))} cells; expected {width}')
    return errors


def collect(root: Path, *, generated_files: set[Path] | None = None) -> tuple[list[dict], list[str]]:
    root = root.resolve()
    pack = root / 'skills'
    paths = sorted(pack.rglob('SKILL.md'))
    errors, records, names = [], [], set()
    if not paths:
        return [], ['No SKILL.md files found under skills/']
    for path in paths:
        try:
            text = path.read_text(encoding='utf-8')
            parts = re.split(r'^---\s*$', text, maxsplit=2, flags=re.MULTILINE)
            if len(parts) != 3 or parts[0].strip():
                raise ValueError('missing or unclosed YAML frontmatter')
            meta = yaml.load(parts[1], Loader=UniqueLoader)
            if not isinstance(meta, dict):
                raise ValueError('frontmatter must be a mapping')
            if set(meta) - ALLOWED:
                raise ValueError(f'unknown frontmatter fields: {sorted(set(meta) - ALLOWED)}')
            name, description = meta.get('name'), meta.get('description')
            if not isinstance(name, str) or len(name) > 64 or not NAME.fullmatch(name):
                raise ValueError('invalid skill name')
            expected = 'open-game-skills' if path == pack / 'SKILL.md' else path.parent.name
            if name != expected:
                raise ValueError(f'name must match effective installed directory: {expected}')
            if name in names:
                raise ValueError(f'duplicate skill name: {name}')
            names.add(name)
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError('description must be a nonempty string of at most 1024 characters')
            metadata = meta.get('metadata', {})
            if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
                raise ValueError('metadata must map strings to strings')
            if 'compatibility' in meta and (not isinstance(meta['compatibility'], str) or not 1 <= len(meta['compatibility']) <= 500):
                raise ValueError('compatibility must be a string of 1-500 characters')
            for field in ('license', 'allowed-tools'):
                if field in meta and not isinstance(meta[field], str):
                    raise ValueError(f'{field} must be a string')
            if not parts[2].strip():
                raise ValueError('skill body is empty')
            errors.extend(markdown_errors(path, text, pack, generated_files=generated_files))
            records.append({'name': name, 'path': path.relative_to(pack).as_posix(), 'description': description.strip()})
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return sorted(records, key=lambda row: row['name']), errors


def catalog_text(records: list[dict]) -> str:
    rows = [{'name': row['name'], 'path': row['path']} for row in records]
    return '[\n' + ',\n'.join('  ' + json.dumps(row, ensure_ascii=False) for row in rows) + '\n]\n'


def write_catalog(root: Path, records: list[dict]) -> None:
    (root / 'skills' / 'catalog.json').write_text(catalog_text(records), encoding='utf-8')


def check_catalog(root: Path, records: list[dict]) -> list[str]:
    path = root / 'skills' / 'catalog.json'
    if not path.is_file() or path.read_text(encoding='utf-8') != catalog_text(records):
        return ['skills/catalog.json is stale; run python tools/skill_quality.py --write-catalog']
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write-catalog', action='store_true')
    parser.add_argument('--check-catalog', action='store_true')
    args = parser.parse_args()
    args.root = args.root.resolve()
    generated = {args.root / 'skills/catalog.json'} if args.write_catalog else set()
    records, errors = collect(args.root, generated_files=generated)
    docs = set(args.root.glob('*.md')) | set((args.root / 'docs').rglob('*.md')) | set((args.root / 'skills').rglob('*.md'))
    for path in sorted(docs):
        if path.name != 'SKILL.md':
            boundary = args.root / 'skills' if path.is_relative_to(args.root / 'skills') else args.root
            errors.extend(markdown_errors(path, path.read_text(encoding='utf-8'), boundary, generated_files=generated))
    if args.write_catalog and not errors:
        write_catalog(args.root, records)
    if args.check_catalog:
        errors.extend(check_catalog(args.root, records))
    for error in errors:
        print(error)
    print(f'{len(records)} skills inspected; {len(errors)} static errors. Runtime/agent behavior: not evaluated.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
