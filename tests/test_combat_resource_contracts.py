"""Regression contracts for combat resources, statuses, swaps and interaction layers."""
from pathlib import Path
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'skills'/'disciplines'

class CombatResourceContracts(unittest.TestCase):
    NAMES=('collision-layers','combo-design','fighting-design','wakeup-oki','throw-tech','stamina-clock','super-meter','status-ailment','weapon-swap','ammo-reload')
    def text(self,n): return (D/n/'SKILL.md').read_text(encoding='utf-8')
    def test_descriptions_trigger_only(self):
        for n in self.NAMES:
            with self.subTest(skill=n):
                d=yaml.safe_load(self.text(n).split('---',2)[1])['description'].strip().lower()
                self.assertTrue(d.startswith('use when '),d)
    def test_collision_layers_publish_matrix_and_stable_categories(self):
        t=self.text('collision-layers').lower()
        for x in ('matrix','stable','hitbox-hurtbox','camera-anti-clip'):
            with self.subTest(token=x): self.assertIn(x,t)
    def test_combo_design_does_not_force_decay_or_ender(self):
        t=self.text('combo-design').lower()
        self.assertNotIn('damage falls off with length',t)
        self.assertNotIn('starter, confirm, ender',t)
        self.assertIn('action-feel',t); self.assertIn('hitstun-recover',t)
    def test_fighting_design_does_not_duplicate_hitstop_or_netcode_policy(self):
        t=self.text('fighting-design').lower()
        self.assertIn('netcode-feel',t); self.assertIn('action-feel',t)
        self.assertNotIn('hitstop freezes the two colliding actorclocks only',t)
        self.assertNotIn('prefer delay + rollback over lockstep',t)
        self.assertNotIn('a throw / grab answers shield or block',t)
    def test_wakeup_owns_options_not_universal_counter(self):
        t=self.text('wakeup-oki').lower()
        for x in ('option id','invulnerability','hitstun-recover'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('meaties lose to at least one rise option',t)
    def test_throw_contract_has_stable_attempt_identity(self):
        t=self.text('throw-tech').lower()
        for x in ('throw attempt id','eligibility','hitbox-hurtbox'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('a grab that cannot miss is a bug',t)
    def test_stamina_spend_is_idempotent_and_timebase_declared(self):
        t=self.text('stamina-clock').lower()
        for x in ('transaction','timebase','idempotent'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('still walk',t)
    def test_super_meter_is_resource_not_combo_only(self):
        t=self.text('super-meter').lower()
        for x in ('transaction','resource','combo-design'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('spending is a node on `combo-design`',t)
        self.assertNotIn('dodge-iframe` cousin',t)
    def test_status_effects_have_stack_policy_and_declared_timebase(self):
        t=self.text('status-ailment').lower()
        for x in ('status instance id','stack','timebase','cleanse'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('ticks use the logic clock',t)
    def test_weapon_swap_has_stable_weapon_state_and_no_audio_clock_ownership(self):
        t=self.text('weapon-swap').lower()
        for x in ('weapon id','interruption','socket'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('hud and audio swap on the same logic frame',t)
    def test_reload_uses_actions_not_fixed_keys_and_atomic_ammo_transfer(self):
        t=self.text('ammo-reload').lower()
        for x in ('reload transaction','input-design','atomic'):
            with self.subTest(token=x): self.assertIn(x,t)
        self.assertNotIn('interact and reload are different keys',t)

if __name__=='__main__': unittest.main()
