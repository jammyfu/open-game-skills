"""Executable matcher checks; not LLM or game-engine evaluations."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'skills/assets/open-asset-fixture'
SCRIPT = PACK / 'scripts/asset_fixture.py'


def module():
    spec = importlib.util.spec_from_file_location('asset_fixture', SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class AssetSelectionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'missing executable asset matcher')
        self.m = module()
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')

    def match(self, **kwargs):
        return self.m.match_assets(self.catalog, kwargs)

    def test_curated_catalog_has_primary_evidence_and_all_requested_categories(self):
        assets = self.catalog['assets']
        self.assertGreaterEqual(len(assets), 16)
        self.assertTrue({'sprite','model','animation','sfx','music','vfx','texture','hdri','ui'}.issubset({k for a in assets for k in a['kinds']}))
        self.assertTrue(all(a['source_url'].startswith('https://') and a['license_evidence_url'].startswith('https://') for a in assets))

    def test_smoke_particles_match_in_chinese_without_returning_audio(self):
        r = self.match(kinds=['vfx'], query='烟雾爆炸粒子')
        self.assertEqual(r['matches'][0]['id'], 'kenney-smoke-particles')
        self.assertTrue(all('vfx' in a['kinds'] for a in r['matches']))

    def test_skeletal_requirement_excludes_static_models(self):
        r = self.match(kinds=['model','animation'], requires=['skeletal-animation'])
        self.assertTrue(r['matches'])
        self.assertTrue(all('skeletal-animation' in a['capabilities'] for a in r['matches']))
        self.assertNotIn('kenney-nature-kit', [a['id'] for a in r['matches']])

    def test_static_format_cannot_inherit_animation_from_other_pack_files(self):
        r=self.match(kinds=['animation'],requires=['skeletal-animation'],formats=['obj'])
        self.assertEqual(r['status'],'unmatched')
        r=self.match(kinds=['animation'],requires=['skeletal-animation'],formats=['gltf'])
        self.assertTrue(r['matches'])

    def test_capability_format_matrix_references_real_formats(self):
        c=deepcopy(self.catalog)
        c['assets'][0]['capability_formats']={'skeletal-animation':['unknown']}
        with self.assertRaises(ValueError): self.m.validate_catalog(c)

    def test_format_unknown_is_not_assumed_compatible(self):
        r = self.match(kinds=['sfx'], formats=['blend'])
        self.assertEqual(r['status'], 'unmatched')
        self.assertFalse(r['matches'])

    def test_missing_required_capability_is_not_silently_relaxed(self):
        r = self.match(kinds=['model'], requires=['four-armed-rig'])
        self.assertEqual(r['status'], 'unmatched')
        self.assertIn('required-capability', r['rejected'][0]['reasons'])

    def test_cc_by_is_explicit_opt_in(self):
        req = dict(kinds=['ui'], requires=['vector-icon'])
        self.assertFalse(self.match(**req)['matches'])
        r = self.match(**req, allow_attribution=True)
        self.assertTrue(r['matches'])
        self.assertTrue(r['matches'][0]['attribution_required'])
        self.assertIn('Lorc', r['matches'][0]['credit'])

    def test_restrictive_unknown_and_paid_assets_are_filtered(self):
        for license_id, cost in [('CC-BY-NC-4.0','free'), ('CC-BY-SA-4.0','free'), ('unknown','free'), ('MIT','free'), ('CC0-1.0','paid')]:
            c = deepcopy(self.catalog)
            c['assets'] = [deepcopy(c['assets'][0])]
            c['assets'][0].update(license=license_id, cost=cost)
            r = self.m.match_assets(c, {'kinds': c['assets'][0]['kinds'], 'allow_attribution':True})
            self.assertFalse(r['matches'], (license_id,cost))

    def test_boolean_strings_are_not_truthy_policy_optins(self):
        with self.assertRaises(ValueError):
            self.match(kinds=['ui'], allow_attribution='false')

    def test_unknown_fields_and_empty_requests_are_rejected(self):
        for req in [{}, {'kinds':[]}, {'kinds':['model'],'require':['rigged']}, {'kinds':'model'}, {'kinds':['unknown']}, {'kinds':['model'],'limit':True}, {'kinds':['model'],'limit':0}]:
            with self.subTest(req=req), self.assertRaises(ValueError):
                self.m.match_assets(self.catalog, req)

    def test_same_rank_is_independent_of_registry_order(self):
        c = deepcopy(self.catalog)
        c['assets'].reverse()
        req = {'kinds':['model'], 'query':'low poly', 'limit':20}
        self.assertEqual(self.m.match_assets(c,req), self.m.match_assets(self.catalog,req))

    def test_unknown_style_does_not_become_a_hard_constraint(self):
        r = self.match(kinds=['sprite'], query='unusual visual style')
        self.assertTrue(r['matches'])
        self.assertEqual(r['runtime_validation'], 'not-run')
        self.assertTrue(all(a['status'] == 'candidate-needs-file-inspection' for a in r['matches']))

    def test_requirements_have_provenance_and_no_guessed_engine_support(self):
        r = self.match(kinds=['animation'], requires=['skeletal-animation'])
        for a in r['matches']:
            self.assertIn('inspection', a)
            self.assertNotIn('engine_verified', a)
            self.assertIn('source_url', a)

    def test_free_animation_edition_is_standard_only(self):
        a = next(a for a in self.catalog['assets'] if a['id']=='quaternius-animation-standard')
        self.assertEqual(a['edition'], 'Standard')
        self.assertNotIn('blend', a['formats'])
        self.assertIn('subset', a['inspection'])

    def test_skill_profiles_do_not_force_visual_assets_for_logic_tests(self):
        self.assertEqual(self.m.plan_for_skill(self.catalog,'rng-seed')['status'], 'not-needed')
        self.assertEqual(self.m.plan_for_skill(self.catalog,'made-up-skill')['status'], 'needs-requirements')
        plan = self.m.plan_for_skill(self.catalog,'materials')
        self.assertEqual({r['role'] for r in plan['roles']}, {'surface','lighting'})
        self.assertTrue(all(r['selection']['matches'] for r in plan['roles']))

    def test_animation_profile_requires_skeletal_animation(self):
        plan = self.m.plan_for_skill(self.catalog, 'animation-blend')
        self.assertEqual(plan['roles'][0]['request']['requires'], ['skeletal-animation'])

    def test_duplicate_catalog_ids_and_non_https_evidence_rejected(self):
        for mutation in ['duplicate','http']:
            c = deepcopy(self.catalog)
            if mutation=='duplicate': c['assets'].append(c['assets'][0])
            else: c['assets'][0]['license_evidence_url']='http://example.com/'
            with tempfile.TemporaryDirectory() as t:
                p=Path(t)/'catalog.json'; p.write_text(json.dumps(c),encoding='utf-8')
                with self.assertRaises(ValueError): self.m.load_catalog(p)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.json'; p.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError): self.m.read_json(p)

    def test_cli_works_from_another_directory_and_returns_unmatched_nonzero(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'request.json'; p.write_text(json.dumps({'kinds':['model'],'requires':['impossible-rig']}))
            r=subprocess.run([sys.executable,str(SCRIPT),'match','--request',str(p)],cwd=t,capture_output=True,text=True)
            self.assertEqual(r.returncode,2,r.stderr)
            self.assertEqual(json.loads(r.stdout)['status'],'unmatched')
            r=subprocess.run([sys.executable,str(SCRIPT),'plan','--skill','audio-feel'],cwd=t,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)


if __name__ == '__main__':
    unittest.main()
