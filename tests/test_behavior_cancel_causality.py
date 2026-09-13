"""Cancel causality gate regressions; synthetic observations, not engine evidence."""
from copy import deepcopy
import unittest

from test_behavior_evidence_gate import load, valid_runtime


class CancelCausalityTests(unittest.TestCase):
    def setUp(self):
        self.gate = load('evidence_gate')
        self.runtime = valid_runtime()
        self.events = self.runtime['traces']['cancel-during-freeze']['events']
        self.cancel = next(e for e in self.events if e['type'] == 'cancel')
        self.fresh = [e for e in self.events if e['type'] == 'hit' and e['actor'] == 'A'][-1]

    def rejected(self):
        self.assertTrue(self.gate.evaluate_runtime(self.runtime),
                        'Malformed cancel causality must not receive a passing assessment')

    def test_valid_cancel_then_fresh_attack_remains_accepted(self):
        self.assertEqual(self.gate.evaluate_runtime(self.runtime), [])

    def test_hit_before_cancel_is_not_a_cancel_result(self):
        self.fresh['tick'] = 4
        self.rejected()

    def test_same_tick_hit_is_not_the_authored_two_tick_startup(self):
        self.fresh['tick'] = 7
        self.rejected()

    def test_late_unrelated_hit_is_not_the_authored_fresh_attack(self):
        self.fresh['tick'] = 90
        self.rejected()

    def test_wrong_victim_cannot_substitute_for_authored_contact(self):
        self.fresh.update(victim='C', id='cancel-a:C')
        self.rejected()

    def test_new_but_unrelated_attack_id_is_rejected(self):
        self.fresh['id'] = 'unrelated-attack:B'
        self.rejected()

    def test_wrong_cancelling_actor_is_rejected(self):
        self.cancel['actor'] = 'B'
        self.rejected()

    def test_cancel_command_identity_must_match_input_tape(self):
        self.cancel['id'] = 'unrelated-command'
        self.rejected()

    def test_fractional_tick_encoding_cannot_masquerade_as_integer(self):
        self.fresh['tick'] = 9.0
        self.rejected()

    def test_event_log_must_record_cancel_before_its_hit(self):
        self.events.remove(self.fresh)
        self.events.insert(0, self.fresh)
        self.rejected()

    def test_duplicate_cancel_still_rejected(self):
        self.events.append(deepcopy(self.cancel))
        self.rejected()

    def test_missing_fresh_hit_still_rejected(self):
        self.events.remove(self.fresh)
        self.rejected()


if __name__ == '__main__':
    unittest.main()
