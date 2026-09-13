import json
from pathlib import Path
import re
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
        self.assertEqual(data['usage_policy'], 'asset-sample-only')
        self.assertIs(data['implementation_authority'], False)
        self.assertNotIn('stack', data, 'demo implementation must not be treated as fixture authority')
        self.assertGreaterEqual(len(data['observed_paths']), 8)
        allowed_roots = ('assets/', 'public/audio/', 'public/models/')
        forbidden_roots = ('src/', 'tests/', 'scripts/')
        observed_kinds = set()
        for row in data['observed_paths']:
            self.assertEqual(set(row), {'path', 'sha', 'size', 'kind'})
            self.assertRegex(row['sha'], r'^[a-f0-9]{40}$')
            self.assertGreater(row['size'], 0)
            self.assertTrue(row['path'].startswith(allowed_roots), row['path'])
            self.assertFalse(row['path'].startswith(forbidden_roots), row['path'])
            self.assertFalse(row['path'].startswith('/'))
            self.assertNotIn('..', Path(row['path']).parts)
            observed_kinds.add(row['kind'])
        self.assertGreaterEqual(observed_kinds, {'concept-image', 'dcc-source', 'runtime-model', 'audio'})

        coverage = json.loads((CORPUS / 'coverage.json').read_text(encoding='utf-8'))
        skills = set(coverage['skills'])
        self.assertGreaterEqual(len(data['applies_to']), 8)
        self.assertLessEqual(set(data['applies_to']), skills)
        for implementation_skill in (
            'threejs', 'browser-input', 'locomotion', 'game-state-flow',
            'gameplay-validation', 'performance-optimization',
        ):
            self.assertNotIn(implementation_skill, data['applies_to'])
        self.assertIn('materials', data['applies_to'])
        self.assertIn('model-pipeline', data['applies_to'])


if __name__ == '__main__':
    unittest.main()
