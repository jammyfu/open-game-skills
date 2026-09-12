"""Check shared README facts; translation quality still needs human review."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {'README.md', 'README.zh.md', 'README.zh-Hant.md', 'README.ja.md', 'README.ko.md'}


class ReadmeSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readmes = {p.name: p.read_text(encoding='utf-8') for p in ROOT.glob('README*.md')}
        cls.engines = {p.parent.name for p in (ROOT / 'skills/engines').glob('*/SKILL.md')}

    def test_all_documented_locales_are_present(self):
        self.assertTrue(LOCALES.issubset(self.readmes))

    def test_protocol_and_engines_match_in_every_locale(self):
        for name, text in self.readmes.items():
            with self.subTest(locale=name):
                blocks = re.findall(r'^```(?:text)?\n(.*?)^```', text, re.M | re.S)
                protocols = [block for block in blocks if block.startswith('USE:\n')]
                self.assertEqual(len(protocols), 1, 'one complete route example is required')
                block = protocols[0]
                self.assertEqual(re.findall(r'^(USE|ENGINE|ASK|DEFER):', block, re.M), ['USE', 'ENGINE', 'ASK', 'DEFER'])
                match = re.search(r'^ENGINE:\s*(.+)$', block, re.M)
                self.assertIsNotNone(match)
                options = [option.strip() for option in match.group(1).split('|')]
                self.assertEqual(set(options), self.engines | {'none', 'unknown'})
                self.assertEqual(len(options), len(set(options)), 'duplicate engine option')

    def test_every_engine_has_a_local_link_in_every_locale(self):
        for name, text in self.readmes.items():
            with self.subTest(locale=name):
                linked = set(re.findall(r'\]\(skills/engines/([a-z0-9-]+)/SKILL\.md\)', text))
                self.assertEqual(linked, self.engines)

    def test_shared_contract_catalog_and_contributing_are_linked(self):
        for name, text in self.readmes.items():
            with self.subTest(locale=name):
                for target in ['skills/SKILL.md', 'skills/dispatcher/SKILL.md', 'skills/CONTRACT.md', 'skills/catalog.json', 'CONTRIBUTING.md']:
                    self.assertIn(f']({target})', text)

    def test_verification_and_catalog_regeneration_are_documented(self):
        for name, text in self.readmes.items():
            with self.subTest(locale=name):
                commands = '\n'.join(re.findall(r'^```(?:bash|sh)\n(.*?)^```', text, re.M | re.S))
                for command in ['python3 -m pip install -r requirements-dev.txt', 'python3 -m unittest discover -s tests -v', 'python3 tools/skill_quality.py --check-catalog', 'python3 tools/skill_quality.py --write-catalog --check-catalog']:
                    self.assertIn(command, commands)

    def test_safe_main_update_is_documented(self):
        for name, text in self.readmes.items():
            with self.subTest(locale=name):
                commands = '\n'.join(re.findall(r'^```(?:bash|sh)\n(.*?)^```', text, re.M | re.S))
                self.assertIn('git switch main\ngit pull --ff-only origin main', commands)
                self.assertNotIn('git reset --hard', commands)
                self.assertIn('Python 3.10+', text)
                self.assertIn('--dry-run', text)
                self.assertIn('--copy', text)


if __name__ == '__main__':
    unittest.main()
