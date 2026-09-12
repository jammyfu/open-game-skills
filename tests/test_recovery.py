"""Repository contract regressions; these do not execute an LLM or game."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from tools.skill_quality import collect, check_catalog

ROOT = Path(__file__).resolve().parents[1]


class RecoveryTests(unittest.TestCase):
    def test_all_readmes_install_from_cloned_directory(self):
        for path in ROOT.glob('README*.md'):
            with self.subTest(locale=path.name):
                text = path.read_text(encoding='utf-8')
                self.assertIn('cd open-game-skills', text)
                self.assertIn('tools/install.py', text)
                self.assertNotIn('ln -sfn', text)

    def test_committed_catalog_covers_actual_skills(self):
        records, errors = collect(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(check_catalog(ROOT, records), [])

    def test_dispatcher_routes_name_each_skill_and_its_mode(self):
        text = (ROOT / 'skills/dispatcher/SKILL.md').read_text(encoding='utf-8')
        routes = re.findall(r'`([a-z0-9-]+) / ([a-z0-9-]+|n/a)`', text)
        self.assertGreaterEqual(len(routes), 40, 'routing needs explicit per-skill mode pairs')
        records, _ = collect(ROOT)
        paths = {r['name']: ROOT / 'skills' / r['path'] for r in records}
        for name, mode in routes:
            with self.subTest(skill=name, mode=mode):
                self.assertIn(name, paths)
                if mode not in {'select', 'existing', 'n/a'}:
                    body = paths[name].read_text(encoding='utf-8').split('---', 2)[2]
                    self.assertRegex(body, r'(?<![\w-])' + re.escape(mode) + r'(?![\w-])')

    def test_full_docs_are_checked_not_only_readmes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills').mkdir()
            (root / 'skills/SKILL.md').write_text('---\nname: open-game-skills\ndescription: Entry.\n---\n# Entry\n')
            (root / 'docs').mkdir()
            (root / 'docs/broken.md').write_text('[broken](absent.md)\n')
            run = subprocess.run([sys.executable, str(ROOT / 'tools/skill_quality.py'), '--root', str(root)], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0, 'a broken non-README reference was ignored')

    def test_catalog_can_bootstrap_with_an_entry_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills').mkdir()
            (root / 'skills/SKILL.md').write_text('---\nname: open-game-skills\ndescription: Entry.\n---\n# Entry\n[catalog](catalog.json)\n')
            run = subprocess.run([sys.executable, str(ROOT / 'tools/skill_quality.py'), '--root', str(root), '--write-catalog', '--check-catalog'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == '__main__':
    unittest.main()
