"""P0 CLI/unit paths for the executable skill scripts; offline, no LLM or engine."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / 'skills/disciplines/scene-assembly/scripts/scene_preflight.py'
TRACE = ROOT / 'skills/disciplines/gameplay-harness/scripts/trace_compare.py'
PACK = ROOT / 'skills/assets/open-asset-fixture'
ASSET = PACK / 'scripts/asset_fixture.py'
LOCK = PACK / 'scripts/fixture_lock.py'
PREPARE = PACK / 'scripts/prepare_assets.py'
BOOM = ROOT / 'skills/disciplines/camera-shots/scripts/boom_sweep.py'
EXAMPLE = ROOT / 'skills/disciplines/camera-shots/assets/boom-sweep.example.json'


def cli(path, *args, cwd=None):
    return subprocess.run([sys.executable, str(path), *map(str, args)],
                          capture_output=True, text=True, timeout=8, cwd=cwd)


def load(path, name=None):
    spec = importlib.util.spec_from_file_location(name or path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def boom_plan():
    return {
        'schema_version': 1,
        'sweep_id': 'intro-boom-v1',
        'units': 'm',
        'basis': 'right-handed-y-up',
        'angle_units': 'deg',
        'owner': 'cinematic-intro',
        'camera_collision_required': True,
        'anchor': {'id': 'hero-chest', 'position': [0, 1.4, 0]},
        'look_target': {'id': 'hero-face', 'position': [0, 1.6, 0.15]},
        'gameplay_lock_target': {'id': 'enemy-lock'},
        'boom': {
            'length_start': 4, 'length_end': 5.5,
            'elevation_start': 12, 'elevation_end': 28,
            'azimuth_start': -30, 'azimuth_sweep': 70,
        },
        'sample_count': 8,
    }


class AssetFixtureP0Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(ASSET.is_file(), 'missing asset_fixture.py')
        self.m = load(ASSET)
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')

    def test_cli_match_happy_and_unmatched_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            request = Path(tmp) / 'request.json'
            request.write_text(json.dumps({'kinds': ['vfx'], 'query': 'smoke'}))
            result = cli(ASSET, 'match', '--request', request, cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'matched')
            self.assertEqual(report['runtime_validation'], 'not-run')
            self.assertTrue(report['matches'])
            request.write_text(json.dumps({'kinds': ['model'], 'requires': ['impossible-rig']}))
            result = cli(ASSET, 'match', '--request', request, cwd=tmp)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'unmatched')

    def test_cli_plan_not_needed_and_needs_requirements(self):
        result = cli(ASSET, 'plan', '--skill', 'rng-seed')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'not-needed')
        result = cli(ASSET, 'plan', '--skill', 'unknown-skill')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'needs-requirements')

    def test_cli_invalid_catalog_request_and_missing_file_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            request = Path(tmp) / 'request.json'
            request.write_text(json.dumps({'kinds': ['vfx']}))
            missing = cli(ASSET, 'match', '--request', Path(tmp) / 'absent.json', cwd=tmp)
            self.assertEqual(missing.returncode, 1)
            self.assertIn('Asset selection failed', missing.stderr)
            request.write_text('{')
            self.assertEqual(cli(ASSET, 'match', '--request', request, cwd=tmp).returncode, 1)
            request.write_text(json.dumps({'kinds': ['model'], 'formats': ['.png']}))
            self.assertEqual(cli(ASSET, 'match', '--request', request, cwd=tmp).returncode, 1)
            catalog = Path(tmp) / 'catalog.json'
            catalog.write_text('{"schema_version":1,"revision":"x","assets":[]}')
            request.write_text(json.dumps({'kinds': ['vfx']}))
            result = cli(ASSET, '--catalog', catalog, 'match', '--request', request, cwd=tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn('Asset selection failed', result.stderr)

    def test_https_credentials_long_query_and_catalog_policy_rejected(self):
        catalog = deepcopy(self.catalog)
        catalog['assets'][0]['source_url'] = 'https://user:pass@example.com/pack'
        with self.assertRaises(ValueError):
            self.m.validate_catalog(catalog)
        catalog = deepcopy(self.catalog)
        catalog['assets'][0]['checked_on'] = '13-09-2026'
        with self.assertRaises(ValueError):
            self.m.validate_catalog(catalog)
        catalog = deepcopy(self.catalog)
        catalog['no_asset_skills'] = list(catalog.get('no_asset_skills', [])) + ['materials']
        with self.assertRaises(ValueError):
            self.m.validate_catalog(catalog)
        with self.assertRaises(ValueError):
            self.m.match_assets(self.catalog, {'kinds': ['vfx'], 'query': 'x' * 2001})
        with self.assertRaises(ValueError):
            self.m.match_assets(self.catalog, {'kinds': ['vfx'], 'formats': ['.png']})
        with self.assertRaises(ValueError):
            self.m.plan_for_skill(self.catalog, 'rng-seed', allow_attribution='true')


class FixtureLockP0Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(LOCK.is_file(), 'missing fixture_lock.py')
        sys.path.insert(0, str(LOCK.parent))
        self.addCleanup(sys.path.pop, 0)
        self.m = load(LOCK, 'fixture_lock_p0')
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'sample.png').write_bytes(b'synthetic fixture bytes - not a real image')
        (self.root / 'LICENSE.txt').write_text('Synthetic evidence for a P0 integrity test.')
        self.request = {
            'asset_id': 'kenney-smoke-particles',
            'acquired_from': 'https://kenney.nl/assets/smoke-particles',
            'files': ['sample.png'],
            'license_file': 'LICENSE.txt',
            'properties': {'kinds': ['vfx'], 'capabilities': ['particle-texture'], 'formats': ['png']},
            'inspection_note': 'Synthetic P0 hash-unit-test input only; no decode/engine test.',
        }
        self.request_path = self.root / 'pin.json'
        self.request_path.write_text(json.dumps(self.request))

    def test_cli_pin_verify_select_happy_and_blocked_paths(self):
        lock_path = self.root / 'fixture.lock.json'
        pin = cli(LOCK, '--root', self.root, 'pin', '--request', self.request_path, '--output', lock_path)
        self.assertEqual(pin.returncode, 0, pin.stderr)
        lock = json.loads(lock_path.read_text())
        self.assertEqual(len(lock['files'][0]['sha256']), 64)
        self.assertEqual(len(lock['license_evidence']['sha256']), 64)
        self.assertEqual(lock['runtime_validation'], 'not-run')
        before = lock_path.read_bytes()
        again = cli(LOCK, '--root', self.root, 'pin', '--request', self.request_path, '--output', lock_path)
        self.assertEqual(again.returncode, 1, again.stderr)
        self.assertEqual(lock_path.read_bytes(), before)
        verify = cli(LOCK, '--root', self.root, 'verify', '--lock', lock_path)
        self.assertEqual(verify.returncode, 0, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)['status'], 'integrity-verified')
        select_req = self.root / 'select.json'
        select_req.write_text(json.dumps({'kinds': ['vfx'], 'requires': ['particle-texture']}))
        selected = cli(LOCK, '--root', self.root, 'select', '--request', select_req, '--locks', lock_path)
        self.assertEqual(selected.returncode, 0, selected.stderr)
        report = json.loads(selected.stdout)
        self.assertEqual(report['status'], 'matched')
        self.assertEqual(report['matches'][0]['status'], 'local-integrity-verified')
        (self.root / 'sample.png').write_bytes(b'tampered fixture bytes')
        tampered = cli(LOCK, '--root', self.root, 'verify', '--lock', lock_path)
        self.assertEqual(tampered.returncode, 1)
        self.assertIn('Fixture operation failed', tampered.stderr)

    def test_cli_select_pinned_only_unmatched_and_invalid_input_exit_codes(self):
        select_req = self.root / 'select.json'
        select_req.write_text(json.dumps({'kinds': ['vfx'], 'requires': ['particle-texture']}))
        result = cli(LOCK, '--root', self.root, 'select', '--request', select_req, '--pinned-only')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'unmatched')
        missing = cli(LOCK, '--root', self.root, 'pin', '--request', self.root / 'absent.json',
                      '--output', self.root / 'out.lock.json')
        self.assertEqual(missing.returncode, 1)
        result = cli(LOCK, '--root', self.root / 'missing-root', 'verify', '--lock', self.root / 'absent.json')
        self.assertEqual(result.returncode, 1)

    def test_pin_rejects_credentials_license_mix_and_unknown_or_paid_assets(self):
        for acquired in ['http://kenney.nl/assets/smoke-particles',
                         'https://user:pass@kenney.nl/assets/smoke-particles']:
            req = deepcopy(self.request); req['acquired_from'] = acquired
            with self.subTest(acquired=acquired), self.assertRaises(ValueError):
                self.m.make_lock(self.catalog, self.root, req)
        req = deepcopy(self.request); req['files'] = ['sample.png', 'LICENSE.txt']
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, req)
        req = deepcopy(self.request); req['inspection_note'] = '   '
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, req)
        req = deepcopy(self.request); req['asset_id'] = 'not-a-real-asset'
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, req)
        catalog = deepcopy(self.catalog)
        next(a for a in catalog['assets'] if a['id'] == 'kenney-smoke-particles')['cost'] = 'paid'
        with self.assertRaises(ValueError):
            self.m.make_lock(catalog, self.root, self.request)
        (self.root / 'LICENSE.png').write_bytes(b'not-evidence')
        req = deepcopy(self.request); req['license_file'] = 'LICENSE.png'
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, req)
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, self.request, max_bytes=0)

    def test_nested_relative_file_pins_and_double_slash_is_rejected(self):
        nested = self.root / 'props'
        nested.mkdir()
        (nested / 'sample.png').write_bytes(b'nested synthetic fixture bytes')
        req = deepcopy(self.request); req['files'] = ['props/sample.png']
        lock = self.m.make_lock(self.catalog, self.root, req)
        self.assertEqual(lock['files'][0]['path'], 'props/sample.png')
        self.assertEqual(self.m.verify_lock(self.catalog, self.root, lock)['status'], 'integrity-verified')
        req['files'] = ['props//sample.png']
        with self.assertRaises(ValueError):
            self.m.make_lock(self.catalog, self.root, req)

    def test_select_records_oversized_lock_without_reusing_it(self):
        huge = self.root / 'huge.lock.json'
        huge.write_bytes(b'x' * (1024 * 1024 + 1))
        result = self.m.select_assets(self.catalog, self.root, [huge],
                                      {'kinds': ['vfx'], 'requires': ['particle-texture']},
                                      pinned_only=True)
        self.assertEqual(result['status'], 'unmatched')
        self.assertTrue(result['invalid_locks'])
        self.assertIn('oversized lock', result['invalid_locks'][0]['reason'])


class PrepareAssetsP0Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PREPARE.is_file(), 'missing prepare_assets.py')
        sys.path.insert(0, str(PREPARE.parent))
        self.addCleanup(sys.path.pop, 0)
        self.m = load(PREPARE, 'prepare_assets_p0')
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')

    def test_cli_not_needed_happy_and_invalid_skill_exit_codes(self):
        result = cli(PREPARE, '--skill', 'rng-seed')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'not-needed')
        self.assertEqual(report['runtime_validation'], 'not-run')
        result = cli(PREPARE, '--skill', 'Materials')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Asset preparation failed', result.stderr)
        result = cli(PREPARE, '--skill', 'unknown-skill')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'blocked')

    def test_cli_malformed_inventory_missing_catalog_and_locks_without_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / 'skills.json'
            inventory.write_text(json.dumps({'name': 'materials'}))
            result = cli(PREPARE, '--all-skills', inventory, cwd=tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn('Asset preparation failed', result.stderr)
            result = cli(PREPARE, '--catalog', Path(tmp) / 'absent.json', '--skill', 'rng-seed')
            self.assertEqual(result.returncode, 1)
            result = cli(PREPARE, '--skill', 'juice-vfx', '--locks', Path(tmp) / 'a.lock.json')
            self.assertEqual(result.returncode, 1)
            self.assertIn('fixture root', result.stderr)

    def test_cli_overwrite_refusal_keeps_existing_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'plan.json'
            out.write_text('keep-me')
            before = out.read_bytes()
            result = cli(PREPARE, '--skill', 'rng-seed', '--output', out, cwd=tmp)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(out.read_bytes(), before)

    def test_prepare_rejects_non_boolean_policy_flags(self):
        with self.assertRaises(ValueError):
            self.m.prepare(self.catalog, ['rng-seed'], pinned_only='true')
        with self.assertRaises(ValueError):
            self.m.prepare(self.catalog, ['rng-seed'], allow_attribution='false')


class SceneAndTraceCliContractTests(unittest.TestCase):
    """Keep a single-module happy/fail/blocked CLI contract for the two layout/trace tools."""

    def test_scene_preflight_pass_fail_and_blocked_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'layout.json'
            source.write_text((SCENE.parents[1] / 'assets/layout.example.json').read_text())
            result = cli(SCENE, source)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'pass')
            self.assertEqual(len(report['input_sha256']), 64)
            failing = json.loads(source.read_text())
            failing['portals'][0]['width'] = .7
            source.write_text(json.dumps(failing))
            result = cli(SCENE, source)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'fail')
            result = cli(SCENE, Path(tmp) / 'absent.json')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)['status'], 'blocked')

    def test_trace_compare_pass_fail_and_blocked_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            example = json.loads((TRACE.parents[1] / 'assets/trace.example.json').read_text())
            a = Path(tmp) / 'baseline.json'; b = Path(tmp) / 'candidate.json'
            a.write_text(json.dumps(example)); b.write_text(json.dumps(example))
            result = cli(TRACE, a, b)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'pass')
            candidate = deepcopy(example)
            candidate['frames'][0]['state'] = dict(candidate['frames'][0]['state'], hp=0)
            b.write_text(json.dumps(candidate))
            result = cli(TRACE, a, b)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'fail')
            candidate = deepcopy(example)
            candidate['context']['oracle'] = 'other-v1'
            b.write_text(json.dumps(candidate))
            result = cli(TRACE, a, b)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'blocked')


class BoomSweepP0Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(BOOM.is_file(), 'missing boom_sweep.py')
        self.m = load(BOOM)

    def report(self, data):
        return self.m.evaluate(data)

    def test_valid_plan_samples_presentation_only(self):
        result = self.report(boom_plan())
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['validation_mode'], 'static-boom-sweep-presentation')
        self.assertEqual(result['runtime_validation'], 'not-run')
        self.assertEqual(result['collision_validation'], 'not-run')
        self.assertEqual(result['comfort_validation'], 'not-run')
        self.assertEqual(result['pose_count'], 8)
        self.assertEqual(len(result['poses']), 8)
        self.assertEqual(result['poses'][0]['anti_clip_validation'], 'required')
        self.assertTrue(any('no world collision' in v for v in result['limits']))
        self.assertTrue(any('no gameplay targeting' in v for v in result['limits']))

    def test_known_boom_geometry_is_right_handed_y_up(self):
        data = boom_plan()
        data['anchor']['position'] = [0, 0, 0]
        data['look_target']['position'] = [0, 0, 0]
        data['boom'].update(length_start=2, length_end=2, elevation_start=0, elevation_end=0,
                            azimuth_start=0, azimuth_sweep=90)
        data['sample_count'] = 2
        poses = self.report(data)['poses']
        self.assertEqual(poses[0]['position'], [0.0, 0.0, 2.0])
        self.assertAlmostEqual(poses[1]['position'][0], 2.0)
        self.assertAlmostEqual(poses[1]['position'][1], 0.0)
        self.assertAlmostEqual(poses[1]['position'][2], 0.0)

    def test_look_target_defaults_to_anchor(self):
        data = boom_plan(); del data['look_target']
        result = self.report(data)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['poses'][0]['look'], [0, 1.4, 0])

    def test_zero_or_negative_boom_fails(self):
        for length in [0, -1]:
            data = boom_plan(); data['boom']['length_start'] = length
            with self.subTest(length=length):
                result = self.report(data)
                self.assertEqual(result['status'], 'fail')
                self.assertTrue(any(r['id'] == 'boom-length-positive' and r['status'] == 'fail' for r in result['checks']))

    def test_sample_count_and_angle_ranges_fail(self):
        cases = [
            ('sample_count', 1, 'sample-count-bounds'),
            ('sample_count', 65, 'sample-count-bounds'),
            ('elevation', 91, 'elevation-range'),
            ('azimuth', 400, 'azimuth-sweep-range'),
        ]
        for kind, value, check_id in cases:
            data = boom_plan()
            if kind == 'sample_count':
                data['sample_count'] = value
            elif kind == 'elevation':
                data['boom']['elevation_end'] = value
            else:
                data['boom']['azimuth_sweep'] = value
            with self.subTest(kind=kind, value=value):
                result = self.report(data)
                self.assertEqual(result['status'], 'fail')
                self.assertTrue(any(r['id'] == check_id and r['status'] == 'fail' for r in result['checks']))

    def test_shared_presentation_and_gameplay_identity_fails(self):
        for field in ['look_target', 'anchor']:
            data = boom_plan(); data['gameplay_lock_target']['id'] = data[field]['id']
            with self.subTest(field=field):
                result = self.report(data)
                self.assertEqual(result['status'], 'fail')
                self.assertTrue(any(r['id'] == 'presentation-gameplay-identity-distinct' and r['status'] == 'fail'
                                    for r in result['checks']))

    def test_camera_on_look_point_fails_separation(self):
        data = boom_plan()
        data['anchor']['position'] = [0, 0, 0]
        data['look_target']['position'] = [0, 2, 0]
        data['boom'].update(length_start=2, length_end=2, elevation_start=90, elevation_end=90,
                            azimuth_start=0, azimuth_sweep=0)
        data['sample_count'] = 2
        result = self.report(data)
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(r['id'] == 'look-separated-from-camera' and r['status'] == 'fail' for r in result['checks']))

    def test_offset_is_applied_and_still_not_collision_proof(self):
        data = boom_plan()
        data['offset_ref'] = {'id': 'shoulder', 'translation': [0, 0.25, 0]}
        data['boom'].update(length_start=2, length_end=2, elevation_start=0, elevation_end=0,
                            azimuth_start=0, azimuth_sweep=0)
        data['sample_count'] = 2
        data['anchor']['position'] = [0, 0, 0]
        result = self.report(data)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['collision_validation'], 'not-run')
        self.assertAlmostEqual(result['poses'][0]['position'][1], 0.25)

    def test_invalid_contracts_are_blocked_not_passed(self):
        bad = []
        for key, value in [('units', 'cm'), ('schema_version', True), ('angle_units', 'rad')]:
            data = boom_plan(); data[key] = value; bad.append(data)
        data = boom_plan(); data['boom']['length_start'] = True; bad.append(data)
        data = boom_plan(); data['sample_count'] = True; bad.append(data)
        data = boom_plan(); data['sample_count'] = 8.5; bad.append(data)
        data = boom_plan(); data['camera_collision_required'] = 1; bad.append(data)
        data = boom_plan(); data['mode'] = 'cinematic-crane'; bad.append(data)
        data = boom_plan(); data['runtime_validation'] = 'pass'; bad.append(data)
        data = boom_plan(); data['anchor']['position'][0] = float('nan'); bad.append(data)
        data = boom_plan(); data['fov_ref'] = {'comfort_profile_id': 'x', 'projection': 'vertical', 'degrees': 0}; bad.append(data)
        for i, data in enumerate(bad):
            with self.subTest(case=i):
                with self.assertRaises(ValueError):
                    self.report(data)

    def test_published_example_executes_in_declared_tool_scope(self):
        scene = json.loads(EXAMPLE.read_text())
        result = self.report(scene)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['runtime_validation'], 'not-run')
        self.assertEqual(result['collision_validation'], 'not-run')
        self.assertEqual(result['pose_count'], scene['sample_count'])

    def test_cli_exit_codes_hashes_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'plan.json'
            source.write_text(json.dumps(boom_plan()))
            out = Path(tmp) / 'report.json'
            passed = cli(BOOM, source, '--output', out)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            report = json.loads(out.read_text())
            before = out.read_bytes()
            self.assertEqual(report['status'], 'pass')
            self.assertEqual(len(report['input_sha256']), 64)
            self.assertEqual(len(report['tool_sha256']), 64)
            self.assertEqual(cli(BOOM, source, '--output', out).returncode, 2)
            self.assertEqual(out.read_bytes(), before)

            failing = Path(tmp) / 'fail.json'
            data = boom_plan(); data['boom']['length_end'] = 0
            failing.write_text(json.dumps(data))
            failed = cli(BOOM, failing)
            self.assertEqual(failed.returncode, 1, failed.stderr)
            self.assertEqual(json.loads(failed.stdout)['status'], 'fail')

            blocked = Path(tmp) / 'blocked.json'
            blocked.write_text('{"schema_version":1,"schema_version":1}')
            result = cli(BOOM, blocked)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)['status'], 'blocked')

    def test_duplicate_json_nonfinite_and_size_limits_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            for raw in ['{"schema_version":1,"schema_version":1}', '{"x": NaN}']:
                source.write_text(raw)
                with self.subTest(raw=raw):
                    self.assertEqual(cli(BOOM, source).returncode, 2)
            maximum = self.m.MAX_BYTES
            source.write_bytes(b' ' * (maximum + 1))
            result = cli(BOOM, source)
            self.assertEqual(result.returncode, 2)
            self.assertIn('limit', json.loads(result.stderr)['reason'])


if __name__ == '__main__':
    unittest.main()
