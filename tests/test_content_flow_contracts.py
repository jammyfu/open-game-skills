"""Guard ownership boundaries for level, tutorial, quest, dialogue, and cutscene skills."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class ContentFlowOwnershipTests(unittest.TestCase):
    NAMES = (
        'level-design', 'level-blockout', 'level-teach', 'teach-room',
        'tutorial-design', 'quest-graph', 'quest-beat', 'dialogue-flags',
        'cutscene-handoff', 'gameplay-validation',
    )

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                desc = yaml.safe_load(front)['description']
                self.assertTrue(desc.strip().lower().startswith('use when '), desc)

    def test_teach_room_is_compatibility_entry_not_second_owner(self):
        text = self._text('teach-room').lower()
        self.assertIn('level-teach', text)
        self.assertRegex(text, r'compat|delegate|alias')
        self.assertNotIn('one new verb per room', text)

    def test_level_design_uses_project_metrics_not_universal_30_second_density(self):
        text = self._text('level-design').lower()
        self.assertNotIn('one readable decision every 30 seconds', text)
        self.assertIn('project', text)
        self.assertRegex(text, r'metric|measure')

    def test_blockout_does_not_require_every_room_to_teach_one_new_verb(self):
        text = self._text('level-blockout').lower()
        self.assertNotIn('one new verb per room', text)
        self.assertNotIn('do not dress a room that has no teach/test beat', text)
        self.assertIn('metric', text)
        self.assertIn('gameplay-validation', text)

    def test_level_teach_keeps_safe_try_as_mode_not_universal_mandate(self):
        text = self._text('level-teach').lower()
        self.assertNotIn('do not skip safe-try', text)
        self.assertIn('safe-try', text)
        self.assertIn('project', text)
        self.assertIn('tutorial-design', text)

    def test_tutorial_design_owns_sequence_and_delegates_spatial_teaching(self):
        text = self._text('tutorial-design').lower()
        self.assertNotIn('three beats for each new verb', text)
        self.assertIn('level-teach', text)
        self.assertRegex(text, r'sequence|onboard|progress')

    def test_quest_graph_supports_multiple_active_hooks_and_stable_node_ids(self):
        text = self._text('quest-graph').lower()
        self.assertNotIn('one active hook', text)
        self.assertNotIn('the system may mark the *active* hook only', text)
        self.assertIn('stable', text)
        self.assertIn('node', text)
        self.assertIn('quest-beat', text)

    def test_quest_beat_models_recoverable_transaction_states(self):
        text = self._text('quest-beat').lower()
        self.assertIn('recover', text)
        self.assertRegex(text, r'fail|cancel|abandon')
        self.assertIn('stable', text)

    def test_dialogue_flags_are_namespaced_persistent_and_not_replay_mandatory(self):
        text = self._text('dialogue-flags').lower()
        self.assertIn('namespace', text)
        self.assertIn('save-systems', text)
        self.assertNotIn('the player can replay and see the other line', text)

    def test_cutscene_handoff_queues_safe_transition_instead_of_banning_hitstop_entry(self):
        text = self._text('cutscene-handoff').lower()
        self.assertNotIn('combat mid-hitstop cannot open a cinematic', text)
        self.assertRegex(text, r'queue|safe boundary|logical boundary')
        self.assertIn('idempot', text)
        self.assertIn('input', text)

    def test_gameplay_validation_is_explicit_about_not_run(self):
        text = self._text('gameplay-validation').lower()
        self.assertIn('not-run', text)
        self.assertIn('evidence', text)


if __name__ == '__main__':
    unittest.main()
