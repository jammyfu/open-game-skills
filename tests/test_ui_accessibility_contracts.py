"""Guard UI focus, accessibility, localization, and presentation ownership."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class UIAccessibilityOwnershipTests(unittest.TestCase):
    NAMES = ('ui-flow','ui-hud-focus','menu-flow','hud-feedback','a11y-controls','game-localization','visual-novel-ui')

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                desc = yaml.safe_load(self._text(name).split('---',2)[1])['description']
                self.assertTrue(desc.strip().lower().startswith('use when '), desc)

    def test_ui_flow_owns_screen_state_not_physical_key_rules(self):
        text=self._text('ui-flow').lower()
        self.assertNotIn('confirm and cancel stay distinct', text)
        self.assertIn('state', text)
        self.assertIn('ui-hud-focus', text)
        self.assertIn('input-design', text)

    def test_menu_flow_is_compatibility_entry_not_duplicate_owner(self):
        text=self._text('menu-flow').lower()
        self.assertRegex(text, r'compat|delegate|alias')
        self.assertIn('ui-flow', text)
        self.assertIn('ui-hud-focus', text)
        self.assertNotIn('esc is pause or back', text)
        self.assertNotIn('menu that opens mid-hitstop waits until the clock resumes', text)

    def test_focus_contract_is_explicit_and_restorable(self):
        text=self._text('ui-hud-focus').lower()
        self.assertIn('focus', text)
        self.assertIn('restore', text)
        self.assertIn('visible', text)
        self.assertIn('input-design', text)

    def test_hud_feedback_does_not_hardcode_durability_threshold(self):
        text=self._text('hud-feedback').lower()
        self.assertNotIn('≤3 hits', text)
        self.assertIn('state', text)
        self.assertRegex(text, r'color|colour')
        self.assertIn('not', text)

    def test_a11y_controls_uses_action_remap_and_alternative_input_without_changing_logic(self):
        text=self._text('a11y-controls').lower()
        self.assertIn('action', text)
        self.assertIn('remap', text)
        self.assertRegex(text, r'toggle|hold')
        self.assertRegex(text, r'digital|alternative')
        self.assertIn('reduced', text)
        self.assertIn('hitbox', text)

    def test_localization_uses_stable_string_ids_and_runtime_safe_switch(self):
        text=self._text('game-localization').lower()
        self.assertIn('stable', text)
        self.assertIn('string id', text)
        self.assertIn('fallback', text)
        self.assertIn('live', text)
        self.assertNotIn('sync readme / help / maker notes / store shots', text)

    def test_visual_novel_ui_uses_stable_line_identity_and_choice_safe_skip(self):
        text=self._text('visual-novel-ui').lower()
        self.assertIn('stable', text)
        self.assertIn('dialogue-flags', text)
        self.assertIn('choice', text)
        self.assertIn('skip', text)
        self.assertIn('game-localization', text)


if __name__ == '__main__':
    unittest.main()
