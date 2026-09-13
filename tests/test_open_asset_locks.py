"""Local integrity tests use synthetic bytes, not downloaded or decoded game assets."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'skills/assets/open-asset-fixture'
SCRIPT = PACK / 'scripts/fixture_lock.py'


class FixtureLockTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'missing local fixture integrity tool')
        spec = importlib.util.spec_from_file_location('fixture_lock', SCRIPT)
        self.m = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT.parent))
        try:
            spec.loader.exec_module(self.m)
        finally:
            sys.path.pop(0)
        self.catalog = self.m.load_catalog(PACK / 'assets/catalog.json')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'sample.png').write_bytes(b'synthetic fixture bytes - not a real image')
        (self.root/'LICENSE.txt').write_text('Synthetic evidence for an integrity unit test; not a license opinion.')
        self.request = {'asset_id':'kenney-smoke-particles',
                        'acquired_from':'https://kenney.nl/assets/smoke-particles',
                        'files':['sample.png'], 'license_file':'LICENSE.txt',
                        'properties':{'kinds':['vfx'], 'capabilities':['particle-texture'], 'formats':['png']},
                        'inspection_note':'Synthetic hash-unit-test input only; no decode/engine test.'}

    def pin(self):
        return self.m.make_lock(self.catalog, self.root, self.request)

    def test_pin_hashes_files_and_license_without_runtime_claim(self):
        lock = self.pin()
        self.assertEqual(len(lock['files'][0]['sha256']), 64)
        self.assertEqual(len(lock['license_evidence']['sha256']), 64)
        self.assertEqual(lock['runtime_validation'], 'not-run')
        r = self.m.verify_lock(self.catalog, self.root, lock)
        self.assertEqual(r['status'], 'integrity-verified')
        self.assertIn('not authenticity', r['scope'])

    def test_changed_asset_and_license_are_detected(self):
        for name in ['sample.png','LICENSE.txt']:
            lock = self.pin()
            p = self.root/name; original = p.read_bytes(); p.write_bytes(original+b' changed')
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.m.verify_lock(self.catalog,self.root,lock)
            p.write_bytes(original)

    def test_deleted_file_fails_verification(self):
        lock = self.pin(); (self.root/'sample.png').unlink()
        with self.assertRaises(ValueError): self.m.verify_lock(self.catalog,self.root,lock)

    def test_missing_empty_or_executable_data_rejected(self):
        for name, data in [('empty.png',b''), ('code.py',b'print(1)'), ('font.ttf',b'font'), ('pack.zip',b'zip')]:
            (self.root/name).write_bytes(data)
            req=deepcopy(self.request); req['files']=[name]
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.m.make_lock(self.catalog,self.root,req)

    def test_traversal_absolute_and_windows_paths_rejected(self):
        for name in ['../sample.png','/tmp/sample.png','C:\\sample.png','a\\sample.png','a/../sample.png','sample.png\n']:
            req=deepcopy(self.request);req['files']=[name]
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.m.make_lock(self.catalog,self.root,req)

    def test_symlink_file_and_symlink_directory_rejected(self):
        (self.root/'alias.png').symlink_to(self.root/'sample.png')
        (self.root/'nested').symlink_to(self.root,target_is_directory=True)
        for name in ['alias.png','nested/sample.png']:
            req=deepcopy(self.request);req['files']=[name]
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.m.make_lock(self.catalog,self.root,req)

    def test_duplicate_paths_and_oversized_inputs_rejected(self):
        req=deepcopy(self.request);req['files']*=2
        with self.assertRaises(ValueError): self.m.make_lock(self.catalog,self.root,req)
        with self.assertRaises(ValueError): self.m.make_lock(self.catalog,self.root,self.request,max_bytes=4)

    def test_changed_catalog_record_invalidates_lock_but_unrelated_record_does_not(self):
        lock=self.pin();c=deepcopy(self.catalog)
        next(a for a in c['assets'] if a['id']==lock['asset_id'])['edition']='new-edition'
        with self.assertRaises(ValueError): self.m.verify_lock(c,self.root,lock)
        c=deepcopy(self.catalog);c['assets'][0]['inspection']+=' revised'
        self.assertEqual(self.m.verify_lock(c,self.root,lock)['status'],'integrity-verified')

    def test_properties_require_file_inspection_not_pack_inference(self):
        for key in ['properties','inspection_note']:
            req=deepcopy(self.request);del req[key]
            with self.assertRaises(ValueError): self.m.make_lock(self.catalog,self.root,req)
        req=deepcopy(self.request);req['properties']['formats']=['fbx']
        with self.assertRaises(ValueError): self.m.make_lock(self.catalog,self.root,req)

    def test_ccby_requires_optin_even_for_local_lock(self):
        req=deepcopy(self.request);req['asset_id']='gameicons-heart-bottle'
        req['properties']={'kinds':['ui'],'capabilities':['vector-icon'],'formats':['png']}
        with self.assertRaises(ValueError): self.m.make_lock(self.catalog,self.root,req)
        lock=self.m.make_lock(self.catalog,self.root,req,allow_attribution=True)
        self.assertIn('Lorc',lock['credit'])
        with self.assertRaises(ValueError): self.m.verify_lock(self.catalog,self.root,lock)
        self.assertEqual(self.m.verify_lock(self.catalog,self.root,lock,allow_attribution=True)['status'],'integrity-verified')

    def test_empty_or_forged_lock_shapes_rejected(self):
        lock=self.pin()
        for key,value in [('files',[]),('schema_version',True),('runtime_validation','pass'),('metadata_sha256','0'*64)]:
            bad=deepcopy(lock);bad[key]=value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.m.verify_lock(self.catalog,self.root,bad)

    def test_exclusive_write_never_overwrites(self):
        p=self.root/'lock.json'; self.m.write_lock(p,self.pin())
        before=p.read_bytes()
        with self.assertRaises(FileExistsError): self.m.write_lock(p,self.pin())
        self.assertEqual(before,p.read_bytes())

    def test_verified_local_is_preferred_and_corrupt_lock_is_not_reused(self):
        p=self.root/'lock.json';self.m.write_lock(p,self.pin())
        req={'kinds':['vfx'],'requires':['particle-texture'],'query':'explosion'}
        r=self.m.select_assets(self.catalog,self.root,[p],req)
        self.assertEqual(r['matches'][0]['status'],'local-integrity-verified')
        (self.root/'sample.png').write_bytes(b'changed')
        r=self.m.select_assets(self.catalog,self.root,[p],req,pinned_only=True)
        self.assertEqual(r['status'],'unmatched')
        self.assertTrue(r['invalid_locks'])

    def test_local_format_and_capability_filters_use_inspected_file_properties(self):
        p=self.root/'lock.json';self.m.write_lock(p,self.pin())
        r=self.m.select_assets(self.catalog,self.root,[p],{'kinds':['vfx'],'formats':['png']},pinned_only=True)
        self.assertEqual(len(r['matches']),1)
        r=self.m.select_assets(self.catalog,self.root,[p],{'kinds':['animation'],'requires':['skeletal-animation']},pinned_only=True)
        self.assertEqual(r['status'],'unmatched')

    def test_local_selection_is_order_independent_and_deduplicates_locks(self):
        p=self.root/'lock.json';self.m.write_lock(p,self.pin())
        req={'kinds':['vfx'],'limit':20}
        self.assertEqual(self.m.select_assets(self.catalog,self.root,[p,p],req),self.m.select_assets(self.catalog,self.root,[p],req))


    def test_mixed_formats_cannot_borrow_skeletal_capability(self):
        for name in ['static.obj', 'animated.glb']:
            (self.root/name).write_bytes(b'Synthetic hash test, not a 3D model')
        req=deepcopy(self.request)
        req['asset_id']='quaternius-monsters'
        req['files']=['static.obj','animated.glb']
        req['properties']={'kinds':['animation','model'],'capabilities':['skeletal-animation'],'formats':['obj','glb']}
        path=self.root/'mixed.lock.json'
        self.m.write_lock(path,self.m.make_lock(self.catalog,self.root,req))
        result=self.m.select_assets(self.catalog,self.root,[path],{'kinds':['animation'],'requires':['skeletal-animation'],'formats':['obj']},pinned_only=True)
        self.assertEqual(result['status'],'unmatched', 'an animation in another format must not qualify OBJ')

    def test_explicit_capability_format_mapping_matches_only_inspected_variant(self):
        for name in ['static.obj', 'animated.glb']:
            (self.root/name).write_bytes(b'Synthetic hash test, not a 3D model')
        req=deepcopy(self.request)
        req['asset_id']='quaternius-monsters'
        req['files']=['static.obj','animated.glb']
        req['properties']={'kinds':['animation','model'],'capabilities':['skeletal-animation'],'formats':['obj','glb'],
                           'capability_formats':{'skeletal-animation':['glb']}}
        # Fail with an assertion rather than an import/schema error on the old implementation.
        try:
            lock=self.m.make_lock(self.catalog,self.root,req)
        except ValueError as exc:
            self.fail(f'inspected format/capability binding is unsupported: {exc}')
        path=self.root/'bound.lock.json';self.m.write_lock(path,lock)
        for fmt,status in [('obj','unmatched'),('glb','matched')]:
            result=self.m.select_assets(self.catalog,self.root,[path],{'kinds':['animation'],'requires':['skeletal-animation'],'formats':[fmt]},pinned_only=True)
            self.assertEqual(result['status'],status)

    def test_local_matches_use_relevance_not_just_alphabetical_pack_id(self):
        paths=[]
        for asset_id in ['kenney-particle-pack','kenney-smoke-particles']:
            req=deepcopy(self.request);req['asset_id']=asset_id
            p=self.root/(asset_id+'.json');paths.append(p)
            self.m.write_lock(p,self.m.make_lock(self.catalog,self.root,req))
        result=self.m.select_assets(self.catalog,self.root,paths,{'kinds':['vfx'],'query':'smoke explosion','limit':1},pinned_only=True)
        self.assertEqual(result['matches'][0]['id'],'kenney-smoke-particles')


if __name__ == '__main__': unittest.main()
