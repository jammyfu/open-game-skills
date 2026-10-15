"""Static tests for the asset-pack-intake validator and its registration; not agent or engine evaluations."""
from pathlib import Path
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/assets/asset-pack-intake'
VALIDATOR = SKILL / 'scripts/validate_pack.py'


def png(path: Path, w: int, h: int) -> None:
    raw = b''.join(b'\x00' + bytes([255, 0, 0, 255]) * w for _ in range(h))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def build_pack(root: Path) -> None:
    """A minimal but complete synthetic pack (one actor, one tileset, one map, feel data)."""
    png(root / 'art/s/characters/hero/big.png', 8, 4)
    frames = {f'hero_big_idle_{i}': {'frame': {'x': i * 4, 'y': 0, 'w': 4, 'h': 4}, 'source_size': {'w': 4, 'h': 4}, 'trim_offset': {'x': 0, 'y': 0}, 'pivot_px': {'x': 2, 'y': 4}, 'ticks': 5, 'duration_ms': 83.33} for i in range(2)}
    write_json(root / 'art/s/characters/hero/big.atlas.json', {'schema': 'x.atlas/1', 'image': 'big.png', 'size': {'w': 8, 'h': 4}, 'frames': frames, 'animations': [{'name': 'idle', 'frames': list(frames), 'loop': True, 'ticks': [5, 5]}], 'logical_tick_hz': 60})
    png(root / 'art/s/tiles/tileset.png', 8, 8)
    write_json(root / 'art/s/tiles/tileset.tsj', {'type': 'tileset', 'name': 't', 'tilecount': 4, 'columns': 2, 'tilewidth': 4, 'tileheight': 4, 'image': 'tileset.png', 'tiles': [{'id': 0, 'type': 'solid'}]})
    write_json(root / 'levels/s/l1.tmj', {'type': 'map', 'width': 2, 'height': 2, 'tilewidth': 4, 'tileheight': 4, 'tilesets': [{'firstgid': 1, 'source': '../../art/s/tiles/tileset.tsj'}],
                                          'layers': [{'type': 'tilelayer', 'name': 'terrain', 'width': 2, 'height': 2, 'data': [1, 0, 2, 4]}, {'type': 'tilelayer', 'name': 'collision', 'width': 2, 'height': 2, 'data': [0, 0, 0, 0]}]})
    write_json(root / 'data/feel/g.feel.json', {'walk': {'value': 1.6, 'unit': 'px/frame', 'source': 'original-suggestion'}, 'derived': {'jump_tiles': 4}})
    listed = []
    for p in sorted(root.rglob('*')):
        if p.is_file():
            data = p.read_bytes()
            listed.append({'path': p.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'role': 'data'})
    write_json(root / 'pack.json', {
        'schema': 'acme.asset-pack/1', 'name': 'mini', 'genre': 'platformer', 'version': '1.0.0',
        'rights': {'originality': 'original', 'third_party': [], 'licence': 'owner'},
        'logical': {'tick_hz': 60, 'unit': 'px16', 'coordinate_system': {'origin': 'top-left'}, 'facing': 'right', 'actor_pivot': 'bottom-center'},
        'styles': [{'id': 's', 'tile_px': 4, 'filter': 'nearest', 'art_root': 'art/s', 'level_root': 'levels/s'}],
        'characters': [{'id': 'hero', 'role': 'hero', 'forms': {'big': {'animations': ['idle'], 'atlas': {'s': {'atlas': 'art/s/characters/hero/big.atlas.json', 'png': 'art/s/characters/hero/big.png'}}}}}],
        'levels': [{'id': 'l1', 'tmj': {'s': 'levels/s/l1.tmj'}}], 'assets': {'feel': 'data/feel/g.feel.json'},
        'acceptance_status': {'engine_import': 'not-run', 'human_playtest': 'not-run'}, 'files': listed})


def run(root: Path, *extra: str):
    proc = subprocess.run([sys.executable, str(VALIDATOR), '--root', str(root), *extra], capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout)


class AssetPackIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'pack'
        self.root.mkdir()
        build_pack(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def reseal(self):
        m = json.loads((self.root / 'pack.json').read_text())
        listed = []
        for p in sorted(self.root.rglob('*')):
            if p.is_file() and p.name != 'pack.json':
                data = p.read_bytes()
                listed.append({'path': p.relative_to(self.root).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'role': 'data'})
        m['files'] = listed
        write_json(self.root / 'pack.json', m)

    def test_valid_pack_passes_static_checks_and_leaves_engine_import_not_run(self):
        code, report = run(self.root, '--plan', '--engine', 'godot', '--style', 's')
        self.assertEqual(code, 0, report['failed'])
        self.assertEqual(report['verdict'], 'pass-static-only')
        status = {c['check']: c['status'] for c in report['checks']}
        self.assertEqual(status['engine_import'], 'not-run')
        self.assertEqual(status['human_playtest'], 'not-run')
        self.assertEqual(status['files.integrity'], 'pass')
        self.assertLessEqual(max(len(p['skills']) for p in report['plan']), 3)
        self.assertTrue(all(p['engine'] == 'godot' for p in report['plan']))

    def test_report_is_deterministic_for_the_same_bytes(self):
        self.assertEqual(run(self.root)[1], run(self.root)[1])

    def test_missing_file_and_changed_hash_fail(self):
        (self.root / 'art/s/tiles/tileset.png').unlink()
        code, report = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn('files.integrity', report['failed'])
        build_pack_dir = Path(self.tmp.name) / 'p2'
        build_pack_dir.mkdir()
        build_pack(build_pack_dir)
        (build_pack_dir / 'data/feel/g.feel.json').write_text('{"changed": true}\n')
        code, report = run(build_pack_dir)
        self.assertIn('files.integrity', report['failed'])

    def test_atlas_rectangle_outside_png_fails(self):
        p = self.root / 'art/s/characters/hero/big.atlas.json'
        a = json.loads(p.read_text())
        a['frames']['hero_big_idle_1']['frame']['x'] = 6
        write_json(p, a)
        self.reseal()
        code, report = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn('atlas.consistency', report['failed'])

    def test_map_gid_past_tileset_and_missing_collision_layer_fail(self):
        p = self.root / 'levels/s/l1.tmj'
        m = json.loads(p.read_text())
        m['layers'][0]['data'] = [1, 0, 2, 99]
        write_json(p, m)
        self.reseal()
        code, report = run(self.root)
        self.assertIn('tiled.maps', report['failed'])
        m['layers'][0]['data'] = [1, 0, 2, 4]
        m['layers'] = m['layers'][:1]
        write_json(p, m)
        self.reseal()
        self.assertIn('tiled.maps', run(self.root)[1]['failed'])

    def test_animation_without_frames_and_missing_manifest_animation_fail(self):
        p = self.root / 'pack.json'
        m = json.loads(p.read_text())
        m['characters'][0]['forms']['big']['animations'].append('walk')
        write_json(p, m)
        code, report = run(self.root)
        self.assertIn('characters.animations_present', report['failed'])

    def test_feel_numbers_need_unit_and_source(self):
        write_json(self.root / 'data/feel/g.feel.json', {'walk': {'value': 1.6}, 'derived': {}})
        self.reseal()
        self.assertIn('feel.provenance', run(self.root)[1]['failed'])

    def test_shipped_code_and_unlisted_files_fail(self):
        (self.root / 'game.gd').write_text('extends Node\n')
        code, report = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn('files.no_code', report['failed'])
        self.assertIn('files.no_unlisted', report['failed'])

    def test_rights_and_acceptance_declarations_are_required(self):
        p = self.root / 'pack.json'
        m = json.loads(p.read_text())
        del m['rights']['licence']
        m['rights']['third_party'] = [{'name': 'x'}]
        write_json(p, m)
        failed = run(self.root)[1]['failed']
        self.assertIn('manifest.rights', failed)
        self.assertIn('manifest.third_party_sourced', failed)

    def test_skill_is_registered_with_owner_tables_and_all_readme_locales(self):
        catalog = {row['name']: row['path'] for row in json.loads((ROOT / 'skills/catalog.json').read_text())}
        self.assertEqual(catalog['asset-pack-intake'], 'assets/asset-pack-intake/SKILL.md')
        coverage = json.loads((ROOT / 'tests/skills/coverage.json').read_text())
        self.assertIn('asset-pack-intake', coverage['skills'])
        self.assertTrue((ROOT / 'tests/skills/cases/assets/asset-pack-intake.json').is_file())
        self.assertIn('asset-pack-intake', (ROOT / 'skills/dispatcher/SKILL.md').read_text())
        self.assertIn('Pack intake and validation', (ROOT / 'skills/CONTRACT.md').read_text())
        for name in ('README.md', 'README.zh.md', 'README.zh-Hant.md', 'README.ja.md', 'README.ko.md'):
            with self.subTest(locale=name):
                text = (ROOT / name).read_text(encoding='utf-8')
                self.assertIn('skills/assets/asset-pack-intake/SKILL.md', text)
                self.assertIn('validate_pack.py', text)
        for engine in ('godot', 'phaser', 'unity', 'custom'):
            with self.subTest(engine=engine):
                self.assertIn('## Asset pack import', (ROOT / f'skills/engines/{engine}/SKILL.md').read_text())

    def test_copied_validator_runs_from_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as other:
            copy = Path(other) / 'validate_pack.py'
            shutil.copy(VALIDATOR, copy)
            proc = subprocess.run([sys.executable, str(copy), '--root', str(self.root)], capture_output=True, text=True, cwd=other)
            self.assertEqual(proc.returncode, 0, proc.stdout)


if __name__ == '__main__':
    unittest.main()
