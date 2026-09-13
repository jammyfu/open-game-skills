"""Pack registration and executable fixture preparation; no model or engine claims."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'skills/assets/open-asset-fixture'
SCRIPT = PACK / 'scripts/prepare_assets.py'


class OpenAssetRegistrationTests(unittest.TestCase):
    def test_skill_registered_in_catalog_coverage_and_review_cases(self):
        self.assertTrue((PACK / 'SKILL.md').is_file(), 'asset scripts have no registered SKILL.md entry')
        catalog = json.loads((ROOT / 'skills/catalog.json').read_text())
        self.assertIn({'name': 'open-asset-fixture', 'path': 'assets/open-asset-fixture/SKILL.md'}, catalog)
        coverage = json.loads((ROOT / 'tests/skills/coverage.json').read_text())
        self.assertIn('open-asset-fixture', coverage['skills'])
        case = json.loads((ROOT / 'tests/skills/cases/assets/open-asset-fixture.json').read_text())
        self.assertEqual(case['review_state'], 'reviewed')
        self.assertEqual([s['kind'] for s in case['scenarios']], ['normal', 'boundary', 'adversarial'])

    def test_dispatcher_and_gameplay_preparation_expose_fixture_owner(self):
        dispatcher = (ROOT / 'skills/dispatcher/SKILL.md').read_text()
        self.assertIn('open-asset-fixture / library-first', dispatcher)
        for path in ['skills/disciplines/gameplay-harness/SKILL.md',
                     'skills/disciplines/gameplay-validation/SKILL.md']:
            with self.subTest(path=path):
                self.assertIn('open-asset-fixture', (ROOT / path).read_text())

    def test_readme_locales_expose_skill_sources_and_executable_preparation(self):
        for path in ROOT.glob('README*.md'):
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn('](skills/assets/open-asset-fixture/SKILL.md)', text)
                self.assertIn('](skills/assets/open-asset-fixture/reference/sources.md)', text)
                self.assertIn('scripts/prepare_assets.py', text)
                self.assertIn('--pinned-only', text)

    def test_source_catalog_includes_kaykit_and_version_scoped_effect_data(self):
        catalog = json.loads((PACK / 'assets/catalog.json').read_text())
        assets = {a['id']: a for a in catalog['assets']}
        self.assertIn('kaykit-dungeon-free', assets)
        self.assertEqual(assets['kaykit-dungeon-free']['license'], 'CC0-1.0')
        self.assertEqual(assets['kaykit-dungeon-free']['edition'], 'FREE')
        self.assertIn('effekseer-effect-materials', assets)
        self.assertIn('1.7', assets['effekseer-effect-materials']['inspection'])
        skill_names = {a['name'] for a in json.loads((ROOT / 'skills/catalog.json').read_text())}
        self.assertFalse(set(catalog['skill_profiles']) - skill_names)
        self.assertFalse(set(catalog['no_asset_skills']) - skill_names)


class AssetPreparationTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'missing executable asset preparation entry')
        sys.path.insert(0, str(SCRIPT.parent))
        self.addCleanup(sys.path.pop, 0)
        spec = importlib.util.spec_from_file_location('asset_preparation', SCRIPT)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')
        self.tmp = tempfile.TemporaryDirectory(prefix='asset preparation ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_logic_tests_need_no_art_and_unknown_skills_need_requirements(self):
        report = self.m.prepare(self.catalog, ['rng-seed', 'unknown-skill'])
        self.assertEqual([r['status'] for r in report['skills']], ['not-needed', 'needs-requirements'])
        self.assertEqual(report['status'], 'blocked')
        self.assertEqual(report['runtime_validation'], 'not-run')

    def test_discovery_plan_is_not_fixture_readiness(self):
        report = self.m.prepare(self.catalog, ['materials'])
        self.assertEqual(report['status'], 'needs-acquisition')
        self.assertEqual({r['role'] for r in report['skills'][0]['roles']}, {'surface', 'lighting'})
        self.assertEqual(report['summary']['needs-acquisition'], 1)
        self.assertEqual(report['decoding_validation'], 'not-run')

    def test_pinned_only_cannot_fall_back_to_remote_candidates(self):
        report = self.m.prepare(self.catalog, ['materials'], root=self.root, pinned_only=True)
        self.assertEqual(report['status'], 'blocked')
        self.assertTrue(all(r['selection']['status'] == 'unmatched' for r in report['skills'][0]['roles']))

    def test_verified_local_lease_is_reused_without_network_and_tampering_blocks(self):
        from fixture_lock import make_lock, write_lock
        (self.root / 'particle.png').write_bytes(b'Synthetic hash fixture, NOT a decoded image')
        (self.root / 'LICENSE.txt').write_text('Synthetic license evidence for tool testing only')
        request = {'asset_id': 'kenney-smoke-particles', 'acquired_from': 'https://kenney.nl/assets/smoke-particles',
                   'files': ['particle.png'], 'license_file': 'LICENSE.txt',
                   'properties': {'kinds': ['vfx'], 'capabilities': ['particle-texture'], 'formats': ['png']},
                   'inspection_note': 'Synthetic bytes used only to test preparation and integrity.'}
        lock = self.root / 'fixture.lock.json'
        write_lock(lock, make_lock(self.catalog, self.root, request))
        report = self.m.prepare(self.catalog, ['juice-vfx'], root=self.root, locks=[lock], pinned_only=True)
        self.assertEqual(report['status'], 'ready-for-import')
        self.assertEqual(report['runtime_validation'], 'not-run')
        (self.root / 'particle.png').write_bytes(b'changed')
        report = self.m.prepare(self.catalog, ['juice-vfx'], root=self.root, locks=[lock], pinned_only=True)
        self.assertEqual(report['status'], 'blocked')
        self.assertTrue(report['skills'][0]['roles'][0]['selection']['invalid_locks'])

    def test_all_inventory_members_remain_in_report_denominator(self):
        names = [a['name'] for a in json.loads((ROOT / 'skills/catalog.json').read_text())]
        report = self.m.prepare(self.catalog, names)
        self.assertEqual(report['total_skills'], len(names))
        self.assertEqual(sum(report['summary'].values()), len(names))
        self.assertEqual({r['skill'] for r in report['skills']}, set(names))

    def test_empty_duplicate_or_malformed_skill_requests_fail(self):
        for skills in [[], ['materials', 'materials'], [''], ['../materials'], 'materials']:
            with self.subTest(skills=skills), self.assertRaises(ValueError):
                self.m.prepare(self.catalog, skills)
        with self.assertRaises(ValueError):
            self.m.prepare(self.catalog, ['materials'], locks=[self.root / 'a.json'])

    def test_copied_pack_runs_from_unrelated_directory_without_repo_imports(self):
        copied = self.root / 'copy'
        shutil.copytree(PACK, copied, ignore=shutil.ignore_patterns('__pycache__'))
        command = [sys.executable, str(copied / 'scripts/prepare_assets.py'), '--skill', 'materials']
        r = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)['status'], 'needs-acquisition')
        r = subprocess.run(command + ['--pinned-only'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, r.stderr)

    def test_cli_inventory_output_is_exclusive_and_does_not_rewrite_existing_results(self):
        output = self.root / 'plan.json'
        command = [sys.executable, str(SCRIPT), '--all-skills', str(ROOT / 'skills/catalog.json'), '--output', str(output)]
        r = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, r.stderr)  # unknown profiles remain blocked
        before = output.read_bytes()
        r = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(output.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
