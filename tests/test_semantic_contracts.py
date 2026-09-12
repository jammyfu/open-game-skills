"""Guard corrected documentation examples, not engine or LLM behavior."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SemanticContractTests(unittest.TestCase):
    def test_pixel_animation_separates_attack_and_vulnerability(self):
        text = (ROOT / 'skills/2d/pixel-animation/SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('hit frames equal hurtbox frames', text)
        self.assertIn('hitbox is the attack volume', text)
        self.assertIn('hurtbox is the vulnerable volume', text)

    def test_positive_advantage_is_not_a_true_combo_proof(self):
        text = (ROOT / 'skills/disciplines/hitstun-recover/SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('the victim never gets a turn', text)
        block = re.search(r'```json\n(.*?)\n```', text, re.S)
        self.assertIsNotNone(block, 'a reviewable tick example is required')
        case = json.loads(block.group(1))
        advantage = case['victim_first_action_tick'] - case['attacker_first_action_tick']
        gap = case['followup_first_contact_tick'] - case['victim_first_action_tick']
        self.assertEqual(advantage, case['advantage_ticks'])
        self.assertEqual(gap, case['gap_ticks'])
        self.assertGreater(advantage, 0)
        self.assertGreater(gap, 0, 'positive advantage can still leave an actionable gap')


if __name__ == '__main__':
    unittest.main()
