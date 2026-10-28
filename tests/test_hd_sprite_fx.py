"""Synthetic FX fixtures test failures, not generation or artistic acceptance."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/2d/hd-sprite-sequence/scripts/validate_fx.py'
spec = importlib.util.spec_from_file_location('fxqa', SCRIPT)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)


class FXTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        im = Image.new('RGBA', (8, 8), (0, 0, 255, 0))
        ImageDraw.Draw(im).rectangle((0, 2, 3, 5), fill=(252, 72, 0, 255))
        im.save(self.root / 'native.png')
        im.resize((32, 32), Image.Resampling.NEAREST).save(self.root / 'hd.png')
        f = {'id': 'impact', 'image': 'native.png', 'sha256': h.digest(self.root / 'native.png'),
             'density': 1, 'frame': {'ax': 4, 'ay': 5, 'w': 8, 'h': 8}, 'durationTicks': 3}
        self.ref = {'schema': 'ogs.independent-fx/1', 'context': {'vflip': True}, 'frames': [f]}
        self.cand = copy.deepcopy(self.ref)
        self.cand['frames'][0].update(image='hd.png', density=4, sha256=h.digest(self.root / 'hd.png'))
        self.thresholds = {'alphaThreshold': 128, 'sampleDensity': 4,
                           'minSilhouetteIoU': .96, 'maxCentroidDrift': .25, 'maxPaletteDrift': 10}

    def run_case(self):
        for name, data in [('reference', self.ref), ('candidate', self.cand)]:
            (self.root / (name + '.json')).write_text(json.dumps(data))
        return h.validate(self.root / 'reference.json', self.root / 'candidate.json', self.thresholds)

    def mutate(self, callback):
        p = self.root / 'hd.png'; im = Image.open(p).convert('RGBA'); callback(im); im.save(p)
        self.cand['frames'][0]['sha256'] = h.digest(p)

    def codes(self):
        return {v['code'] for v in self.run_case()['issues']}

    def test_different_density_same_geometry_and_native_edge_contact_pass(self):
        r = self.run_case(); self.assertEqual(r['status'], 'pass', r)
        self.assertFalse(r['artAccepted']); self.assertEqual(r['metrics'][0]['silhouetteIoU'], 1)

    def test_shape_translation_fails_centroid_and_iou(self):
        self.mutate(lambda im: im.paste(im.copy(), (4, 0)))
        self.assertTrue({'silhouette', 'centroid'} <= self.codes())

    def test_palette_change_fails_even_with_same_alpha(self):
        self.mutate(lambda im: im.paste((0, 72, 252, 255), (0, 8, 16, 24)))
        self.assertIn('palette', self.codes()); self.assertNotIn('silhouette', self.codes())

    def test_timing_geometry_context_sha_fail_independently(self):
        f = self.cand['frames'][0]
        f['sha256'] = '0' * 64; f['durationTicks'] = 4; f['frame']['ax'] += 1
        self.cand['context']['vflip'] = False
        self.assertTrue({'sha256', 'durationTicks', 'frame', 'context', 'centroid'} <= self.codes())

    def test_unexpected_frame_checked_and_order_rejected(self):
        extra = copy.deepcopy(self.cand['frames'][0]); extra.update(id='extra', sha256='0'*64)
        self.cand['frames'].append(extra)
        self.assertTrue({'frame-order', 'sha256'} <= self.codes())

    def test_invisible_rgb_does_not_count_as_palette_or_silhouette(self):
        self.mutate(lambda im: im.putpixel((31, 31), (255, 0, 255, 0)))
        self.assertEqual(self.run_case()['status'], 'pass')

    def test_nonintegral_density_geometry_does_not_silently_resize(self):
        self.cand['frames'][0]['density'] = 3
        self.assertIn('image-geometry', self.codes())

    def test_thresholds_must_be_explicit_and_valid(self):
        del self.thresholds['maxPaletteDrift']
        with self.assertRaises(ValueError): self.run_case()

    def test_missing_candidate_and_empty_alpha_cannot_pass(self):
        self.mutate(lambda im: im.paste((0, 0, 0, 0), (0, 0, 32, 32)))
        self.assertTrue({'centroid', 'silhouette'} <= self.codes())


if __name__ == '__main__':
    unittest.main()
