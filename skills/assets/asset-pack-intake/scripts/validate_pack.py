#!/usr/bin/env python3
"""Static intake checks for an asset pack (manifest contract v1).

Python 3.10+, standard library only. It reads files, hashes and PNG headers; it never decodes pixels,
runs an engine, downloads anything or judges art. Statuses: pass, fail, not-run.

  python3 validate_pack.py --root /abs/pack [--out report.json] [--plan --engine godot --style pixel-16bit]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

RES = re.compile(r'^(\d+)x(\d+)$')
CODE_SUFFIXES = {'.js', '.mjs', '.ts', '.py', '.gd', '.cs', '.lua', '.cpp', '.h', '.c', '.rs', '.java', '.kt', '.swift', '.gdshader', '.sh'}
SCHEMA = re.compile(r'^[a-z0-9][a-z0-9_.-]*\.asset-pack/1$')
REQUIRED = ['schema', 'name', 'genre', 'version', 'rights', 'logical', 'styles', 'characters', 'levels', 'assets', 'files', 'acceptance_status']
# a gameplay-collision layer may carry a genre name (a kart track's typed surface layer, a fighter stage's floor / bounds)
COLLISION_LAYERS = {'collision', 'surface', 'floor', 'bounds'}
ENGINES = {'godot', 'phaser', 'unity', 'custom', 'threejs', 'pixijs', 'cocos', 'unreal'}


class Report:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def add(self, check: str, ok: bool | None, evidence: str) -> None:
        status = 'not-run' if ok is None else 'pass' if ok else 'fail'
        self.checks.append({'check': check, 'status': status, 'evidence': evidence})

    @property
    def failed(self) -> list[dict]:
        return [c for c in self.checks if c['status'] == 'fail']


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open('rb') as fh:
            head = fh.read(24)
    except OSError:
        return None
    if len(head) < 24 or head[:8] != b'\x89PNG\r\n\x1a\n' or head[12:16] != b'IHDR':
        return None
    return struct.unpack('>II', head[16:24])


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_manifest(root: Path, rep: Report):
    mpath = root / 'pack.json'
    if not mpath.is_file():
        rep.add('manifest.present', False, 'pack.json not found')
        return None
    try:
        m = load(mpath)
    except (OSError, json.JSONDecodeError) as exc:
        rep.add('manifest.parse', False, str(exc))
        return None
    missing = [k for k in REQUIRED if k not in m]
    rep.add('manifest.required_keys', not missing, f'missing: {missing}' if missing else 'all required keys present')
    rep.add('manifest.schema', isinstance(m.get('schema'), str) and bool(SCHEMA.match(m['schema'])), str(m.get('schema')))
    rights = m.get('rights') or {}
    rep.add('manifest.rights', all(k in rights for k in ('originality', 'third_party', 'licence')), 'originality/third_party/licence declared' if rights else 'rights missing')
    tp = rights.get('third_party')
    rep.add('manifest.third_party_sourced', isinstance(tp, list) and all(isinstance(x, dict) and x.get('source') and x.get('licence') for x in tp), f'{len(tp or [])} third-party entries')
    status = m.get('acceptance_status') or {}
    rep.add('manifest.acceptance_status_declared', all(k in status for k in ('engine_import', 'human_playtest')), json.dumps(status, ensure_ascii=False)[:200])
    return m


def check_files(root: Path, m: dict, rep: Report) -> None:
    listed = {f['path']: f for f in m.get('files', []) if isinstance(f, dict) and 'path' in f}
    rep.add('files.listed', bool(listed), f'{len(listed)} files listed')
    bad = []
    for rel, f in sorted(listed.items()):
        p = root / rel
        if not p.is_file():
            bad.append(f'{rel}: missing')
            continue
        data = p.read_bytes()
        if len(data) != f.get('bytes'):
            bad.append(f'{rel}: size {len(data)} != {f.get("bytes")}')
        elif hashlib.sha256(data).hexdigest() != f.get('sha256'):
            bad.append(f'{rel}: sha256 mismatch')
    rep.add('files.integrity', not bad, f'{len(listed)} checked' if not bad else '; '.join(bad[:8]))
    on_disk = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} - {'pack.json'}
    unlisted = sorted(on_disk - set(listed))
    rep.add('files.no_unlisted', not unlisted, 'every file is listed' if not unlisted else f'unlisted: {unlisted[:8]}')
    code = [r for r in on_disk if Path(r).suffix.lower() in CODE_SUFFIXES]
    rep.add('files.no_code', not code, 'no executable code in the pack' if not code else f'code files: {code[:8]}')


def check_atlases(root: Path, rep: Report) -> None:
    problems, count, anims = [], 0, 0
    for p in sorted(root.rglob('*.atlas.json')):
        count += 1
        a = load(p)
        rel = p.relative_to(root).as_posix()
        png = p.parent / a.get('image', '')
        size = png_size(png)
        if size is None:
            problems.append(f'{rel}: image {a.get("image")} missing or not a PNG')
            continue
        if [a['size']['w'], a['size']['h']] != list(size):
            problems.append(f'{rel}: size {a["size"]} != PNG {size}')
        for name, f in a.get('frames', {}).items():
            r = f.get('frame', {})
            if r.get('x', -1) < 0 or r.get('y', -1) < 0 or r.get('x', 0) + r.get('w', 0) > size[0] or r.get('y', 0) + r.get('h', 0) > size[1]:
                problems.append(f'{rel}: frame {name} outside PNG')
            for key in ('source_size', 'trim_offset', 'pivot_px'):
                if key not in f:
                    problems.append(f'{rel}: frame {name} lacks {key}')
            if not (isinstance(f.get('ticks'), int) and f['ticks'] > 0):
                problems.append(f'{rel}: frame {name} ticks must be a positive integer')
        for an in a.get('animations', []):
            anims += 1
            names = an.get('frames', [])
            if not names or any(n not in a['frames'] for n in names):
                problems.append(f'{rel}: animation {an.get("name")} has missing frames')
            if len(an.get('ticks', [])) != len(names):
                problems.append(f'{rel}: animation {an.get("name")} ticks length')
    rep.add('atlas.consistency', not problems and count > 0, f'{count} atlases, {anims} animations' if not problems else '; '.join(problems[:8]))


def check_manifest_animations(root: Path, m: dict, rep: Report) -> None:
    bad, n = [], 0
    for ch in m.get('characters', []):
        for form, f in (ch.get('forms') or {}).items():
            for style, atl in (f.get('atlas') or {}).items():
                if 'atlas' not in atl:  # a 3D style entry: GLB files instead of an atlas
                    glb = atl.get('glb')
                    n += 1
                    if not glb or not (root / glb).is_file():
                        bad.append(f'{ch.get("id")}/{form}/{style}: GLB {glb!r} missing')
                    continue
                ap = root / atl['atlas']
                if not ap.is_file():
                    bad.append(f'{ch.get("id")}/{form}/{style}: atlas missing')
                    continue
                have = {a['name'] for a in load(ap).get('animations', [])}
                for want in f.get('animations', []):
                    n += 1
                    if want not in have:
                        bad.append(f'{ch.get("id")}/{form}/{style}: missing animation {want}')
    rep.add('characters.animations_present', not bad, f'{n} animation references' if not bad else '; '.join(bad[:8]))


def check_tiled(root: Path, rep: Report) -> None:
    problems, maps = [], 0
    for p in sorted(root.rglob('*.tmj')):
        maps += 1
        t = load(p)
        rel = p.relative_to(root).as_posix()
        counts = []
        for ts in t.get('tilesets', []):
            src = (p.parent / ts['source']).resolve() if 'source' in ts else None
            if src is None or not src.is_file():
                problems.append(f'{rel}: tileset {ts.get("source")} missing')
                counts.append((ts.get('firstgid', 1), 0))
                continue
            counts.append((ts['firstgid'], load(src).get('tilecount', 0)))
        top = max((fg + n - 1 for fg, n in counts), default=0)
        for layer in t.get('layers', []):
            if layer.get('type') == 'tilelayer':
                if len(layer['data']) != t['width'] * t['height']:
                    problems.append(f'{rel}: layer {layer["name"]} length')
                if any((not isinstance(g, int)) or g < 0 or g > top for g in layer['data']):
                    problems.append(f'{rel}: layer {layer["name"]} has a gid outside the tilesets')
        names = {layer.get('name') for layer in t.get('layers', [])}
        roles = {p_.get('value') for layer in t.get('layers', []) for p_ in (layer.get('properties') or []) if isinstance(p_, dict) and p_.get('name') == 'role'}
        if not (names & COLLISION_LAYERS or 'collision' in roles):
            problems.append(f'{rel}: no collision layer (one of {sorted(COLLISION_LAYERS)} or a layer with role=collision)')
    rep.add('tiled.maps', not problems and maps > 0, f'{maps} maps' if not problems else '; '.join(problems[:8]))


def check_feel(root: Path, rep: Report) -> None:
    problems, n = [], 0
    for p in sorted(root.glob('data/feel/*.json')):
        d = load(p)

        def walk(o, path):
            nonlocal n
            if isinstance(o, dict):
                if 'value' in o and isinstance(o['value'], (int, float)):
                    n += 1
                    if 'unit' not in o or 'source' not in o:
                        problems.append(f'{p.name}:{path}: numeric entry without unit/source')
                for k, v in o.items():
                    walk(v, f'{path}.{k}' if path else k)
        walk(d, '')
        if 'derived' not in d:
            problems.append(f'{p.name}: no derived outcomes')
    rep.add('feel.provenance', not problems and n > 0, f'{n} numeric entries' if not problems else '; '.join(problems[:8]))


def parse_res(text):
    m = RES.match(text) if isinstance(text, str) else None
    return (int(m.group(1)), int(m.group(2))) if m else None


def check_display(m: dict, rep: Report) -> None:
    """Resolution declaration: every 2D style is a virtual canvas that integer-scales to the target resolution."""
    target = parse_res(m.get('targetResolution') or (m.get('display') or {}).get('targetResolution'))
    if target is None:
        rep.add('display.declared', False, 'pack.json must declare targetResolution as "WxH" (for example 1920x1080)')
        return
    display = m.get('display') or {}
    profiles = display.get('profiles') or {}
    problems, n3d, n2d = [], 0, 0
    for st in m.get('styles', []):
        sid = st.get('id')
        prof = profiles.get(sid) or {}
        if st.get('kind') == '3d' or prof.get('kind') == '3d':
            n3d += 1
            continue
        n2d += 1
        virtual = parse_res(st.get('virtual_resolution') or prof.get('virtualResolution'))
        scale = st.get('integer_scale', prof.get('integerScale'))
        if virtual is None:
            problems.append(f'{sid}: virtual resolution not declared')
            continue
        if not isinstance(scale, int) or isinstance(scale, bool) or scale < 1:
            problems.append(f'{sid}: integer scale must be a whole number >= 1, got {scale!r}')
            continue
        if (virtual[0] * scale, virtual[1] * scale) != target:
            problems.append(f'{sid}: {virtual[0]}x{virtual[1]} x{scale} is not {target[0]}x{target[1]}')
        tile = st.get('tile_px')
        if isinstance(tile, int) and tile > 0 and virtual[0] % tile:
            problems.append(f'{sid}: virtual width {virtual[0]} is not a multiple of tile {tile}')
        if st.get('filter') not in ('nearest', 'linear', 'n/a', None):
            problems.append(f'{sid}: filter {st.get("filter")!r}')
    rep.add('display.integer_scale', not problems and n2d > 0, f'{n2d} 2D styles at integer scale to {target[0]}x{target[1]}; {n3d} 3D styles' if not problems else '; '.join(problems[:8]))


def glb_json(path: Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 20 or data[:4] != b'glTF':
        return None
    length, kind = struct.unpack('<I4s', data[12:20])
    if kind != b'JSON':
        return None
    try:
        return json.loads(data[20:20 + length].decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def check_styles_map(root: Path, m: dict, rep: Report) -> None:
    """styles.json: every asset key resolves to a file in every declared style (the style-switch contract)."""
    declared = (m.get('assets') or {}).get('styles_map')
    path = root / (declared or 'styles.json')
    style_ids = [s.get('id') for s in m.get('styles', [])]
    if not path.is_file():
        rep.add('styles.map', len(style_ids) <= 1, 'single style, no styles.json needed' if len(style_ids) <= 1 else 'multiple styles but no styles.json')
        return
    try:
        sm = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        rep.add('styles.map', False, f'styles.json unreadable: {exc}')
        return
    problems, checked, glbs = [], 0, 0
    if not isinstance(sm.get('schema'), str) or not sm['schema'].endswith('.styles/1'):
        problems.append(f'schema {sm.get("schema")!r}')
    if set(sm.get('styles', {})) != set(style_ids):
        problems.append(f'styles {sorted(sm.get("styles", {}))} != pack.json styles {sorted(style_ids)}')
    if sm.get('default_style') not in style_ids:
        problems.append('default_style is not a declared style')
    assets = sm.get('assets') or {}
    if sm.get('asset_keys') is not None and sm['asset_keys'] != len(assets):
        problems.append(f'asset_keys {sm["asset_keys"]} != {len(assets)}')
    glb_cache: dict[str, dict | None] = {}
    for key, entry in sorted(assets.items()):
        per = entry.get('styles') or {}
        anims = entry.get('animations') or []
        for sid in style_ids:
            e = per.get(sid)
            if not e:
                problems.append(f'{key}: missing in style {sid}')
                continue
            for rel in (e.get('paths') or {}).values():
                if isinstance(rel, str) and not (root / rel).is_file():
                    problems.append(f'{key}@{sid}: file {rel} missing')
            checked += 1
            paths = e.get('paths') or {}
            if paths.get('atlas') and (root / paths['atlas']).is_file() and anims:
                names = {a['name'] for a in load(root / paths['atlas']).get('animations', [])}
                for a in anims:
                    if a not in names and not any(n.endswith(f'_{a}') for n in names):
                        problems.append(f'{key}@{sid}: animation {a} not in atlas')
                        break
            if paths.get('glb') and (root / paths['glb']).is_file():
                glbs += 1
                j = glb_cache.setdefault(paths['glb'], glb_json(root / paths['glb']))
                if j is None:
                    problems.append(f'{key}@{sid}: {paths["glb"]} is not a readable GLB')
                    continue
                nodes = {n.get('name') for n in j.get('nodes', [])}
                clips = {a.get('name') for a in j.get('animations', [])}
                if e.get('node') and e['node'] not in nodes:
                    problems.append(f'{key}@{sid}: node {e["node"]} not in GLB')
                for c in e.get('clips') or []:
                    if c not in clips:
                        problems.append(f'{key}@{sid}: clip {c} not in GLB')
    rep.add('styles.map', not problems and bool(assets), f'{len(assets)} asset keys x {len(style_ids)} styles ({checked} entries, {glbs} GLB references)' if not problems else '; '.join(problems[:8]))


GENRE_PHASES = {
    'platformer': [('movement', ['platform-jump', 'jump-leniency', 'pixel-animation'], ['data/feel/*.json', 'data/animations.json']),
                   ('first level', ['level-blockout', 'level-teach', 'level-design'], ['levels/{style}/*.tmj', 'data/levels/*.level.json']),
                   ('combat and items', ['hitbox-hurtbox', 'attack-tell', 'action-feel'], ['data/boxes/*.json', 'data/enemies/*.json']),
                   ('remaining levels and bosses', ['moving-platform', 'boss-design', 'enemy-ai'], ['data/levels/*.level.json'])],
    'topdown-adventure': [('movement', ['locomotion', 'pixel-animation', 'camera-anti-clip'], ['data/feel/*.json', 'data/animations.json']),
                          ('overworld', ['level-blockout', 'level-design', 'collision-layers'], ['levels/{style}/*.tmj', 'data/levels/*.level.json']),
                          ('combat', ['action-feel', 'hitbox-hurtbox', 'attack-tell'], ['data/boxes/*.json', 'data/enemies/*.json']),
                          ('dungeon and bosses', ['ability-gate', 'level-teach', 'boss-design'], ['data/levels/*.level.json'])],
    'run-and-gun': [('movement', ['locomotion', 'platform-jump', 'pixel-animation'], ['data/feel/*.json']),
                    ('shooting', ['projectile-hitscan', 'aim-assist', 'ammo-reload'], ['data/boxes/*.json']),
                    ('stages', ['level-blockout', 'spawn-wave', 'encounter-design'], ['levels/{style}/*'])],
    'kart': [('handling', ['racing-feel', 'racing-design', 'kb-mouse-map'], ['data/feel/*.json']),
             ('tracks', ['level-blockout', 'racing-design', 'ghost-line'], ['levels/{style}/*'])],
    'fighter': [('moves', ['fighting-design', 'action-feel', 'hitbox-hurtbox'], ['data/**/*.json']),
                ('stages and flow', ['roster-select', 'training-mode', 'gameplay-validation'], ['levels/{style}/*'])],
}


ENGINE_DISPLAY = {
    'godot': 'project.godot [display]: viewport = virtual resolution, stretch mode viewport (pixel) or canvas_items (cartoon), scale_mode integer, default texture filter Nearest (pixel) / Linear',
    'phaser': 'Phaser.Game width/height = virtual resolution, scale.mode NONE with zoom = integer scale, pixelArt true for pixel styles; never a fractional zoom',
    'unity': 'Pixel Perfect Camera: Assets PPU = tile px, reference resolution = virtual resolution, filter Point (pixel) / Bilinear, compression None; game view 1920x1080',
    'custom': 'render to an offscreen canvas of the virtual resolution and blit it at the integer scale; nearest for pixel styles, linear otherwise',
}
SWITCH = 'switch art style by changing one style id; resolve every asset through styles.json (2D: atlas + animation name, 3D: GLB + node + clips), load levels/<style>/, keep logic in tile units and hitboxes from data/boxes'


def display_plan(m: dict, engine: str, style: str) -> dict:
    prof = ((m.get('display') or {}).get('profiles') or {}).get(style) or {}
    return {'target_resolution': m.get('targetResolution'), 'style': style, 'kind': prof.get('kind', '2d'),
            'virtual_resolution': prof.get('virtualResolution'), 'integer_scale': prof.get('integerScale'), 'tile_px': prof.get('tile_px'),
            'engine_settings': ENGINE_DISPLAY.get(engine, ENGINE_DISPLAY['custom']), 'style_switching': SWITCH,
            'styles_available': [s['id'] for s in m.get('styles', [])]}


def resolve_style(m: dict, requested: str) -> str:
    styles = [s['id'] for s in m.get('styles', [])]
    if requested in styles:
        return requested
    return m.get('default_style') if m.get('default_style') in styles else (styles[0] if styles else '?')


def phase_plan(m: dict, engine: str, style: str) -> list[dict]:
    style = resolve_style(m, style)
    root = next((s.get('art_root') for s in m.get('styles', []) if s.get('id') == style), None) or f'styles/{style}'
    plan = [{'phase': 1, 'name': 'intake', 'skills': ['asset-pack-intake', 'sprite-atlas', 'art-bible'], 'engine': engine, 'inputs': [f'{root}/**/*.atlas.json', 'art-bible.md', 'styles.json', 'data/display.json']}]
    for name, skills, inputs in GENRE_PHASES.get(str(m.get('genre')), []):
        plan.append({'phase': len(plan) + 1, 'name': name, 'skills': skills, 'engine': engine, 'inputs': [i.replace('{style}', style) for i in inputs]})
    plan.append({'phase': len(plan) + 1, 'name': 'audio and validation', 'skills': ['audio-feel', 'juice-vfx', 'gameplay-validation'], 'engine': engine, 'inputs': ['data/audio/*.json']})
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--engine', default='unknown')
    ap.add_argument('--style')
    args = ap.parse_args()
    root = args.root.resolve()
    rep = Report()
    m = check_manifest(root, rep)
    if m:
        check_files(root, m, rep)
        check_atlases(root, rep)
        check_manifest_animations(root, m, rep)
        check_tiled(root, rep)
        check_display(m, rep)
        check_styles_map(root, m, rep)
        check_feel(root, rep)
        status = m.get('acceptance_status', {})
        rep.add('engine_import', None, f'declared: {status.get("engine_import", "not-run")}; run the engine adapter import-check')
        rep.add('human_playtest', None, f'declared: {status.get("human_playtest", "not-run")}')
    report = {'schema': 'open-game-skills.pack-intake/1', 'root': str(root), 'checks': rep.checks,
              'failed': [c['check'] for c in rep.failed], 'verdict': 'fail' if rep.failed else 'pass-static-only',
              'note': 'static checks only; engine import, playthrough and audio perception remain not-run unless evidence exists'}
    if args.plan and m and not rep.failed:
        engine = args.engine if args.engine in ENGINES | {'unknown'} else 'custom'
        report['plan'] = phase_plan(m, engine, args.style or '')
        report['display'] = display_plan(m, engine, resolve_style(m, args.style or ''))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + '\n', encoding='utf-8')
    print(text)
    return 1 if rep.failed else 0


if __name__ == '__main__':
    sys.exit(main())
