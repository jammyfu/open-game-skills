"""Guard engine adapter timing ownership against engine lifecycle assumptions."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EngineAdapterTimingTests(unittest.TestCase):
    NAMES = ('unity', 'unreal', 'godot', 'threejs', 'pixijs', 'phaser', 'cocos', 'custom')

    def _text(self, name):
        return (ROOT / f'skills/engines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_engine_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(engine=name):
                front = self._text(name).split('---', 2)[1]
                description = yaml.safe_load(front)['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_adapters_do_not_impose_universal_60hz_logic(self):
        forbidden = ('fixed 60hz', '60hz default', 'owns 60hz logic', 'acc >= 1/60', 'own a 60hz')
        for name in self.NAMES:
            text = self._text(name).lower()
            with self.subTest(engine=name):
                for token in forbidden:
                    self.assertNotIn(token, text)
                self.assertRegex(text, r'project|existing|configured|version')

    def test_unity_distinguishes_frame_and_fixed_loops(self):
        text = self._text('unity')
        self.assertIn('FixedUpdate', text)
        self.assertIn('Update', text)
        self.assertIn('Time.fixedDeltaTime', text)

    def test_unreal_does_not_treat_actor_tick_as_fixed_step(self):
        text = self._text('unreal').lower()
        self.assertRegex(text, r'actor tick.*frame|frame.*actor tick|aactor::tick.*frame')
        self.assertRegex(text, r'substep|fixed')

    def test_godot_distinguishes_idle_and_physics_processing(self):
        text = self._text('godot')
        self.assertIn('_process', text)
        self.assertIn('_physics_process', text)
        self.assertRegex(text.lower(), r'physics.*(?:fps|tick)|configured')

    def test_web_adapters_treat_tickers_as_frame_driven(self):
        expectations = {
            'threejs': ('useFrame', 'AnimationMixer.update'),
            'pixijs': ('Ticker', 'frame'),
            'phaser': ('TimeStep', 'frame'),
            'cocos': ('update', 'frame'),
        }
        for name, tokens in expectations.items():
            text = self._text(name)
            with self.subTest(engine=name):
                for token in tokens:
                    self.assertIn(token.lower(), text.lower())

    def test_each_adapter_requires_version_and_runtime_evidence(self):
        for name in self.NAMES:
            text = self._text(name).lower()
            with self.subTest(engine=name):
                self.assertRegex(text, r'version|package|engine')
                self.assertRegex(text, r'accept|evidence|verify|test')


if __name__ == '__main__':
    unittest.main()
