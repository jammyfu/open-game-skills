from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "skills" / "disciplines"


def read(name):
    return (D / name / "SKILL.md").read_text(encoding="utf-8")


class WorldNavigationContractTests(unittest.TestCase):
    def test_nav_mesh_is_revisioned_and_capability_based(self):
        text = read("nav-mesh")
        for token in ("agent_profile_id", "nav_revision", "request_id", "authored traversal links"):
            self.assertIn(token, text)
        self.assertIn("does not universally require a full rebuild", text)
        self.assertIn("Do not globally mark all jump gaps unreachable", text)

    def test_hazards_have_stable_effect_identity(self):
        text = read("hazard-volume")
        for token in ("hazard_id", "enter/stay/exit", "at-most-once"):
            self.assertIn(token, text)
        self.assertIn("Decorative art is not the oracle", text)

    def test_world_map_consumes_truth_and_has_stable_ids(self):
        text = read("world-map")
        for token in ("region_id", "marker_id", "source_owner", "visibility_predicate"):
            self.assertIn(token, text)
        self.assertIn("project parameters, not fixed values", text)
        self.assertIn("must not mutate the underlying quest", text)

    def test_minimap_consumes_authorized_sources(self):
        text = read("minimap-pins")
        for token in ("pin_id", "source_owner", "visibility predicate/revision"):
            self.assertIn(token, text)
        self.assertIn("no universal rule that only one active quest hook may be shown", text)
        self.assertIn("Turning the minimap off removes presentation only", text)

    def test_ability_gate_uses_stable_predicates(self):
        text = read("ability-gate")
        for token in ("gate_id", "predicate version", "idempotent"):
            self.assertIn(token, text)
        self.assertIn("Soft-lock policy is project-specific", text)
        self.assertIn("does not own tutorials, map pins, save storage or rest-site placement", text)

    def test_adventure_tool_keeps_domain_owners(self):
        text = read("adventure-tool")
        for token in ("tool_action_id", "target capability", "interruption/cancel policy"):
            self.assertIn(token, text)
        self.assertIn("Those are project design choices", text)
        self.assertIn("remains owned by its dedicated system", text)

    def test_interact_prompt_consumes_resolver_priority(self):
        text = read("interact-prompt")
        for token in ("target_id", "action_id", "source resolver revision"):
            self.assertIn(token, text)
        self.assertIn("project's authored priority/tie-break", text)
        self.assertIn("showing a prompt never commits it", text)

    def test_rest_site_is_atomic_and_repopulation_is_data(self):
        text = read("rest-site")
        for token in ("site_id", "rest_txn_id", "commit boundary", "idempotent"):
            self.assertIn(token, text)
        self.assertIn("Repopulation is explicit data", text)
        self.assertIn("interrupted before commit", text)

    def test_vehicle_exit_uses_project_safe_surface(self):
        text = read("vehicle-mount")
        for token in ("vehicle_id", "mount_session_id", "safe-exit query policy"):
            self.assertIn(token, text)
        self.assertIn("not universally navmesh", text)
        self.assertIn("Exactly one authority controls rider locomotion", text)

    def test_fall_resolution_is_single_owner_and_versioned(self):
        text = read("fall-rules")
        for token in ("fall_event_id", "selected cost rule/version", "commits at most once"):
            self.assertIn(token, text)
        self.assertIn("project/accessibility design choices", text)
        self.assertIn("delegates to `landing-lag`", text)


if __name__ == "__main__":
    unittest.main()
