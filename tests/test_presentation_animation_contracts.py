"""Regression contracts for presentation, audio, camera and animation ownership."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'skills' / 'disciplines'


class PresentationAnimationContracts(unittest.TestCase):
    NAMES = ('audio-buses','audio-feel','haptic-rumble','juice-vfx','camera-shots','animation-blend','animation-graph','ik-foot-locking','face-morph','avatar-create')

    def text(self, name):
        return (D / name / 'SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                desc = yaml.safe_load(self.text(name).split('---',2)[1])['description'].strip().lower()
                self.assertTrue(desc.startswith('use when '), desc)

    def test_audio_buses_own_routing_not_universal_gameplay_event_policy(self):
        text = self.text('audio-buses').lower()
        self.assertIn('routing', text)
        self.assertIn('duck', text)
        self.assertIn('audio-feel', text)
        self.assertNotIn('hitstop does not mute sfx', text)

    def test_audio_feel_uses_event_identity_not_hardcoded_mix_numbers(self):
        text = self.text('audio-feel').lower()
        for token in ('event id', 'logical event', 'audio-buses', 'fallback'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('1–2 db', text)
        self.assertNotIn('ui confirms are shorter than combat hits', text)
        self.assertNotIn('publish stems for explore / fight / win / fail / retry', text)

    def test_haptics_have_capability_fallback_and_are_not_sole_critical_signal(self):
        text = self.text('haptic-rumble').lower()
        for token in ('capability', 'fallback', 'critical'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('intensity cap per second', text)

    def test_vfx_is_presentation_and_has_no_universal_duration(self):
        text = self.text('juice-vfx').lower()
        self.assertIn('presentation', text)
        self.assertIn('authoritative', text)
        self.assertNotIn('under 200ms', text)
        self.assertNotIn('pause-frame extra', text)

    def test_camera_shots_do_not_own_gameplay_targeting_or_universal_hitstop_rules(self):
        text = self.text('camera-shots').lower()
        for token in ('presentation', 'camera-anti-clip', 'target'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('do not change shot mid-hitstop', text)
        self.assertNotIn('combat may not', text)
        self.assertNotIn('30 seconds', text)

    def test_animation_blend_owns_pose_composition_not_gameplay_state(self):
        text = self.text('animation-blend').lower()
        self.assertIn('presentation', text)
        self.assertIn('gameplay', text)
        self.assertNotIn('cuts use inertialization or a 2-6 frame fade.', text)
        self.assertNotIn('cuts use inertialization or a 2–6 frame fade.', text)

    def test_animation_graph_allows_weighted_layer_composition(self):
        text = self.text('animation-graph').lower()
        for token in ('weighted', 'layer', 'gameplay state'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('two clips never write the same bone channel', text)
        self.assertNotIn('hitstop sets that skeleton `timescale` to 0', text)

    def test_foot_locking_supports_joint_fallbacks_and_moving_surfaces(self):
        text = self.text('ik-foot-locking').lower()
        for token in ('foot/ankle', 'moving', 'relative', 'pelvis'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('lock the toe, not the heel', text)
        self.assertNotIn('3-5 frame majority vote', text)
        self.assertNotIn('toe travel < 1 cm', text)

    def test_face_morph_is_presentation_rate_independent_and_stable_schema(self):
        text = self.text('face-morph').lower()
        for token in ('stable', 'range', 'neutral', 'presentation'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('weights live on the logic tick', text)

    def test_avatar_creation_has_stable_identity_and_no_universal_unlock_policy(self):
        text = self.text('avatar-create').lower()
        for token in ('stable', 'save', 'rig', 'gameplay'):
            with self.subTest(token=token): self.assertIn(token, text)
        self.assertNotIn('identity (skin, body) is available up front', text)
        self.assertNotIn('wardrobe can unlock later', text)


if __name__ == '__main__':
    unittest.main()
