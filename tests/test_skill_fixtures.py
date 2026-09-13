import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'skills' / 'fixtures'
CORPUS = ROOT / 'tests' / 'skills'


class SkillFixtureTests(unittest.TestCase):
    def test_the_legend_of_trump_fixture_is_pinned_and_scoped(self):
        path = FIXTURES / 'the-legend-of-trump.json'
        self.assertTrue(path.is_file(), 'missing pinned TheLegendOfTrump fixture manifest')
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['schema_version'], 1)
        self.assertEqual(data['id'], 'the-legend-of-trump')
        self.assertEqual(data['repository'], 'jammyfu/TheLegendOfTrump')
        self.assertRegex(data['commit'], r'^[a-f0-9]{40}$')
        self.assertEqual(data['commit'], '8871ee8293f815eff848d1064f05735cfe45ced8')
        self.assertIn('threejs', data['stack'])
        self.assertIn('react-three-fiber', data['stack'])
        self.assertIn('vite', data['stack'])
        self.assertGreaterEqual(len(data['observed_paths']), 6)
        for row in data['observed_paths']:
            self.assertRegex(row['sha'], r'^[a-f0-9]{40}$')
            self.assertFalse(row['path'].startswith('/'))
            self.assertNotIn('..', Path(row['path']).parts)

        coverage = json.loads((CORPUS / 'coverage.json').read_text(encoding='utf-8'))
        skills = set(coverage['skills'])
        self.assertGreaterEqual(len(data['applies_to']), 10)
        self.assertLessEqual(set(data['applies_to']), skills)
        self.assertNotIn('iap-offers', data['applies_to'])
        self.assertNotIn('matchmaking', data['applies_to'])


if __name__ == '__main__':
    unittest.main()
