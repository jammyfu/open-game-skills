"""Offline tests for acquiring the bounded, pinned behavior-runtime inputs."""
import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tests/behavior/acquire_inputs.py'

class BehaviorInputTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.is_file(), 'A reproducible pinned-input acquisition entry is required')
        spec = importlib.util.spec_from_file_location('behavior_acquire', SCRIPT)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod

    def test_source_urls_are_pinned_and_bounded(self):
        mod = self.load()
        data = mod.read_spec()
        self.assertGreaterEqual(len(data['files']), 2)
        for row in data['files']:
            mod.validate_entry(row)
        self.assertLessEqual(len(data['files']), 10)

    def test_unpinned_or_external_input_is_rejected(self):
        mod = self.load()
        base = mod.read_spec()['files'][0]
        for url in ['https://raw.githubusercontent.com/a/b/main/model.glb', 'https://example.com/model.glb']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                mod.validate_entry(dict(base, url=url))

    def test_paths_cannot_escape_fixture_directory(self):
        mod = self.load(); base = mod.read_spec()['files'][0]
        for path in ['../outside', '/tmp/outside', 'a/../../outside', 'a\\outside']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                mod.validate_entry(dict(base, path=path))

    def test_hash_check_uses_bytes_not_existence(self):
        mod = self.load()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); p = root/'sample.bin'; p.write_bytes(b'synthetic-bytes')
            row = {'path': 'sample.bin', 'size': p.stat().st_size, 'sha256': mod.digest(p.read_bytes())}
            mod.verify_file(root, row)
            p.write_bytes(b'changed-fixture')
            with self.assertRaises(ValueError): mod.verify_file(root,row)

if __name__ == '__main__': unittest.main()
