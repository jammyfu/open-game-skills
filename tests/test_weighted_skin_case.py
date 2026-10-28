import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'examples/weighted-skinning'
spec=importlib.util.spec_from_file_location('weighted_skin_case',HERE/'run.py');case=importlib.util.module_from_spec(spec);spec.loader.exec_module(case)

class WeightedSkinCaseTests(unittest.TestCase):
    def test_actual_runtime_traces_reproduce_opposite_outcomes(self):
        with tempfile.TemporaryDirectory() as temp:
            report=case.run(temp)
        self.assertEqual(report['cases']['current']['actual'],'PASS')
        self.assertEqual(report['cases']['narrow']['actual'],'FAIL')
        self.assertEqual(report['cases']['current']['visibleBadUVPixels'],0)
        self.assertEqual(report['cases']['narrow']['visibleBadUVPixels'],2529)
        self.assertEqual(report['cases']['current']['samples'],121)

    def test_case_is_portable_and_has_no_private_machine_paths(self):
        for name in ['current','narrow']:
            raw=gzip.decompress((HERE/'cases'/(name+'.trace.json.gz')).read_bytes()).decode()
            self.assertNotIn('/Users/',raw);self.assertNotIn('yuyu-md-remake',raw)
            data=json.loads(raw);self.assertEqual(data['meshes']['arm']['image'],'arm-setup.png')
            self.assertFalse(data['provenance']['fullCharacterAccepted'])

    def test_showcase_is_self_contained(self):
        demo=ROOT/'docs/demos/weighted-skinning'
        for name in ['index.html','demo.js','arm-setup.png','current.model.json','narrow.model.json','ink-triangles.json','preview.gif','THIRD-PARTY-NOTICES.txt']:
            self.assertTrue((demo/name).is_file(),name)
        self.assertNotIn('https://cdn.',(demo/'index.html').read_text())

    def test_published_case_and_bundle_match_their_sources(self):
        for manifest in [HERE/'case-manifest.json',ROOT/'docs/demos/weighted-skinning/bundle-manifest.json']:
            data=json.loads(manifest.read_text())
            for name,expected in data['files'].items():
                self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),expected,name)

    def test_public_resources_have_portable_texture_paths(self):
        demo=ROOT/'docs/demos/weighted-skinning'
        for path in demo.iterdir():
            if path.suffix in {'.json','.js','.html','.txt'}:
                content=path.read_text()
                self.assertNotIn('/Users/',content,path.name)
                self.assertNotIn('/home/',content,path.name)
                self.assertNotIn('yuyu-md-remake',content,path.name)
        for name in ['current','narrow']:
            model=json.loads((demo/(name+'.model.json')).read_text())
            self.assertTrue(all(image['page']=='arm-setup.png' for image in model['images']))

if __name__=='__main__':unittest.main()
