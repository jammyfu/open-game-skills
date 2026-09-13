from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills" / "disciplines"


def text(name):
    return (BASE / name / "SKILL.md").read_text(encoding="utf-8")


class EncounterProgressionContractTests(unittest.TestCase):
    def test_balance_is_versioned_policy_not_universal_counter_philosophy(self):
        body = text("balance-design")
        self.assertIn("balance_policy_id", body)
        self.assertIn("metric definition and denominator", body)
        self.assertNotIn("Soft counters beat hard deletes", body)
        self.assertNotIn("Feel columns outrank spreadsheet columns", body)

    def test_boss_design_uses_authored_risk_readability_not_damage_telegraph_formula(self):
        body = text("boss-design")
        self.assertIn("boss_encounter_id", body)
        self.assertIn("risk/readability policy", body)
        self.assertNotIn("A one-shot is slower than a jab", body)
        self.assertNotIn("Story bosses sit on the main path", body)

    def test_difficulty_is_project_policy_not_fixed_layer_order(self):
        body = text("difficulty-design")
        self.assertIn("difficulty_policy_id", body)
        self.assertIn("measurement context", body)
        self.assertNotIn("Three layers (always this order)", body)
        self.assertNotIn("Default for exploration games", body)

    def test_encounter_design_supports_composite_encounters_and_stable_identity(self):
        body = text("encounter-design")
        self.assertIn("encounter_id", body)
        self.assertIn("state/beat graph", body)
        self.assertNotIn("One idea per encounter", body)
        self.assertNotIn("drop covers spend", body)

    def test_first_session_value_is_genre_neutral_and_offer_is_separate(self):
        body = text("first-session-value")
        self.assertIn("session_variant_id", body)
        self.assertIn("core challenge or decision", body)
        self.assertNotIn("goal, one fight, reward, next step", body)
        self.assertIn("game-monetization", body)

    def test_game_planning_has_slice_identity_and_revision(self):
        body = text("game-planning")
        self.assertIn("slice_id", body)
        self.assertIn("slice_revision", body)
        self.assertIn("acceptance evidence", body)

    def test_puzzle_design_does_not_force_one_room_or_tooltip_failure(self):
        body = text("puzzle-design")
        self.assertIn("puzzle_id", body)
        self.assertIn("legal solution policy", body)
        self.assertNotIn("One room, one new combination", body)
        self.assertNotIn("A tooltip that names the solution is a fail", body)

    def test_set_piece_owns_handoff_not_mandatory_input_shape(self):
        body = text("set-piece-action")
        self.assertIn("set_piece_id", body)
        self.assertIn("control/handoff policy", body)
        self.assertNotIn("not a cut that plays itself", body)
        self.assertNotIn("Enemies may not snipe from off-camera", body)

    def test_spawn_wave_has_wave_identity_and_visibility_policy(self):
        body = text("spawn-wave")
        self.assertIn("wave_id", body)
        self.assertIn("spawn_visibility_policy", body)
        self.assertNotIn("Spawn points are off-camera or gated", body)
        self.assertNotIn("Player can feel a pause between packs", body)

    def test_tower_wave_consumes_spawn_owner_and_has_schedule_revision(self):
        body = text("tower-wave")
        self.assertIn("wave_schedule_id", body)
        self.assertIn("schedule_revision", body)
        self.assertIn("`spawn-wave`", body)
        self.assertNotIn("A wave is a published count and interval", body)


if __name__ == "__main__":
    unittest.main()
