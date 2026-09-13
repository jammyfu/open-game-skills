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


class AllSkillCoverageTests(unittest.TestCase):
    def test_every_skill_has_exactly_one_case_file(self):
        coverage_path = CORPUS / 'coverage.json'
        self.assertTrue(coverage_path.is_file(), 'missing tests/skills/coverage.json')
        coverage = json.loads(coverage_path.read_text(encoding='utf-8'))
        self.assertEqual(coverage['schema_version'], 1)
        entries = coverage['entries']
        self.assertEqual([(row['skill'], row['skill_path']) for row in entries], actual_skills())

        declared = {row['case_path'] for row in entries}
        actual = {p.relative_to(ROOT).as_posix() for p in (CORPUS / 'cases').rglob('*.json')}
        self.assertEqual(declared, actual, 'case files must match coverage one-to-one')

        for row in entries:
            with self.subTest(skill=row['skill']):
                case_path = ROOT / row['case_path']
                self.assertTrue(case_path.is_file())
                case = json.loads(case_path.read_text(encoding='utf-8'))
                self.assertEqual(case['schema_version'], 1)
                self.assertEqual(case['skill'], row['skill'])
                self.assertEqual(case['skill_path'], row['skill_path'])
                self.assertEqual(case['category'], row['category'])
                self.assertIn(case['review_state'], {'seeded', 'reviewed'})
                self.assertEqual({item['kind'] for item in case['scenarios']}, {'normal', 'boundary', 'adversarial'})
                self.assertEqual(len(case['scenarios']), 3)
                for scenario in case['scenarios']:
                    self.assertTrue(scenario['prompt'].strip())
                    self.assertGreaterEqual(len(scenario['criteria']), 3)
                    self.assertNotIn('result', scenario)
                    self.assertNotIn('status', scenario)

    def test_coverage_is_sorted_and_names_are_unique(self):
        coverage = json.loads((CORPUS / 'coverage.json').read_text(encoding='utf-8'))
        entries = coverage['entries']
        self.assertEqual(entries, sorted(entries, key=lambda row: row['skill_path']))
        names = [row['skill'] for row in entries]
        self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':
    unittest.main()
