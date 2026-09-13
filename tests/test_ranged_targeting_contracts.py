from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "skills" / "disciplines"


def read(name):
    return (D / name / "SKILL.md").read_text(encoding="utf-8")


class RangedTargetingContractTests(unittest.TestCase):
    def test_aim_assist_transforms_intent_not_hit_truth(self):
        text = read("aim-assist")
        for token in ("assist_profile_id", "raw aim", "assisted aim", "target_id"):
            self.assertIn(token, text)
        self.assertIn("never enlarges hit geometry", text)

    def test_cover_space_owns_affordance_and_cover_shooter_consumes_it(self):
        space = read("cover-space")
        shooter = read("cover-shooter")
        self.assertIn("cover_anchor_id", space)
        self.assertIn("geometry/collision revision", space)
        self.assertIn("cover_session_id", shooter)
        self.assertIn("`cover-space` owns valid anchors/capabilities", shooter)
        self.assertIn("Exactly one system owns the actor's cover locomotion", shooter)

    def test_enemy_fire_has_sequence_and_replay_identity(self):
        text = read("enemy-fire")
        for token in ("fire_pattern_id", "fire_sequence_id", "shot IDs", "RNG stream ID"):
            self.assertIn(token, text)
        self.assertIn("shot slot commits at most once", text)

    def test_fps_feel_does_not_own_hit_reload_or_swap_truth(self):
        text = read("fps-feel")
        for owner in ("`projectile-hitscan`", "`ammo-reload`", "`weapon-swap`", "`input-design`"):
            self.assertIn(owner, text)
        self.assertIn("cannot retroactively change an already committed shot query", text)

    def test_keyboard_mouse_mapping_is_a_preset_layer(self):
        text = read("kb-mouse-map")
        self.assertIn("`input-design` owns semantic actions", text)
        self.assertIn("input_preset_id", text)
        self.assertIn("conventions, not mandatory universal core controls", text)

    def test_lock_on_has_session_revision_and_deterministic_switching(self):
        text = read("lock-on-target")
        for token in ("lock_session_id", "target_id", "targeting revision", "tie-break", "hysteresis"):
            self.assertIn(token, text)
        self.assertIn("render iteration order", text)

    def test_ranged_resolution_has_stable_shot_identity(self):
        text = read("projectile-hitscan")
        for token in ("shot_id", "projectile_id", "collision/filter revision", "impact event IDs"):
            self.assertIn(token, text)
        self.assertIn("presentation cannot alter hit/no-hit truth", text.lower())

    def test_overwatch_uses_trigger_identity_and_deterministic_ties(self):
        text = read("overwatch-fire")
        for token in ("overwatch_session_id", "trigger event/request ID", "tie-break"):
            self.assertIn(token, text)
        self.assertIn("consumes readiness at most once", text)

    def test_stealth_info_consumes_perception_truth(self):
        text = read("stealth-info")
        self.assertIn("`enemy-perception` owns detection/suspicion truth", text)
        self.assertIn("perception revision", text)
        self.assertIn("derived presentation, not a detection query", text)


if __name__ == "__main__":
    unittest.main()
