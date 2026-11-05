"""Run the skin-weights fixtures and both repository cases in normal CI."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/2d/skin-weights/scripts'))
from test_skin_weights import (AnatomyTests, IdleTests, LintTests, MeshTests, MotionQATests, PoseTests,  # noqa: E402,F401
                               RenderTests, SolverTests)


class SkinWeightsCaseTests(unittest.TestCase):
    def test_pelican_bicycle_reproduces_pass_and_rejects_rigid_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, ROOT / 'examples/pelican-bicycle/run.py', '--out', tmp, '--no-render'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])
            summary = json.loads((Path(tmp) / 'summary.json').read_text())
            self.assertEqual(summary['harmonic']['visibleFoldPixels'], {})
            self.assertTrue(summary['nearest']['visibleFoldPixels'])
            self.assertLess(summary['harmonic']['maxContactGap'], 1e-6)

    def test_whole_figure_idle_passes_and_rejects_both_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, ROOT / 'examples/whole-figure-idle/run.py', '--out', tmp, '--no-render'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])
            summary = json.loads((Path(tmp) / 'summary.json').read_text())
            self.assertEqual(summary['anatomy']['neckSource'], 'bottleneck')
            self.assertEqual((summary['lint'], summary['audit'], summary['motionQA']['status']), ('PASS', 'PASS', 'PASS'))
            self.assertEqual(summary['controls'], {'fractionalBreaths': 'REFUSED', 'jitteredHead': 'FAIL'})

    def test_arm_harmonic_case_passes_the_spine_skeletal_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, ROOT / 'examples/weighted-skinning/harmonic_case.py', '--out', tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])
            self.assertEqual(json.loads(result.stdout)['visibleFoldPixels'], 0)


if __name__ == '__main__':
    unittest.main()
