"""Guard ownership, conservation, idempotency, and project-specific policy in economy skills."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class EconomyProgressionOwnershipTests(unittest.TestCase):
    NAMES = (
        'inventory-economy', 'equipment-progression', 'durability-economy',
        'crafting-loop', 'loot-roll', 'currency-dual', 'shop-price',
        'pity-table', 'season-track', 'game-monetization',
    )

    def _text(self, name):
        return (ROOT / f'skills/disciplines/{name}/SKILL.md').read_text(encoding='utf-8')

    def test_descriptions_are_trigger_only(self):
        for name in self.NAMES:
            with self.subTest(skill=name):
                front = self._text(name).split('---', 2)[1]
                desc = yaml.safe_load(front)['description']
                self.assertTrue(desc.strip().lower().startswith('use when '), desc)

    def test_inventory_does_not_force_discard_pressure_or_combat_hotbar(self):
        text = self._text('inventory-economy').lower()
        self.assertNotIn('discard is a real choice', text)
        self.assertNotIn('hotbar ≤ what fingers can hit in combat', text)
        self.assertIn('overflow', text)
        self.assertIn('stable', text)

    def test_equipment_progression_does_not_force_specific_tier_or_endgame_laws(self):
        text = self._text('equipment-progression').lower()
        self.assertNotIn('set bonuses open at mid-tier or full set, never at +0', text)
        self.assertNotIn('the starter item in a replace slot cannot finish the game', text)
        self.assertIn('stable', text)
        self.assertIn('inventory-economy', text)

    def test_durability_is_project_policy_not_mass_or_replacement_formula(self):
        text = self._text('durability-economy').lower()
        self.assertNotIn('standard fight must drop', text)
        self.assertNotIn('combat swap ≤ 1s', text)
        self.assertNotIn('air, grass, and missed swings are 0', text)
        self.assertIn('project', text)
        self.assertIn('transaction', text)

    def test_crafting_owns_transform_and_atomic_resource_transaction(self):
        text = self._text('crafting-loop').lower()
        self.assertNotIn('if the player cannot name the gather step, the craft is a shop with extra clicks', text)
        self.assertNotIn('no recipe that only works on one named quest prop', text)
        self.assertIn('transaction', text)
        self.assertIn('idempot', text)
        self.assertIn('inventory-economy', text)

    def test_loot_roll_has_stable_table_identity_and_does_not_assume_ten_kills(self):
        text = self._text('loot-roll').lower()
        self.assertNotIn('after ten kills', text)
        self.assertIn('stable', text)
        self.assertIn('rng-seed', text)
        self.assertIn('pity-table', text)

    def test_currency_wallets_use_ledger_identity_not_universal_sink_law(self):
        text = self._text('currency-dual').lower()
        self.assertNotIn('infinite soft with no sink is a bug', text)
        self.assertIn('ledger', text)
        self.assertIn('idempot', text)
        self.assertIn('entitlement-grant', text)

    def test_shop_price_does_not_force_finding_to_be_cheaper_than_buying(self):
        text = self._text('shop-price').lower()
        self.assertNotIn('must cost more time than finding it', text)
        self.assertIn('price', text)
        self.assertIn('currency-dual', text)
        self.assertIn('entitlement-grant', text)

    def test_pity_table_owns_counter_state_and_pool_identity(self):
        text = self._text('pity-table').lower()
        self.assertIn('stable', text)
        self.assertIn('counter', text)
        self.assertIn('pool', text)
        self.assertIn('transaction', text)

    def test_season_track_separates_track_state_from_entitlements_and_gameplay_rules(self):
        text = self._text('season-track').lower()
        self.assertIn('season', text)
        self.assertIn('entitlement-grant', text)
        self.assertIn('stable', text)
        self.assertNotIn('cosmetics default', text)

    def test_monetization_does_not_author_combat_or_claim_business_outcomes(self):
        text = self._text('game-monetization').lower()
        self.assertIn('action-feel', text)
        self.assertIn('entitlement-grant', text)
        self.assertIn('restore-purchase', text)
        self.assertIn('does not', text)
        self.assertIn('revenue', text)


if __name__ == '__main__':
    unittest.main()
