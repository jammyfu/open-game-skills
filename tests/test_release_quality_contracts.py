"""Regression contracts for QA, release evidence, live-ops and platform targets."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills' / 'disciplines'


class ReleaseQualityOwnershipTests(unittest.TestCase):
    NAMES = (
        'game-qa', 'test-matrix', 'cert-handoff', 'gameplay-capture',
        'live-ops', 'patch-cadence', 'platform-targets', 'ship-checklist',
        'debug-slate',
    )

    def text(self, name):
        return (SKILLS / name / 'SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self.text(name).split('---', 2)[1]
                desc = yaml.safe_load(front)['description'].strip().lower()
                self.assertTrue(desc.startswith('use when '), desc)

    def test_game_qa_is_single_owner_of_test_pass_taxonomy(self):
        qa = self.text('game-qa').lower()
        matrix = self.text('test-matrix').lower()
        self.assertIn('owns the qa pass taxonomy', qa)
        self.assertIn('compatibility entry', matrix)
        self.assertIn('game-qa', matrix)
        self.assertNotIn('smoke ≤ 10 min', matrix)

    def test_cert_handoff_does_not_force_controller_loss_to_menu(self):
        text = self.text('cert-handoff').lower()
        self.assertNotIn('pad-lost is a menu', text)
        self.assertIn('policy', text)
        self.assertIn('input-design', text)
        self.assertIn('game-qa', text)

    def test_capture_evidence_has_stable_provenance(self):
        text = self.text('gameplay-capture').lower()
        for token in ('capture id', 'build id', 'source take', 'edit'):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn('pause the game and pause the recorder as two buttons', text)

    def test_live_ops_is_versioned_and_has_fallback(self):
        text = self.text('live-ops').lower()
        for token in ('event id', 'config revision', 'eligibility', 'fallback', 'idempotent'):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_patch_cadence_owns_rollout_and_compatibility_not_fixed_content_policy(self):
        text = self.text('patch-cadence').lower()
        for token in ('minimum client', 'rollback', 'rollout', 'schema'):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn('| weekly-live | offers, cosmetics, sinks |', text)
        self.assertNotIn('slot 0', text)

    def test_platform_targets_do_not_hardcode_frame_rates_or_pause_menu_budget_ui(self):
        text = self.text('platform-targets').lower()
        self.assertNotIn('unlocked or 60', text)
        self.assertNotIn('30 or 60 plus a mode', text)
        self.assertNotIn('publishes both budgets in the pause menu', text)
        self.assertIn('capability', text)
        self.assertIn('performance-budget', text)

    def test_ship_checklist_is_evidence_manifest_not_one_fixed_first_room(self):
        text = self.text('ship-checklist').lower()
        for token in ('release manifest', 'build id', 'target', 'blocker', 'game-qa'):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn('can finish the first teach room', text)

    def test_debug_slate_records_structured_session_provenance(self):
        text = self.text('debug-slate').lower()
        for token in ('session id', 'build id', 'structured', 'save-integrity'):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn('dev builds show them', text)


if __name__ == '__main__':
    unittest.main()
