from pathlib import Path
import tempfile
import unittest
from tools.install import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skills test ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'repo' / 'skills'
        (self.source / 'dispatcher').mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('entry')
        (self.source / 'dispatcher' / 'SKILL.md').write_text('dispatcher')
        self.target = self.root / 'agent skills'

    def test_creates_parents_and_absolute_link(self):
        path = install(self.source, self.target)
        self.assertTrue(path.is_symlink())
        self.assertEqual(path.resolve(), self.source.resolve())

    def test_same_link_is_idempotent(self):
        first = install(self.source, self.target)
        self.assertEqual(install(self.source, self.target), first)

    def test_refuses_existing_file(self):
        self.target.mkdir()
        dest = self.target / 'open-game-skills'
        dest.write_text('keep')
        with self.assertRaises(FileExistsError):
            install(self.source, self.target)
        self.assertEqual(dest.read_text(), 'keep')

    def test_refuses_existing_directory_and_broken_link(self):
        self.target.mkdir()
        dest = self.target / 'open-game-skills'
        dest.mkdir()
        with self.assertRaises(FileExistsError):
            install(self.source, self.target)
        dest.rmdir(); dest.symlink_to(self.root / 'absent')
        with self.assertRaises(FileExistsError):
            install(self.source, self.target)

    def test_dry_run_does_not_write(self):
        path = install(self.source, self.target, dry_run=True)
        self.assertFalse(path.exists())
        self.assertFalse(self.target.exists())

    def test_missing_source_fails(self):
        with self.assertRaises(FileNotFoundError):
            install(self.root / 'absent', self.target)

    def test_no_recursive_destination(self):
        with self.assertRaises(ValueError):
            install(self.source, self.source / 'nested', copy=True)

    def test_copy_is_independent_and_does_not_overwrite(self):
        dest = install(self.source, self.target, copy=True)
        self.assertFalse(dest.is_symlink())
        (self.source / 'SKILL.md').write_text('new')
        self.assertEqual((dest / 'SKILL.md').read_text(), 'entry')
        with self.assertRaises(FileExistsError):
            install(self.source, self.target, copy=True)


if __name__ == '__main__':
    unittest.main()
