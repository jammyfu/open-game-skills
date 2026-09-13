from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def text(path):
    return (SKILLS / path / "SKILL.md").read_text(encoding="utf-8")


class FinalOwnershipContractTests(unittest.TestCase):
    def test_root_and_router_delegate_to_single_dispatcher_owner(self):
        root = text(Path("."))
        router = text(Path("router"))
        self.assertIn("dispatcher", root)
        self.assertIn("pack entry point, not a second dispatcher", root)
        self.assertIn("compatibility alias", router)
        self.assertIn("single routing-policy owner", router)
        self.assertIn("same USE / ENGINE / ASK / DEFER decision", router)

    def test_genre_route_is_advisory_not_authoritative(self):
        body = text(Path("disciplines/genre-route"))
        self.assertIn("heuristic hint layer", body)
        self.assertIn("Existing project architecture", body)
        self.assertIn("dispatcher", body)
        self.assertIn("final bounded USE / ENGINE / ASK / DEFER decision", body)

    def test_tactics_stealth_composes_domain_owners(self):
        body = text(Path("disciplines/tactics-stealth"))
        self.assertIn("stealth_scenario_id", body)
        self.assertIn("plan-queue", body)
        self.assertIn("does not redefine sight/hearing truth", body)
        self.assertIn("not required to start on the same logical tick", body)

    def test_ad_break_has_stable_lifecycle_and_idempotent_reward_handoff(self):
        body = text(Path("disciplines/ad-break"))
        self.assertIn("ad_session_id", body)
        self.assertIn("placement-policy revision", body)
        self.assertIn("Duplicate provider callbacks cannot duplicate the grant", body)
        self.assertIn("Unavailable or cancelled ads", body)

    def test_analytics_funnel_versions_steps_cohort_and_denominator(self):
        body = text(Path("disciplines/analytics-funnel"))
        self.assertIn("funnel_id", body)
        self.assertIn("denominator definition", body)
        self.assertIn("cohort / eligibility predicate", body)
        self.assertIn("correlation is not causal proof", body)
        self.assertIn("independent of ingestion order", body)

    def test_iap_offer_catalog_does_not_own_transaction_truth(self):
        body = text(Path("disciplines/iap-offers"))
        self.assertIn("offer_id", body)
        self.assertIn("catalog revision", body)
        self.assertIn("Platform/store APIs own transaction truth", body)
        self.assertIn("entitlement-grant", body)
        self.assertIn("Pending, cancelled, failed, deferred and successful", body)
        self.assertIn("Duplicate callbacks do not duplicate ownership", body)


if __name__ == "__main__":
    unittest.main()
