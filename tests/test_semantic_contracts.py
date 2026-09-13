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


if __name__ == '__main__':
    unittest.main()
