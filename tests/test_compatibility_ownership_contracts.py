"""Regression contracts for compatibility aliases and split design/runtime owners."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'skills' / 'disciplines'
A = ROOT / 'skills' / 'assets'


class CompatibilityOwnershipTests(unittest.TestCase):
    SEEDED = ('training-dummy','training-mode','racing-design','racing-feel','studio-column','studio-columns','move-tell','vfx-prompt')

    def text(self, name):
        return (D / name / 'SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.SEEDED:
            with self.subTest(skill=name):
                front = self.text(name).split('---',2)[1]
                desc = yaml.safe_load(front)['description'].strip().lower()
                self.assertTrue(desc.startswith('use when '), desc)

    def test_training_dummy_is_compatibility_entry_and_training_mode_is_owner(self):
        dummy = self.text('training-dummy').lower()
        mode = self.text('training-mode').lower()
        self.assertIn('compatibility entry', dummy)
        self.assertIn('training-mode', dummy)
        self.assertIn('owns the practice-room contract', mode)
        self.assertNotIn('fighting-design should ship at least dummy-block', mode)
        self.assertNotIn('lab-full is the default', mode)

    def test_racing_design_owns_race_structure_and_feel_owns_vehicle_response(self):
        design = self.text('racing-design').lower()
        feel = self.text('racing-feel').lower()
        self.assertIn('owns race structure', design)
        self.assertIn('racing-feel', design)
        self.assertIn('owns vehicle and speed response', feel)
        self.assertIn('racing-design', feel)
        self.assertNotIn('one readable decision every few seconds of travel:', design)
        self.assertNotIn('logical tick stays 60 hz', feel)

    def test_studio_alias_has_one_owner(self):
        alias = self.text('studio-column').lower()
        owner = self.text('studio-columns').lower()
        self.assertIn('compatibility entry', alias)
        self.assertIn('studio-columns', alias)
        self.assertIn('single owner', owner)

    def test_move_tell_is_compatibility_entry_for_attack_tell(self):
        move = self.text('move-tell').lower()
        attack = self.text('attack-tell').lower()
        self.assertIn('compatibility entry', move)
        self.assertIn('attack-tell', move)
        self.assertIn('warning contract', attack)
        self.assertNotIn('under 8f', move)

    def test_vfx_prompt_remains_alias_with_acceptance(self):
        prompt = self.text('vfx-prompt').lower()
        gen = (A / 'vfx-generate' / 'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('compatibility entry', prompt)
        self.assertIn('vfx-generate', prompt)
        self.assertIn('## accept', prompt)
        self.assertIn('all generation and acceptance rules remain here', gen)


if __name__ == '__main__':
    unittest.main()
