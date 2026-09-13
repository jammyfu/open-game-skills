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


class CombatPipelineOwnershipTests(unittest.TestCase):
    NAMES = (
        'action-feel', 'hitbox-hurtbox', 'knockback-body', 'knockback-launch',
        'hitstun-recover', 'dodge-iframe', 'parry-guard', 'poise-stagger',
        'hyper-armor', 'landing-lag',
    )

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_combat_batch_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(skill=name):
                text = self._text(name)
                front = text.split('---', 2)[1]
                description = yaml.safe_load(front)['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_knockback_does_not_reference_missing_wall_splat_skill(self):
        for name in ('knockback-body', 'knockback-launch'):
            with self.subTest(skill=name):
                self.assertNotIn('wall-splat', self._text(name))

    def test_poise_pool_has_one_owner(self):
        poise = self._text('poise-stagger')
        armor = self._text('hyper-armor')
        self.assertIn('poise pool', poise.lower())
        self.assertNotIn('| poise-bar |', armor)
        self.assertIn('poise-stagger', armor)

    def test_dodge_invulnerability_is_not_implemented_by_deleting_hurtboxes(self):
        dodge = self._text('dodge-iframe')
        self.assertNotIn('Hurt boxes turn off', dodge)
        self.assertIn('eligibility', dodge.lower())

    def test_landing_lag_does_not_assume_connected_aerial_is_always_longer(self):
        landing = self._text('landing-lag')
        self.assertNotIn('Soft land (empty hop) is shorter than an aerial that connected', landing)


class CameraMovementInputOwnershipTests(unittest.TestCase):
    NAMES = (
        'camera-anti-clip', 'fov-comfort', 'locomotion', 'jump-leniency',
        'platform-jump', 'moving-platform', 'climb-vault', 'swim-water',
        'input-design', 'browser-input',
    )

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_batch_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                description = yaml.safe_load(front)['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_camera_collision_covers_near_plane_and_final_offsets(self):
        text = self._text('camera-anti-clip')
        self.assertNotIn('Shake and kick are offsets applied after the sweep.', text)
        self.assertRegex(text.lower(), r'near[- ]plane|frustum')
        self.assertRegex(text.lower(), r'shake.*(?:collision|validate|clamp)|(?:collision|validate|clamp).*shake')

    def test_jump_forgiveness_has_one_owner(self):
        locomotion = self._text('locomotion')
        platform = self._text('platform-jump')
        leniency = self._text('jump-leniency')
        self.assertNotIn('Coyote and jump buffer live here', locomotion)
        self.assertIn('jump-leniency', locomotion)
        self.assertIn('jump-leniency', platform)
        self.assertIn('owns', leniency.lower())

    def test_jump_leniency_does_not_hardcode_universal_millisecond_cap(self):
        text = self._text('jump-leniency')
        self.assertNotIn('Both under ~150ms unless the column says otherwise.', text)
        self.assertIn('logical', text.lower())

    def test_moving_platform_does_not_unconditionally_double_add_velocity(self):
        text = self._text('moving-platform')
        self.assertNotIn('A jump from a mover adds the platform velocity to v0 unless the column is one-shot-lift.', text)
        self.assertIn('relative', text.lower())

    def test_climb_and_swim_do_not_own_universal_input_or_camera_solid_rules(self):
        climb = self._text('climb-vault')
        swim = self._text('swim-water')
        self.assertNotIn('Jump and interact are not the same key on a 3D climber.', climb)
        self.assertIn('input-design', climb)
        self.assertNotIn('water plane as a collider', swim)
        self.assertIn('volume', swim.lower())

    def test_input_design_is_action_context_based_not_fixed_physical_keys(self):
        text = self._text('input-design')
        self.assertNotIn('Jump and confirm are not the same key on a 3D climber.', text)
        self.assertNotIn('The same key must not be Confirm and Cancel.', text)
        self.assertIn('action', text.lower())
        self.assertIn('context', text.lower())

    def test_browser_input_handles_browser_lifecycle_and_device_changes(self):
        text = self._text('browser-input').lower()
        for token in ('pointerlockchange', 'pointerlockerror', 'visibilitychange', 'pointercancel', 'gamepadconnected', 'gamepaddisconnected'):
            with self.subTest(token=token):
                self.assertIn(token, text)


class PersistenceEntitlementOwnershipTests(unittest.TestCase):
    NAMES = ('save-systems', 'save-integrity', 'cloud-save', 'settings-persist', 'entitlement-grant', 'restore-purchase')

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_batch_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                description = yaml.safe_load(front)['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_save_systems_requires_atomic_commit_and_migration_evidence(self):
        text = self._text('save-systems').lower()
        self.assertIn('atomic', text)
        self.assertIn('migration', text)
        self.assertRegex(text, r'previous|backup|last-known-good')

    def test_cloud_save_does_not_use_blind_last_write_for_divergent_progress(self):
        text = self._text('cloud-save').lower()
        self.assertNotIn('columns: one-slot | prompt-conflict | last-write-wins', text)
        self.assertRegex(text, r'revision|base version|ancestor|generation')
        self.assertIn('conflict', text)

    def test_settings_persist_is_versioned_and_atomic(self):
        text = self._text('settings-persist').lower()
        self.assertIn('schema', text)
        self.assertIn('atomic', text)
        self.assertIn('confirmed', text)

    def test_entitlement_grants_are_idempotent_across_crash_retry(self):
        text = self._text('entitlement-grant').lower()
        self.assertRegex(text, r'transaction|purchase token|event id')
        self.assertIn('idempotent', text)
        self.assertRegex(text, r'acknowledge|consume|finish')
        self.assertIn('pending', text)

    def test_restore_distinguishes_restorable_and_consumable_products(self):
        text = self._text('restore-purchase').lower()
        self.assertIn('consumable', text)
        self.assertRegex(text, r'non-consumable|subscription|restorable')
        self.assertIn('idempotent', text)


class DeterminismPerformanceEvidenceTests(unittest.TestCase):
    NAMES = ('netcode-feel', 'rng-seed', 'performance-budget', 'performance-optimization', 'telemetry-events', 'soak-stability')

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_batch_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                description = yaml.safe_load(front)['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_rollback_distinguishes_predicted_and_confirmed_events(self):
        text = self._text('netcode-feel').lower()
        self.assertNotIn('a rollback correction does not cancel a move the player already saw connect', text)
        self.assertIn('predicted', text)
        self.assertIn('confirmed', text)
        self.assertRegex(text, r'snapshot|restore')
        self.assertIn('rng', text)

    def test_rng_replay_captures_algorithm_stream_and_rollback_state(self):
        text = self._text('rng-seed').lower()
        self.assertNotIn('replay = seed + inputs', text)
        self.assertRegex(text, r'algorithm|version')
        self.assertRegex(text, r'stream.*state|state.*stream|counter')
        self.assertRegex(text, r'rollback|snapshot')

    def test_performance_budget_uses_percentiles_and_does_not_claim_equal_presentation_latency(self):
        text = self._text('performance-budget').lower()
        self.assertNotIn('feel is identical at 60 and 30 render because logic did not move', text)
        self.assertRegex(text, r'p95|p99|percentile')
        self.assertRegex(text, r'latency|frame pacing')
        self.assertNotIn('logic still 60', text)

    def test_optimization_consumes_budget_and_reports_critical_path(self):
        text = self._text('performance-optimization').lower()
        self.assertIn('performance-budget', text)
        self.assertRegex(text, r'critical path|cpu.*gpu|gpu.*cpu')
        self.assertRegex(text, r'p95|p99|percentile')

    def test_telemetry_has_versioned_schema_sampling_and_denominator_contract(self):
        text = self._text('telemetry-events').lower()
        self.assertIn('schema', text)
        self.assertIn('sampling', text)
        self.assertIn('denominator', text)
        self.assertRegex(text, r'consent|privacy|retention')

    def test_soak_tracks_slope_and_does_not_hardcode_slot_zero(self):
        text = self._text('soak-stability').lower()
        self.assertNotIn('slot 0 must still read', text)
        self.assertRegex(text, r'slope|trend')
        self.assertRegex(text, r'p95|p99|percentile')


if __name__ == '__main__':
    unittest.main()
