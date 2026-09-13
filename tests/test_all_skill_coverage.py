import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
CORPUS = ROOT / 'tests' / 'skills'


def actual_skills():
    rows = []
    for path in sorted(SKILLS.rglob('SKILL.md')):
        rel = path.relative_to(SKILLS).as_posix()
        text = path.read_text(encoding='utf-8')
        name = next(line.split(':', 1)[1].strip() for line in text.splitlines() if line.startswith('name:'))
        rows.append((name, rel))
    return rows


def profile(name):
    path = CORPUS / 'profiles' / f'{name}.json'
    return json.loads(path.read_text(encoding='utf-8'))


class AllSkillCoverageTests(unittest.TestCase):
    def test_every_skill_has_exactly_one_case_file(self):
        coverage_path = CORPUS / 'coverage.json'
        self.assertTrue(coverage_path.is_file(), 'missing tests/skills/coverage.json')
        coverage = json.loads(coverage_path.read_text(encoding='utf-8'))
        self.assertEqual(coverage['schema_version'], 1)
        expected = actual_skills()
        self.assertEqual(coverage['skills'], [name for name, _ in expected])

        actual_paths = sorted((CORPUS / 'cases').rglob('*.json'))
        self.assertEqual(len(actual_paths), len(expected), 'case count must equal skill count')
        seen = []
        for case_path in actual_paths:
            case = json.loads(case_path.read_text(encoding='utf-8'))
            seen.append((case['skill'], case['skill_path']))
            with self.subTest(skill=case['skill']):
                self.assertEqual(case['schema_version'], 1)
                self.assertEqual(case_path.relative_to(ROOT).as_posix(), f"tests/skills/cases/{case['category']}/{case['skill']}.json")
                self.assertIn(case['review_state'], {'seeded', 'reviewed'})
                if case['review_state'] == 'seeded':
                    self.assertEqual(set(case), {'schema_version','skill','skill_path','category','review_state','scenario_profile'})
                    definition = profile(case['scenario_profile'])
                    self.assertEqual(definition['scenario_kinds'], ['normal', 'boundary', 'adversarial'])
                    self.assertEqual(set(definition['templates']), {'normal', 'boundary', 'adversarial'})
                    self.assertGreaterEqual(len(definition['criteria']), 3)
                else:
                    scenarios = case['scenarios']
                    self.assertEqual({item['kind'] for item in scenarios}, {'normal', 'boundary', 'adversarial'})
                    self.assertEqual(len(scenarios), 3)
                    for scenario in scenarios:
                        self.assertTrue(scenario['prompt'].strip())
                        self.assertGreaterEqual(len(scenario['criteria']), 3)
                        self.assertNotIn('result', scenario)
                        self.assertNotIn('status', scenario)
        self.assertEqual(sorted(seen, key=lambda row: row[1]), expected)

    def test_coverage_is_sorted_and_names_are_unique(self):
        coverage = json.loads((CORPUS / 'coverage.json').read_text(encoding='utf-8'))
        names = coverage['skills']
        self.assertEqual(names, [name for name, _ in actual_skills()])
        self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':
    unittest.main()
