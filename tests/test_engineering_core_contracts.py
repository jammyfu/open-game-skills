"""Guard ownership boundaries for the engineering-core skills."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EngineeringCoreOwnershipTests(unittest.TestCase):
    NAMES = ('game-state-flow', 'asset-runtime', 'procedural-generation', 'terrain-surface', 'world-streaming', 'physics-interaction')

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_engineering_core_descriptions_are_trigger_only(self):
        import yaml
        for name in self.NAMES:
            with self.subTest(skill=name):
                description = yaml.safe_load(self._text(name).split('---', 2)[1])['description']
                self.assertTrue(description.strip().lower().startswith('use when '), description)

    def test_procedural_generation_delegates_rng_algorithm_and_stream_state(self):
        text = self._text('procedural-generation')
        self.assertNotIn('Derive named random streams with a documented stable algorithm.', text)
        self.assertRegex(text.lower(), r'rng-seed.*owns|owned by.*rng-seed')
        self.assertRegex(text.lower(), r'stream.*request|request.*stream')

    def test_game_state_flow_uses_identity_and_stale_task_guards(self):
        text = self._text('game-state-flow').lower()
        self.assertRegex(text, r'session.*id|round.*id')
        self.assertIn('epoch', text)
        self.assertIn('idempotent', text)

    def test_asset_runtime_separates_consumer_lease_from_shared_resource(self):
        text = self._text('asset-runtime').lower()
        self.assertIn('lease', text)
        self.assertRegex(text, r'shared.*(?:release|request|resource)|(?:release|request|resource).*shared')
        self.assertRegex(text, r'epoch|stale')

    def test_streaming_has_readiness_gates_and_dirty_state_policy(self):
        text = self._text('world-streaming').lower()
        self.assertRegex(text, r'collision-ready|navigation-ready|active')
        self.assertRegex(text, r'dirty|delta')
        self.assertIn('hysteresis', text)

    def test_physics_interaction_has_single_motion_owner(self):
        text = self._text('physics-interaction').lower()
        self.assertRegex(text, r'one system writes|motion authority')
        self.assertRegex(text, r'continuous collision|sweep')


if __name__ == '__main__':
    unittest.main()
