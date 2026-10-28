"""Behavioral fixtures: visible defects must fail, invisible canvas folds may pass."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from audit_skin import audit


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Image.new('RGBA', (16, 16), (220, 150, 70, 255)).save(self.root/'source.png')
        bones = {'root': dict(a=1,b=0,c=0,d=1,x=0,y=0),
                 'tip': dict(a=1,b=0,c=0,d=1,x=1,y=0)}
        vertices = [0,1,1,1,1,0,0,0]
        self.data = dict(schema='ogs.skin-trace/1', sampleRate=2,
            tolerances=dict(length=1e-5,scale=1e-6,loop=1e-5,weights=1e-6,area=1e-10,alphaThreshold=32),
            boneScales={'root':[1,1],'tip':[1,1]}, segments=[dict(a='root',b='tip',length=1)],
            meshes={'body':dict(image='source.png',sha256=self.digest(),uvs=[0,0,1,0,1,1,0,1],
                triangles=[0,1,2,0,2,3],setupVertices=vertices,
                weights=[[dict(bone='root',weight=1)] for _ in range(4)])},
            frames=[dict(t=i/2,bones=copy.deepcopy(bones),meshes={'body':vertices.copy()}) for i in range(3)],
            loops=[dict(first=0,last=2)],contacts=[dict(bone='root',first=0,last=2,target=[0,0],tolerance=0)])

    def digest(self):
        return hashlib.sha256((self.root/'source.png').read_bytes()).hexdigest()

    def run_audit(self):
        path=self.root/'trace.json';path.write_text(json.dumps(self.data))
        return audit(path)

    def test_valid_trace_is_technical_only(self):
        result=self.run_audit()
        self.assertEqual(result['technicalStatus'],'PASS')
        self.assertFalse(result['characterAccepted'])

    def test_visible_fold_fails_between_identical_endpoints(self):
        self.data['frames'][1]['meshes']['body']=[0,1,-1,1,-1,0,0,0]
        result=self.run_audit()
        self.assertEqual(result['technicalStatus'],'FAIL')
        self.assertGreater(result['meshes']['body']['visibleBadUVPixels'],0)

    def test_collapsed_visible_triangle_fails(self):
        self.data['frames'][1]['meshes']['body']=[0,0,1,0,2,0,3,0]
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_transparent_only_fold_is_counted_without_failing_ink(self):
        image=Image.new('RGBA',(16,16));image.paste((220,150,70,255),(0,0,6,16));image.save(self.root/'source.png')
        mesh=self.data['meshes']['body']
        mesh.update(sha256=self.digest(),uvs=[0,0,.3,0,.3,1,.7,0,1,0,1,1],
                    triangles=[0,1,2,3,4,5],setupVertices=[0,1,.3,1,.3,0,.7,1,1,1,1,0],
                    weights=[[dict(bone='root',weight=1)] for _ in range(6)])
        for frame in self.data['frames']:frame['meshes']['body']=mesh['setupVertices'].copy()
        self.data['frames'][1]['meshes']['body'][8]=.5
        result=self.run_audit()
        self.assertEqual(result['technicalStatus'],'PASS')
        self.assertEqual(result['meshes']['body']['badTriangles'],1)
        self.assertEqual(result['meshes']['body']['visibleBadUVPixels'],0)

    def test_weight_sum_fails(self):
        self.data['meshes']['body']['weights'][0][0]['weight']=.5
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_unknown_weight_bone_blocks(self):
        self.data['meshes']['body']['weights'][0][0]['bone']='absent'
        with self.assertRaisesRegex(ValueError,'unknown/duplicate'):self.run_audit()

    def test_length_drift_fails(self):
        self.data['frames'][1]['bones']['tip']['x']=1.1
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_scale_drift_fails(self):
        self.data['frames'][1]['bones']['root']['a']=1.1
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_unit_columns_with_shear_fail(self):
        self.data['frames'][1]['bones']['root'].update(b=.6,d=.8)
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_loop_drift_fails(self):
        self.data['frames'][2]['meshes']['body'][0]=.01
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_unused_bone_rotation_at_loop_endpoint_fails(self):
        self.data['frames'][2]['bones']['tip'].update(a=0,b=-1,c=1,d=0)
        result=self.run_audit()
        self.assertTrue(any('loop endpoint bone transform' in s for s in result['errors']))

    def test_single_frame_planted_contact_can_be_checked(self):
        self.data['contacts'][0].update(first=1,last=1)
        self.assertEqual(self.run_audit()['technicalStatus'],'PASS')

    def test_contact_drift_fails_even_with_constant_bone_lengths(self):
        for bone in self.data['frames'][1]['bones'].values():bone['y']+=.1
        result=self.run_audit()
        self.assertTrue(any('planted contact' in s for s in result['errors']))

    def test_sample_gap_fails(self):
        self.data['frames'][1]['t']=.1
        self.assertEqual(self.run_audit()['technicalStatus'],'FAIL')

    def test_source_identity_change_blocks(self):
        Image.new('RGBA',(16,16),(0,0,0,255)).save(self.root/'source.png')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.run_audit()

    def test_missing_pose_observation_blocks(self):
        del self.data['frames'][1]['bones']['tip']
        with self.assertRaisesRegex(ValueError,'bone observations'):self.run_audit()

    def test_rendered_loop_pixel_change_fails(self):
        Image.new('RGBA',(16,16),(0,0,0,255)).save(self.root/'first.png')
        image=Image.new('RGBA',(16,16),(0,0,0,255));image.putpixel((4,4),(1,0,0,255));image.save(self.root/'last.png')
        self.data['loops'][0].update(firstImage='first.png',lastImage='last.png')
        self.assertIn('Rendered loop endpoint pixels differ',self.run_audit()['errors'])

    def test_nan_is_blocked_and_cli_writes_report(self):
        self.data['frames'][1]['meshes']['body'][0]=float('nan')
        path=self.root/'trace.json';path.write_text(json.dumps(self.data))
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('audit_skin.py')),str(path),'--out',str(self.root/'report.json')],capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads((self.root/'report.json').read_text())['technicalStatus'],'BLOCKED')

    def test_non_object_root_is_blocked_with_report(self):
        path=self.root/'trace.json';path.write_text('[]')
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('audit_skin.py')),str(path),'--out',str(self.root/'report.json')],capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads((self.root/'report.json').read_text())['technicalStatus'],'BLOCKED')

    def test_oversized_json_integer_is_blocked_with_report(self):
        self.data['frames'][1]['bones']['root']['x']=10**400
        path=self.root/'trace.json';path.write_text(json.dumps(self.data))
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('audit_skin.py')),str(path),'--out',str(self.root/'report.json')],capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads((self.root/'report.json').read_text())['technicalStatus'],'BLOCKED')


if __name__=='__main__':unittest.main(verbosity=2)
