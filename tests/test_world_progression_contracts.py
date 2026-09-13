from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills" / "disciplines"


def text(name):
    return (BASE / name / "SKILL.md").read_text(encoding="utf-8")


class WorldProgressionContractTests(unittest.TestCase):
    def test_day_night_has_versioned_clock_contract(self):
        body = text("day-night")
        self.assertIn("time_cycle_id", body)
        self.assertIn("clock source", body)
        self.assertIn("transition identity", body)
        self.assertNotIn("ignore it and still finish the hook", body)

    def test_weather_has_stable_state_and_delegated_effects(self):
        body = text("weather-rules")
        self.assertIn("weather_state_id", body)
        self.assertIn("weather_revision", body)
        self.assertIn("effect owner", body)
        self.assertIn("presentation is not the rule oracle", body.lower())

    def test_chemistry_is_versioned_reaction_table_not_growth_formula(self):
        body = text("chemistry-verbs")
        self.assertIn("reaction_table_id", body)
        self.assertIn("reaction_id", body)
        self.assertNotIn("must multiply onto two old properties", body)
        self.assertNotIn("Do not add a ninth skill", body)

    def test_survival_needs_declares_timebase_and_threshold_policy(self):
        body = text("survival-needs")
        self.assertIn("needs_policy_id", body)
        self.assertIn("timebase", body)
        self.assertIn("threshold/effect policy", body)
        self.assertNotIn("Empty hunger is a published fail", body)

    def test_checkpoint_policy_delegates_bytes_and_cloud(self):
        body = text("save-checkpoint")
        self.assertIn("checkpoint_policy_id", body)
        self.assertIn("`save-systems`", body)
        self.assertIn("`cloud-save`", body)
        self.assertNotIn("unsaved 20-minute fight", body)

    def test_death_carry_is_idempotent_and_versioned(self):
        body = text("death-carry")
        self.assertIn("death_policy_id", body)
        self.assertIn("death_event_id", body)
        self.assertIn("exactly once", body)
        self.assertIn("drop/recovery record", body)

    def test_new_game_plus_has_cycle_and_carry_manifest(self):
        body = text("new-game-plus")
        self.assertIn("cycle_id", body)
        self.assertIn("carry_manifest", body)
        self.assertIn("entry predicate", body)
        self.assertNotIn("A natural clear", body)

    def test_roguelike_run_has_run_identity_and_ruleset_revision(self):
        body = text("roguelike-run")
        self.assertIn("run_id", body)
        self.assertIn("ruleset_revision", body)
        self.assertIn("RNG stream", body)
        self.assertIn("meta carry policy", body)

    def test_skill_tree_has_stable_graph_and_atomic_spend(self):
        body = text("skill-tree")
        self.assertIn("tree_id", body)
        self.assertIn("node_id", body)
        self.assertIn("prerequisite graph", body)
        self.assertIn("atomic", body)

    def test_deck_build_has_ruleset_zones_and_rng_owner(self):
        body = text("deck-build")
        self.assertIn("deck_ruleset_id", body)
        self.assertIn("card_id", body)
        self.assertIn("zone", body)
        self.assertIn("`rng-seed`", body)
        self.assertNotIn("Required first fight is possible with the starter deck", body)


if __name__ == "__main__":
    unittest.main()
