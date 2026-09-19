"""Offline adapter regressions; synthetic bytes test integrity, not art or decoding."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACK = Path(__file__).resolve().parents[1] / 'skills/assets/open-asset-fixture'
SCRIPTS = PACK / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from asset_fixture import load_catalog
from prepare_assets import prepare


class ContextTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.request = self.write('request.json', {
            'kinds': ['vfx'], 'requires': ['particle-texture'],
            'formats': ['png'], 'query': 'smoke', 'limit': 3})
        (self.root / 'synthetic.png').write_bytes(b'synthetic-integrity-test-only')
        (self.root / 'license.txt').write_text('Synthetic license evidence for an offline contract test.')
        self.pin = self.write('pin.json', {
            'asset_id': 'kenney-smoke-particles',
            'acquired_from': 'https://example.invalid/synthetic-only',
            'files': ['synthetic.png'], 'license_file': 'license.txt',
            'properties': {'kinds': ['vfx'], 'capabilities': ['particle-texture'], 'formats': ['png']},
            'inspection_note': 'Synthetic contract-test bytes, NOT sourced art or decoding evidence.'})
        self.counter = 0

    def write(self, name, value):
        p = self.root / name
        p.write_text(json.dumps(value), encoding='utf-8')
        return p

    def run_cli(self, *args, expected=0, report=None, budget=4096):
        self.counter += 1
        report = report or self.root / f'report-{self.counter}.json'
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / 'asset_context.py'), '--report', str(report),
             '--max-output-bytes', str(budget), *map(str, args)],
            capture_output=True, timeout=20)
        self.assertEqual(result.returncode, expected, result.stderr.decode()[:800])
        self.assertLessEqual(len(result.stdout), budget)
        if expected == 1:
            self.assertEqual(result.stdout, b'')
            return result, report
        small = json.loads(result.stdout)
        raw = report.read_bytes()
        self.assertEqual(small['report_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(small['report_bytes'], len(raw))
        self.assertEqual(small['runtime_validation'], 'not-run')
        return small, json.loads(raw)

    def make_lock(self):
        p = self.root / 'fixture.lock.json'
        self.run_cli('pin', '--root', self.root, '--request', self.pin, report=p)
        return p

    def test_prepare_preserves_full_result(self):
        small, full = self.run_cli('prepare', '--skill', 'materials', 'audio-feel', 'juice-vfx')
        expected = prepare(load_catalog(PACK / 'assets/catalog.json'), ['materials', 'audio-feel', 'juice-vfx'])
        self.assertEqual(full, expected)
        self.assertEqual(small['status'], 'needs-acquisition')
        self.assertEqual(small['total_skills'], 3)

    def test_unknown_profile_stays_blocked(self):
        small, full = self.run_cli('prepare', '--skill', 'new-unprofiled-test', expected=2)
        self.assertEqual(small['status'], 'blocked')
        self.assertEqual(full['skills'][0]['status'], 'needs-requirements')

    def test_synthetic_logic_needs_no_art(self):
        small, _ = self.run_cli('prepare', '--skill', 'rng-seed')
        self.assertEqual(small['status'], 'not-needed')

    def test_pinned_only_absent_input_blocks(self):
        small, _ = self.run_cli('prepare', '--skill', 'juice-vfx', '--root', self.root,
                                '--pinned-only', expected=2)
        self.assertEqual(small['status'], 'blocked')

    def test_match_hard_format_not_relaxed(self):
        small, full = self.run_cli('match', '--request', self.request, expected=2)
        self.assertEqual(small['status'], 'unmatched')
        self.assertTrue(full['rejected'])

    def test_ccby_requires_explicit_opt_in(self):
        req = {'kinds': ['ui'], 'requires': ['vector-icon'], 'formats': ['svg']}
        p = self.write('icon.json', req)
        self.run_cli('match', '--request', p, expected=2)
        req['allow_attribution'] = True
        self.write('icon.json', req)
        small, full = self.run_cli('match', '--request', p)
        self.assertEqual(small['choices'][0]['license'], 'CC-BY-3.0')
        self.assertTrue(full['matches'][0]['attribution_required'])

    def test_pin_report_is_original_lock_schema(self):
        small, full = self.run_cli('pin', '--root', self.root, '--request', self.pin)
        self.assertEqual(small['status'], 'lock-created')
        self.assertNotIn('report_sha256', full)
        self.assertEqual(full['files'][0]['path'], 'synthetic.png')

    def test_verify_and_offline_reuse(self):
        lock = self.make_lock()
        small, _ = self.run_cli('verify', '--root', self.root, '--lock', lock)
        self.assertEqual(small['status'], 'integrity-verified')
        small, full = self.run_cli('select', '--root', self.root, '--locks', lock,
                                  '--request', self.request, '--pinned-only')
        self.assertEqual(small['choices'][0]['status'], 'local-integrity-verified')
        self.assertEqual(full['mode'], 'pinned-only')

    def test_local_first_not_replaced_by_catalog(self):
        lock = self.make_lock()
        req = self.write('wide.json', {'kinds': ['vfx'], 'requires': ['particle-texture']})
        small, full = self.run_cli('select', '--root', self.root, '--locks', lock, '--request', req)
        self.assertEqual(full['matches'][0]['status'], 'local-integrity-verified')
        self.assertEqual(small['choices'][0]['id'], 'kenney-smoke-particles')

    def test_tampering_is_visible_and_blocked(self):
        lock = self.make_lock()
        (self.root / 'synthetic.png').write_bytes(b'changed')
        small, full = self.run_cli('select', '--root', self.root, '--locks', lock,
                                  '--request', self.request, '--pinned-only', expected=2)
        self.assertEqual(small['invalid_lock_occurrences'], 1)
        self.assertEqual(len(full['invalid_locks']), 1)

    def test_missing_license_blocks(self):
        lock = self.make_lock()
        (self.root / 'license.txt').unlink()
        small, _ = self.run_cli('select', '--root', self.root, '--locks', lock,
                               '--request', self.request, '--pinned-only', expected=2)
        self.assertEqual(small['invalid_lock_occurrences'], 1)

    def test_fabricated_runtime_pass_is_rejected(self):
        lock = self.make_lock()
        data = json.loads(lock.read_text()); data['runtime_validation'] = 'passed'
        self.write(lock.name, data)
        self.run_cli('verify', '--root', self.root, '--lock', lock, expected=1)

    def test_existing_report_never_overwritten(self):
        report = self.root / 'existing.json'; report.write_text('keep')
        self.run_cli('prepare', '--skill', 'rng-seed', report=report, expected=1)
        self.assertEqual(report.read_text(), 'keep')

    def test_duplicate_request_keys_rejected(self):
        self.request.write_text('{"kinds":["model"],"kinds":["vfx"]}')
        self.run_cli('match', '--request', self.request, expected=1)

    def test_missing_request_does_not_create_report(self):
        report = self.root / 'should-not-exist.json'
        self.run_cli('match', '--request', self.root / 'missing.json', report=report, expected=1)
        self.assertFalse(report.exists())

    def test_minimum_budget_remains_json(self):
        small, full = self.run_cli('prepare', '--skill', 'materials', 'audio-feel', 'juice-vfx', budget=1024)
        self.assertEqual(small['status'], full['status'])

    def test_many_skills_not_dropped_from_denominator(self):
        names = [f'unknown-{i}' for i in range(120)]
        small, full = self.run_cli('prepare', '--skill', *names, expected=2, budget=1024)
        self.assertEqual(small['total_skills'], 120)
        self.assertEqual(small['summary']['needs-requirements'], 120)
        self.assertEqual(len(full['skills']), 120)

    def test_local_missing_capability_is_not_relaxed(self):
        lock = self.make_lock()
        req = self.write('rig.json', {'kinds': ['vfx'], 'requires': ['skeletal-animation'], 'formats': ['png']})
        small, _ = self.run_cli('select', '--root', self.root, '--locks', lock,
                               '--request', req, '--pinned-only', expected=2)
        self.assertEqual(small['status'], 'unmatched')

    def test_ambiguous_mixed_format_not_reused(self):
        pin = json.loads(self.pin.read_text())
        (self.root / 'synthetic.glb').write_bytes(b'synthetic-glb-contract-test-only')
        pin['files'].append('synthetic.glb'); pin['properties']['formats'].append('glb')
        self.write(self.pin.name, pin)
        lock = self.make_lock()
        self.run_cli('select', '--root', self.root, '--locks', lock,
                     '--request', self.request, '--pinned-only', expected=2)

    def test_explicit_capability_format_binding_reuses_only_bound_format(self):
        pin = json.loads(self.pin.read_text())
        (self.root / 'synthetic.glb').write_bytes(b'synthetic-glb-contract-test-only')
        pin['files'].append('synthetic.glb'); pin['properties']['formats'].append('glb')
        pin['properties']['capability_formats'] = {'particle-texture': ['png']}
        self.write(self.pin.name, pin); lock = self.make_lock()
        self.run_cli('select', '--root', self.root, '--locks', lock,
                     '--request', self.request, '--pinned-only')
        req = json.loads(self.request.read_text()); req['formats'] = ['glb']
        self.write(self.request.name, req)
        self.run_cli('select', '--root', self.root, '--locks', lock,
                     '--request', self.request, '--pinned-only', expected=2)

    def test_pin_traversal_is_rejected(self):
        pin = json.loads(self.pin.read_text()); pin['files'] = ['../outside.png']
        self.write(self.pin.name, pin)
        self.run_cli('pin', '--root', self.root, '--request', self.pin, expected=1)

    def test_pin_executable_is_rejected(self):
        pin = json.loads(self.pin.read_text()); pin['files'].append('unsafe.py')
        (self.root / 'unsafe.py').write_text('raise RuntimeError("must not execute")')
        self.write(self.pin.name, pin)
        self.run_cli('pin', '--root', self.root, '--request', self.pin, expected=1)

    def test_pin_symlink_is_rejected(self):
        (self.root / 'link.png').symlink_to(self.root / 'synthetic.png')
        pin = json.loads(self.pin.read_text()); pin['files'] = ['link.png']
        self.write(self.pin.name, pin)
        self.run_cli('pin', '--root', self.root, '--request', self.pin, expected=1)

    def test_report_symlink_is_not_followed(self):
        target = self.root / 'target.json'; target.write_text('keep')
        output = self.root / 'linked.json'; output.symlink_to(target)
        self.run_cli('prepare', '--skill', 'rng-seed', report=output, expected=1)
        self.assertEqual(target.read_text(), 'keep')

    def test_all_skills_file(self):
        p = self.write('skills.json', [{'name': 'rng-seed'}, {'name': 'materials'}])
        small, full = self.run_cli('prepare', '--all-skills', p)
        self.assertEqual(small['total_skills'], 2)
        self.assertEqual(full['skills'][0]['status'], 'not-needed')

    def test_non_array_all_skills_is_rejected(self):
        p = self.write('skills.json', {'name': 'rng-seed'})
        self.run_cli('prepare', '--all-skills', p, expected=1)

    def tree(self, rows=None, truncated=False):
        return self.write('tree.json', {'sha': 'a' * 40, 'truncated': truncated, 'tree': rows or [
            {'path': 'Assets/gltf/floor.glb', 'type': 'blob', 'mode': '100644', 'size': 100, 'sha': 'b' * 40},
            {'path': 'Assets/gltf/wall.glb', 'type': 'blob', 'mode': '100644', 'size': 200, 'sha': 'c' * 40},
            {'path': 'Assets/fbx/wall.fbx', 'type': 'blob', 'mode': '100644', 'size': 300, 'sha': 'd' * 40},
            {'path': 'Assets/gltf-backup/wall.glb', 'type': 'blob', 'mode': '100644', 'size': 400, 'sha': 'e' * 40}]})

    def test_inventory_prefix_is_component_boundary(self):
        small, full = self.run_cli('inventory', '--input', self.tree(), '--prefix', 'Assets/gltf')
        self.assertEqual(full['matched_count'], 2)
        self.assertEqual(small['status'], 'candidates-only')
        self.assertNotIn('ready-for-import', str(small))

    def test_inventory_patterns_and_formats_are_explicit(self):
        _, full = self.run_cli('inventory', '--input', self.tree(), '--prefix', 'Assets',
                               '--pattern', '*wall*', '--formats', 'fbx')
        self.assertEqual([r['path'] for r in full['matches']], ['Assets/fbx/wall.fbx'])

    def test_inventory_truncated_is_blocked_even_with_candidates(self):
        small, full = self.run_cli('inventory', '--input', self.tree(truncated=True),
                                  '--prefix', 'Assets/gltf', expected=2)
        self.assertEqual(small['status'], 'blocked')
        self.assertTrue(full['source_truncated'])

    def test_inventory_requires_scope(self):
        self.run_cli('inventory', '--input', self.tree(), expected=1)

    def test_inventory_no_match_not_success(self):
        small, _ = self.run_cli('inventory', '--input', self.tree(), '--prefix', 'Absent', expected=2)
        self.assertEqual(small['status'], 'unmatched')

    def test_inventory_does_not_echo_content_or_urls(self):
        p = self.tree(); data = json.loads(p.read_text())
        data['tree'][0]['content'] = 'BASE64_SECRET' * 100
        data['tree'][0]['url'] = 'https://example.invalid/?token=SECRET'
        self.write(p.name, data)
        small, full = self.run_cli('inventory', '--input', p, '--prefix', 'Assets/gltf')
        self.assertNotIn('SECRET', str(small) + str(full))

    def test_inventory_excludes_symlink_and_executable(self):
        p = self.tree(); data = json.loads(p.read_text())
        data['tree'][0]['mode'] = '120000'; data['tree'][1]['mode'] = '100755'
        self.write(p.name, data)
        _, full = self.run_cli('inventory', '--input', p, '--prefix', 'Assets/gltf', expected=2)
        self.assertEqual(full['excluded_entries'], 2)

    def test_inventory_invalid_path_is_rejected(self):
        p = self.tree(); data = json.loads(p.read_text()); data['tree'][0]['path'] = '../evil.glb'
        self.write(p.name, data)
        self.run_cli('inventory', '--input', p, '--prefix', 'Assets', expected=1)

    def test_inventory_duplicate_path_is_rejected(self):
        p = self.tree(); data = json.loads(p.read_text()); data['tree'].append(copy.deepcopy(data['tree'][0]))
        self.write(p.name, data)
        self.run_cli('inventory', '--input', p, '--prefix', 'Assets', expected=1)

    def test_inventory_limit_retains_counts(self):
        _, full = self.run_cli('inventory', '--input', self.tree(), '--prefix', 'Assets/gltf', '--limit', '1')
        self.assertEqual(full['matched_count'], 2)
        self.assertEqual(full['omitted_matches'], 1)

    def test_inventory_oversized_input_rejected(self):
        self.run_cli('inventory', '--input', self.tree(), '--prefix', 'Assets', '--max-input-bytes', '64', expected=1)

    def test_inventory_missing_truncation_flag_is_not_complete(self):
        p = self.tree(); data = json.loads(p.read_text()); del data['truncated']; self.write(p.name, data)
        self.run_cli('inventory', '--input', p, '--prefix', 'Assets', expected=1)

    def test_inventory_bad_sha_rejected(self):
        p = self.tree(); data = json.loads(p.read_text()); data['tree'][0]['sha'] = 'guess'
        self.write(p.name, data)
        self.run_cli('inventory', '--input', p, '--prefix', 'Assets', expected=1)


if __name__ == '__main__':
    unittest.main()
