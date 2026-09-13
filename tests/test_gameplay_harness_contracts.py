from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "disciplines" / "gameplay-harness" / "SKILL.md"


class GameplayHarnessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_harness_owns_driving_not_validation_claims(self):
        self.assertIn("`gameplay-validation`", self.text)
        self.assertIn("evidence/claim taxonomy", self.text)
        self.assertIn("Driver mode is execution metadata, not a claim.", self.text)
        self.assertNotIn("| Column | Driver | Cheats | May prove |", self.text)

    def test_harness_uses_project_clock_not_a_universal_tick(self):
        self.assertIn("simulation/update boundary", self.text)
        self.assertIn("existing", self.text)
        self.assertIn("Do not invent a 60 Hz clock.", self.text)
        self.assertIn("`advance_project_tick()`", self.text)
        self.assertIn("delta and substep policy come from the engine/project adapter", self.text)

    def test_tape_and_oracle_are_versioned_and_semantic(self):
        self.assertIn("versioned semantic JSONL tape", self.text)
        self.assertIn("Store semantic actions, not physical key codes.", self.text)
        self.assertIn("Versioned oracle", self.text)
        self.assertIn("Never auto-accept a mismatch.", self.text)

    def test_session_report_has_stable_provenance(self):
        for token in (
            '"session_id"',
            '"build"',
            '"harness_version"',
            '"adapter_version"',
            '"driver_mode"',
            '"validation_mode"',
            '"seed"',
            '"save_id"',
            '"oracle"',
        ):
            self.assertIn(token, self.text)

    def test_overrides_cannot_masquerade_as_clean_evidence(self):
        self.assertIn("teleport, force-phase, god mode", self.text)
        self.assertIn("classify the evidence through `gameplay-validation` as scripted", self.text)
        self.assertIn("A soak with gameplay overrides is not clean soak evidence.", self.text)

    def test_presentation_is_not_the_gameplay_oracle(self):
        self.assertIn("Camera, animation pose, audio, haptics, particles, and juice", self.text)
        self.assertIn("they do not decide gameplay pass/fail", self.text)
        self.assertIn("demo's current runtime implementation is not an oracle", self.text)


if __name__ == "__main__":
    unittest.main()
