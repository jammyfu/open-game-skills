"""Guard ownership and determinism contracts for enemy decision skills."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class EnemyDecisionOwnershipTests(unittest.TestCase):
    NAMES = (
        'enemy-ai', 'enemy-perception', 'aggro-table', 'target-priority',
        'group-tactics', 'squad-tactics', 'attack-tell', 'enemy-kit-balance',
    )

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_enemy_batch_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                desc = yaml.safe_load(front)['description']
                self.assertTrue(desc.strip().lower().startswith('use when '), desc)

    def test_enemy_ai_delegates_sensing_and_tells(self):
        text = self._text('enemy-ai').lower()
        self.assertIn('enemy-perception', text)
        self.assertIn('attack-tell', text)
        self.assertNotIn('sense is a cone + range + hearing', text)

    def test_perception_does_not_require_universal_drop_or_render_mesh_rules(self):
        text = self._text('enemy-perception').lower()
        self.assertNotIn('infinite chase is a bug', text)
        self.assertIn('line of sight', text)
        self.assertIn('hysteresis', text)
        self.assertIn('collision-layers', text)

    def test_aggro_and_target_selection_publish_stable_ties_and_switch_rules(self):
        for name in ('aggro-table', 'target-priority'):
            with self.subTest(skill=name):
                text = self._text(name).lower()
                self.assertIn('stable', text)
                self.assertRegex(text, r'tie|hysteresis|switch')
        self.assertNotIn('nearest is default', self._text('aggro-table').lower())
        self.assertNotIn('hard-lock uses stick-until-dead', self._text('target-priority').lower())

    def test_group_tactics_uses_concurrency_budget_not_single_attacker_law(self):
        text = self._text('group-tactics').lower()
        self.assertNotIn('one actor commits', text)
        self.assertNotIn('three armored bodies is over budget', text)
        self.assertRegex(text, r'concurr|token|budget')

    def test_squad_tactics_does_not_force_genre_camera_size_or_gun_policy(self):
        text = self._text('squad-tactics').lower()
        self.assertNotIn('a squad is 3–6 bodies', text)
        self.assertNotIn('view is top-down or iso', text)
        self.assertNotIn('guns are last resort', text)
        self.assertIn('project', text)

    def test_attack_tell_owns_warning_contract_not_universal_reaction_numbers(self):
        text = self._text('attack-tell').lower()
        self.assertNotIn('one-shot and grab tells default', text)
        self.assertNotIn('4f jab', text)
        self.assertIn('activation', text)
        self.assertIn('channel', text)

    def test_enemy_kit_does_not_impose_one_scary_move_or_two_hit_confirm(self):
        text = self._text('enemy-kit-balance').lower()
        self.assertNotIn('a kit gets **one** scary move', text)
        self.assertNotIn('2-hit confirm', text)
        self.assertIn('encounter', text)
        self.assertIn('group-tactics', text)


if __name__ == '__main__':
    unittest.main()
