from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills" / "disciplines"


def text(name):
    return (BASE / name / "SKILL.md").read_text(encoding="utf-8")


class SessionMultiplayerContractTests(unittest.TestCase):
    def test_local_coop_has_stable_session_player_and_device_identity(self):
        body = text("local-coop")
        self.assertIn("coop_session_id", body)
        self.assertIn("player_id", body)
        self.assertIn("device_id", body)
        self.assertIn("join/leave request", body)
        self.assertNotIn("Extra cameras drop shadows first", body)

    def test_matchmaking_has_ticket_ruleset_and_compatibility_contract(self):
        body = text("matchmaking")
        self.assertIn("match_ticket_id", body)
        self.assertIn("match_ruleset_id", body)
        self.assertIn("compatibility predicate", body)
        self.assertIn("idempotent", body)
        self.assertNotIn("Casual does not hide a hidden MMR", body)

    def test_party_follow_has_companion_identity_and_recovery_policy(self):
        body = text("party-follow")
        self.assertIn("party_id", body)
        self.assertIn("follower_id", body)
        self.assertIn("recovery policy", body)
        self.assertNotIn("slower accel", body)
        self.assertNotIn("teleport only after a published wait", body)

    def test_roster_select_has_selection_identity_and_ready_commit(self):
        body = text("roster-select")
        self.assertIn("roster_id", body)
        self.assertIn("selection_id", body)
        self.assertIn("ready/commit", body)
        self.assertIn("idempotent", body)
        self.assertNotIn("Blind select is for versus only", body)

    def test_plan_queue_has_command_identity_and_commit_order(self):
        body = text("plan-queue")
        self.assertIn("plan_session_id", body)
        self.assertIn("command_id", body)
        self.assertIn("commit order", body)
        self.assertIn("idempotent", body)
        self.assertNotIn("all verbs start the same logic tick", body)

    def test_pause_owns_time_policy_not_fixed_timescale_assumptions(self):
        body = text("pause-timescale")
        self.assertIn("pause_policy_id", body)
        self.assertIn("pause_request_id", body)
        self.assertIn("arbitration", body)
        self.assertIn("clock owner", body)
        self.assertNotIn("only if netcode column allows", body)

    def test_rhythm_judge_has_chart_event_and_calibration_identity(self):
        body = text("rhythm-judge")
        self.assertIn("chart_id", body)
        self.assertIn("note_event_id", body)
        self.assertIn("calibration", body)
        self.assertIn("clock mapping", body)
        self.assertNotIn("Off-window is a miss", body)

    def test_ghost_line_versions_replay_and_track_compatibility(self):
        body = text("ghost-line")
        self.assertIn("ghost_replay_id", body)
        self.assertIn("track_revision", body)
        self.assertIn("input_schema", body)
        self.assertIn("compatibility", body)
        self.assertNotIn("If the ghost clips geometry after a patch, drop it", body)

    def test_grapple_has_latch_session_and_motion_owner(self):
        body = text("grapple-swing")
        self.assertIn("grapple_session_id", body)
        self.assertIn("latch_id", body)
        self.assertIn("motion owner", body)
        self.assertIn("release request", body)
        self.assertNotIn("Release lands on nav", body)

    def test_fov_comfort_has_stable_profile_and_projection_evidence(self):
        body = text("fov-comfort")
        self.assertIn("comfort_profile_id", body)
        self.assertIn("projection convention", body)
        self.assertIn("settings-persist", body)
        self.assertIn("gameplay trace", body)


if __name__ == "__main__":
    unittest.main()
