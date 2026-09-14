"""Historical experiment bytes stay frozen when production Skill guidance evolves."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'tests/behavior'
FROZEN = 'tests/behavior/experiments/asset-runtime-ab-v1/asset-runtime.skill-snapshot.txt'


def runner():
    spec = importlib.util.spec_from_file_location('snapshot_ab', HERE / 'ab_experiment.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


class HistoricalSkillTests(unittest.TestCase):
    def test_historical_treatment_uses_exact_preregistered_bytes(self):
        m = runner()
        archived = ROOT / FROZEN
        self.assertTrue(archived.is_file(), 'missing frozen historical Skill bytes')
        p = m.load_plan()
        self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), p['source_pins'][p['skill_path']])
        expected = (ROOT / p['task_path']).read_text() + m.SKILL_SEPARATOR + archived.read_text()
        self.assertEqual(m.payload(p, 'with-skill')['input'], expected)
        self.assertNotEqual(archived.read_bytes(), (ROOT / p['skill_path']).read_bytes())

    def isolate(self, root):
        p = json.loads((HERE / 'experiments/asset-runtime-ab-v1/plan.json').read_text())
        for rel in list(p['source_pins']) + [FROZEN]:
            src = ROOT / rel
            self.assertTrue(src.is_file(), 'missing archived Skill source')
            target = root / rel; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(src.read_bytes())
        return p

    def test_missing_or_corrupt_snapshot_cannot_accept_new_guidance(self):
        for mode in ['missing', 'corrupt', 'symlink']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); p = self.isolate(root); archive = root / FROZEN
                if mode == 'corrupt': archive.write_text('replacement guidance')
                else:
                    archive.unlink()
                    if mode == 'symlink': archive.symlink_to(root / p['skill_path'])
                m = runner()
                with patch.object(m, 'ROOT', root), self.assertRaises(ValueError): m.load_plan()

    def test_non_skill_input_drift_still_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); p = self.isolate(root)
            (root / p['fixed_simulation']).write_text('changed simulation')
            m = runner()
            with patch.object(m, 'ROOT', root), self.assertRaisesRegex(ValueError, 'simulation.mjs'): m.load_plan()

    def test_live_legacy_bytes_work_when_archive_is_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); p = self.isolate(root); archive = root / FROZEN
            (root / p['skill_path']).write_bytes(archive.read_bytes()); archive.unlink()
            m = runner()
            with patch.object(m, 'ROOT', root): self.assertEqual(m.load_plan()['experiment_id'], p['experiment_id'])

    def test_collection_records_storage_path_without_editing_preregistration(self):
        m = runner()
        self.assertTrue((ROOT / FROZEN).is_file(), 'missing archived Skill source')
        original = m.PLAN.read_bytes(); p = m.load_plan()
        with tempfile.TemporaryDirectory() as tmp:
            result = m.generate(p, Path(tmp) / 'run', execute=False)
            self.assertEqual(result['source_locations'][p['skill_path']], FROZEN)
            self.assertEqual(m.PLAN.read_bytes(), original)
            self.assertEqual(result['plan_sha256'], hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest())


if __name__ == '__main__': unittest.main()
