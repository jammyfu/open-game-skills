import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

import skill_test_runner


class AllSkillContractTests(unittest.TestCase):
    def test_all_current_skills_have_no_hard_contract_errors(self):
        report = skill_test_runner.check_all(ROOT)
        self.assertEqual(report['skills'], 187)
        self.assertEqual(report['hard_errors'], [], '\n'.join(report['hard_errors']))
        self.assertIn('description_trigger', report['review_candidates'])
        self.assertIn('acceptance_signal', report['review_candidates'])

    def test_seeded_profile_materializes_three_scenarios_without_results(self):
        case = json.loads((ROOT / 'tests/skills/cases/disciplines/action-feel.json').read_text())
        scenarios = skill_test_runner.materialize_scenarios(ROOT, case)
        self.assertEqual([row['kind'] for row in scenarios], ['normal', 'boundary', 'adversarial'])
        for row in scenarios:
            self.assertEqual(set(row), {'id', 'kind', 'prompt', 'criteria'})
            self.assertNotIn('result', row)
            self.assertGreaterEqual(len(row['criteria']), 3)


if __name__ == '__main__':
    unittest.main()
