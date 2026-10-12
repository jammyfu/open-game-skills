"""Synthetic regression tests, not engine or LLM evaluation evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent / 'behavior'
spec = importlib.util.spec_from_file_location('input_trust_acquire', HERE / 'acquire_inputs.py')
acquire = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acquire)


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class InputTrustTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        data = b'reviewed-synthetic-input'
        self.pin = {'path': 'fixture.bin', 'url': 'https://raw.githubusercontent.com/a/b/' + 'a'*40 + '/fixture.bin',
                    'max_bytes': 100, 'license': 'MIT', 'git_blob_sha': git_blob(data)}
        self.report = {'schema_version': 1, 'status': 'acquired-not-imported',
                       'spec_sha256': acquire.digest((HERE / 'inputs.json').read_bytes()),
                       'files': [{**self.pin, 'size': len(data), 'sha256': acquire.digest(data)}]}
        (self.root / 'fixture.bin').write_bytes(data)
        self.spec_patch = patch.object(acquire, 'read_spec', return_value={'files': [self.pin]})
        self.spec_patch.start()
        self.addCleanup(self.spec_patch.stop)
        self.save()

    def save(self):
        (self.root / 'acquisition.json').write_text(json.dumps(self.report))

    def test_reviewed_input_is_accepted(self):
        self.assertEqual(acquire.verify(self.root)['status'], 'acquired-not-imported')

    def test_rehashing_modified_bytes_cannot_repin_input(self):
        data = b'changed-synthetic-input'
        (self.root / 'fixture.bin').write_bytes(data)
        self.report['files'][0].update(size=len(data), sha256=acquire.digest(data), git_blob_sha=git_blob(data))
        self.save()
        with self.assertRaises(ValueError):
            acquire.verify(self.root)

    def test_acquisition_cannot_change_reviewed_url(self):
        self.report['files'][0]['url'] = 'https://example.com/unreviewed.bin'
        self.save()
        with self.assertRaises(ValueError):
            acquire.verify(self.root)

    def test_duplicate_rows_are_rejected(self):
        self.report['files'].append(dict(self.report['files'][0]))
        self.save()
        with self.assertRaises(ValueError):
            acquire.verify(self.root)

    def test_incorrect_acquisition_status_is_rejected(self):
        self.report['status'] = 'pass'
        self.save()
        with self.assertRaises(ValueError):
            acquire.verify(self.root)

    def test_missing_immutable_pin_is_rejected(self):
        del self.pin['git_blob_sha']
        with self.assertRaises(ValueError):
            acquire.verify(self.root)


if __name__ == '__main__':
    unittest.main()
