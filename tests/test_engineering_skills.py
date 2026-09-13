"""Verify authored engineering contracts and cases, not agent behavior."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('game-state-flow', 'asset-runtime', 'procedural-generation', 'terrain-surface', 'world-streaming', 'physics-interaction')
HEADINGS = ('Scope', 'Modes', 'Procedure', 'Outputs', 'Acceptance', 'References')


class EngineeringSkillTests(unittest.TestCase):
    def test_skills_have_bounded_contracts(self):
        for name in NAMES:
            with self.subTest(skill=name):
                path = ROOT / f'skills/disciplines/{name}/SKILL.md'
                self.assertTrue(path.is_file(), f'missing {name}')
                text = path.read_text(encoding='utf-8')
                self.assertIn('description: Use when ', text)
                for heading in HEADINGS:
                    self.assertIn(f'## {heading}\n', text)
                self.assertLess(len(text.splitlines()), 120)
                self.assertIn('assets/contract.example.json', text)
                self.assertIn('assets/evals.json', text)
                self.assertIn('not-run', text)

    def test_each_skill_has_a_valid_mode_example_and_three_case_classes(self):
        ids = set()
        for name in NAMES:
            with self.subTest(skill=name):
                path = ROOT / f'skills/disciplines/{name}'
                self.assertTrue((path / 'assets/contract.example.json').is_file())
                example = json.loads((path / 'assets/contract.example.json').read_text())
                self.assertEqual(example['skill'], name)
                self.assertEqual(example['status'], 'not-run')
                body = (path / 'SKILL.md').read_text()
                self.assertIn(f"| {example['mode']} |", body)
                cases = json.loads((path / 'assets/evals.json').read_text())
                self.assertEqual({c['kind'] for c in cases}, {'normal', 'boundary', 'adversarial'})
                for case in cases:
                    self.assertNotIn(case['id'], ids)
                    ids.add(case['id'])
                    self.assertGreater(len(case['prompt']), 20)
                    self.assertGreaterEqual(len(case['criteria']), 3)
                    self.assertEqual(case['skill'], name)
                    self.assertNotIn('result', case, 'scenarios are not measured results')

    def test_new_skills_are_routable_without_forcing_project_modes(self):
        dispatcher = (ROOT / 'skills/dispatcher/SKILL.md').read_text(encoding='utf-8')
        for name in NAMES:
            with self.subTest(skill=name):
                self.assertIn(f'`{name} / select`', dispatcher)
        self.assertIn('../engineering-registry.json', dispatcher)

    def test_dispatcher_has_observable_acceptance(self):
        dispatcher = (ROOT / 'skills/dispatcher/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('## Acceptance\n', dispatcher)
        self.assertIn('three specialized skills', dispatcher)
        self.assertIn('Replace unresolved', dispatcher)

    def test_readme_locales_link_the_six_skills_and_evidence_instructions(self):
        for path in ROOT.glob('README*.md'):
            with self.subTest(locale=path.name):
                text = path.read_text(encoding='utf-8')
                for name in NAMES:
                    self.assertIn(f'](skills/disciplines/{name}/SKILL.md)', text)
                self.assertIn('](docs/EVALUATION.md)', text)
                self.assertIn('python3 tools/engineering_quality.py', text)
                self.assertIn('not-run', text)

    def test_shared_execution_contract_links_the_scoped_registry(self):
        text = (ROOT / 'skills/CONTRACT.md').read_text(encoding='utf-8')
        self.assertIn('](engineering-registry.json)', text)
        self.assertIn('](references/engineering-workflow.md)', text)

if __name__ == '__main__':
    unittest.main()
