"""Surface strain must catch changes that bone/area-only checks miss."""
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from measure_surface import stretches
class SurfaceTests(unittest.TestCase):
    def setUp(self):self.rest=np.array([[0.,0.],[1.,0.],[0.,1.]]);self.tri=np.array([[0,1,2]])
    def test_rigid_rotation_translation_preserves_surface(self):
        a=.7;r=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);s,d=stretches(self.rest,self.rest@r.T+[4,7],self.tri);np.testing.assert_allclose(s,1);np.testing.assert_allclose(d,1)
    def test_equal_area_anisotropy_is_not_rigid(self):
        s,d=stretches(self.rest,self.rest@np.diag([2,.5]),self.tri);np.testing.assert_allclose(d,1);np.testing.assert_allclose(s,[[2,.5]])
    def test_shear_is_measured_despite_unit_area(self):
        s,d=stretches(self.rest,self.rest@np.array([[1.,1.],[0.,1.]]),self.tri);np.testing.assert_allclose(d,1);self.assertGreater(s[0,0],1.6);self.assertLess(s[0,1],.62)
    def test_reflection_keeps_signed_area(self):
        s,d=stretches(self.rest,self.rest@np.diag([-1,1]),self.tri);np.testing.assert_allclose(s,1);np.testing.assert_allclose(d,-1)
    def test_collapsed_surface_is_measured(self):
        s,d=stretches(self.rest,self.rest@np.diag([1,.02]),self.tri);np.testing.assert_allclose(s,[[1,.02]]);np.testing.assert_allclose(d,.02)
    def test_report_is_measured_without_accepting_art(self):
        from test_audit_skin import AuditTests
        import json
        from measure_surface import measure
        fixture=AuditTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        path=fixture.root/'trace.json';path.write_text(json.dumps(fixture.data));r=measure(path)
        self.assertEqual(r['status'],'MEASURED-NOT-ACCEPTED');self.assertFalse(r['characterAccepted']);self.assertAlmostEqual(r['meshes']['body']['maximumPrincipalScale'],1)
    def test_declared_alpha_threshold_changes_visible_areas(self):
        from measure_surface import visible_areas
        alpha=np.full((8,8),100,dtype=np.uint8);uv=np.array([[0.,0.],[1.,0.],[0.,1.]])
        self.assertGreater(visible_areas(uv,self.tri,alpha,32).sum(),0);self.assertEqual(visible_areas(uv,self.tri,alpha,128).sum(),0)
    def test_bad_cli_input_writes_blocked_report(self):
        import tempfile,subprocess,json
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'bad.json').write_text('[]');out=root/'report.json'
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('measure_surface.py')),str(root/'bad.json'),'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2);self.assertEqual(json.loads(out.read_text())['status'],'BLOCKED');self.assertNotIn('Traceback',result.stderr)
if __name__=='__main__':unittest.main()

