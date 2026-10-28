"""Executable fixtures for the skin-weights scripts (numpy + Pillow only)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lint_weights  # noqa: E402
import pose_trace  # noqa: E402
import solve_weights  # noqa: E402
from build_mesh import build  # noqa: E402
from skinlib import (SkinError, apply, build_grid_mesh, forward, load_mesh, load_rig, signed_areas,  # noqa: E402
                     write_json)

AUDIT = HERE.parents[1] / 'spine-skeletal/scripts/audit_skin.py'


def strip_fixture(root, spacing=6, inset=0.3, radius=3.0, gap_image=False):
    """A 40x8-unit limb (two 20-unit bones), 4 px per unit, with interior ink."""
    image = Image.new('RGBA', (164, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([2, 4, 161, 35], fill=(230, 160, 80, 255), outline=(30, 30, 30, 255), width=3)
    for x in range(10, 160, 12):
        draw.line([(x, 8), (x, 31)], fill=(90, 50, 30, 255), width=2)
    if gap_image:
        draw.rectangle([50, 0, 62, 39], fill=(0, 0, 0, 0))   # three islands; the middle one
        draw.rectangle([102, 0, 114, 39], fill=(0, 0, 0, 0))  # holds neither bone core
    image.save(root / 'limb.png')
    rig = {'schema': 'ogs.skin-rig/1', 'bones': [
        {'name': 'root'},
        {'name': 'upper', 'parent': 'root', 'x': 0, 'y': 0, 'rotation': 0, 'length': 20},
        {'name': 'lower', 'parent': 'upper', 'x': 20, 'y': 0, 'rotation': 0, 'length': 20}],
        'parts': [{'name': 'limb', 'image': 'limb.png', 'origin': [2, 20], 'at': [0, 0], 'density': 4,
                   'bones': ['upper', 'lower'], 'mesh': {'spacing': spacing, 'alphaThreshold': 32, 'margin': 2},
                   'weights': {'handleRadius': radius, 'coreInset': inset, 'maxInfluences': 2, 'pruneBelow': 0.01}}]}
    (root / 'rig.json').write_text(json.dumps(rig))
    return root / 'rig.json'


def pipeline(root, method='harmonic', **kw):
    rig = load_rig(strip_fixture(root, **kw))
    mesh_doc = build(rig)
    write_json(root / 'mesh.json', mesh_doc)
    mesh = load_mesh(root / 'mesh.json')
    weights, report = solve_weights.solve(rig, mesh, method)
    return rig, mesh, weights, report


class SolverTests(unittest.TestCase):
    def test_harmonic_weights_are_bounded_partition_of_unity_and_rigid_at_handles(self):
        with tempfile.TemporaryDirectory() as tmp:
            rig, mesh, weights, report = pipeline(Path(tmp))
            stats = report['limb']
            self.assertLess(stats['partitionOfUnityError'], 1e-9)
            self.assertGreaterEqual(stats['rawMin'], -1e-12)
            self.assertLessEqual(stats['rawMax'], 1 + 1e-9)
            rows = weights['parts']['limb']['weights']
            for row in rows:
                self.assertAlmostEqual(sum(i['weight'] for i in row), 1, places=9)
            for index in weights['parts']['limb']['handles']:
                self.assertEqual(len(rows[index]), 1)

    def test_transition_is_monotonic_along_the_limb(self):
        with tempfile.TemporaryDirectory() as tmp:
            rig, mesh, weights, _ = pipeline(Path(tmp))
            v = mesh['parts']['limb']['vertices']
            lower = np.array([sum(i['weight'] for i in r if i['bone'] == 'lower') for r in weights['parts']['limb']['weights']])
            centre = np.abs(v[:, 1]) < 0.5
            order = np.argsort(v[centre, 0])
            self.assertTrue(np.all(np.diff(lower[centre][order]) >= -1e-9))
            self.assertEqual(lower[v[:, 0] < 5].max(), 0)
            self.assertEqual(lower[v[:, 0] > 35].min(), 1)

    def test_asymmetric_inset_moves_the_transition_to_one_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig = load_rig(strip_fixture(root))
            rig['parts'][0]['weights']['coreInset'] = {'upper': [0.1, 0.4], 'lower': [0.02, 0.1]}
            write_json(root / 'mesh.json', build(rig))
            mesh = load_mesh(root / 'mesh.json')
            weights, _ = solve_weights.solve(rig, mesh)
            v = mesh['parts']['limb']['vertices']
            lower = np.array([sum(i['weight'] for i in r if i['bone'] == 'lower') for r in weights['parts']['limb']['weights']])
            self.assertEqual(lower[(v[:, 0] > 21.5) & (np.abs(v[:, 1]) <= 3)].min(), 1)  # rigid right after the joint, inside the handle tube
            self.assertGreater(lower[(v[:, 0] > 12.5) & (v[:, 0] < 19)].max(), 0)  # the bend lives on the upper side
            rig['parts'][0]['weights']['coreInset'] = {'upper': [0.6, 0.5], 'lower': 0.1}
            with self.assertRaises(SkinError):
                solve_weights.solve(rig, mesh)

    def test_bindings_reproduce_setup_vertices(self):
        with tempfile.TemporaryDirectory() as tmp:
            rig, mesh, weights, _ = pipeline(Path(tmp))
            world = forward(rig)
            posed = pose_trace.deform(weights['parts']['limb']['weights'], world)
            self.assertLess(np.abs(posed - mesh['parts']['limb']['vertices']).max(), 1e-5)

    def test_island_without_handle_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig = load_rig(strip_fixture(root, gap_image=True))
            rig['parts'][0]['weights']['coreInset'] = 0.45  # cores shrink into the far ends; middle islands stay handle-free
            rig['parts'][0]['weights']['handleRadius'] = 1.0
            write_json(root / 'mesh.json', build(rig))
            mesh = load_mesh(root / 'mesh.json')
            with self.assertRaises(SkinError):
                solve_weights.solve(rig, mesh)

    def test_missing_handle_radius_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig = load_rig(strip_fixture(root))
            rig['parts'][0]['weights'].pop('handleRadius')
            write_json(root / 'mesh.json', build(rig))
            with self.assertRaises(SkinError):
                solve_weights.solve(rig, load_mesh(root / 'mesh.json'))


class MeshTests(unittest.TestCase):
    def test_grid_mesh_covers_every_visible_pixel_with_consistent_winding(self):
        alpha = np.zeros((50, 70), dtype=np.uint8)
        yy, xx = np.mgrid[:50, :70]
        alpha[(xx-35)**2/900 + (yy-25)**2/400 < 1] = 255
        pixels, triangles, _ = build_grid_mesh(alpha, 7, 32, 0)
        areas = signed_areas(pixels, triangles)
        self.assertTrue(np.all(areas > 0) or np.all(areas < 0))
        covered = np.zeros_like(alpha, dtype=bool)
        for tri in triangles:
            p = pixels[tri]
            x0, y0 = np.floor(p.min(0)).astype(int)
            x1, y1 = np.ceil(p.max(0)).astype(int)
            covered[y0:y1, x0:x1] = True  # cells are axis aligned: the two triangles tile the cell box
        self.assertTrue(np.all(covered[alpha > 32]))

    def test_holes_and_diagonal_contacts_become_one_outline_listed_first(self):
        from skinlib import boundary_loops, hull_first
        alpha = np.zeros((40, 40), dtype=np.uint8)
        alpha[4:36, 4:36] = 255
        alpha[14:26, 14:26] = 0          # enclosed hole
        alpha[0:4, 36:40] = 255          # touches the square only at a corner
        pixels, triangles, _ = build_grid_mesh(alpha, 4, 32, 0)
        self.assertEqual(len(boundary_loops(triangles)), 1)
        ordered, tris, hull, loops = hull_first(pixels, triangles)
        self.assertEqual(loops, 1)
        self.assertEqual(sorted(boundary_loops(tris)[0]), list(range(hull)))
        self.assertTrue(np.all(np.sign(signed_areas(ordered, tris)) == np.sign(signed_areas(pixels, triangles))[0]))

    def test_quad_mode_gives_one_outline_for_separate_islands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = Image.new('RGBA', (120, 40), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            for x in (6, 52, 98):
                draw.ellipse([x, 8, x + 16, 30], fill=(200, 200, 200, 255))
            image.save(root / 'scenery.png')
            rig = {'schema': 'ogs.skin-rig/1', 'bones': [{'name': 'root'}],
                   'parts': [{'name': 'scenery', 'image': 'scenery.png', 'origin': [0, 0], 'at': [0, 0], 'density': 4,
                              'bones': ['root'], 'mesh': {'mode': 'quad'}}]}
            (root / 'rig.json').write_text(json.dumps(rig))
            built = build(load_rig(root / 'rig.json'))
            part = built['parts']['scenery']
            self.assertEqual(part['stats']['vertices'], 4)
            self.assertEqual(part['hull'], 4)
            rig['parts'][0]['mesh'] = {'spacing': 8, 'margin': 0}
            (root / 'rig.json').write_text(json.dumps(rig))
            self.assertIsNone(build(load_rig(root / 'rig.json'))['parts']['scenery']['hull'])  # grid mode: three outlines
            rig['bones'].append({'name': 'other'})
            rig['parts'][0].update(bones=['root', 'other'], mesh={'mode': 'quad'}, weights={'handleRadius': 2})
            (root / 'rig.json').write_text(json.dumps(rig))
            with self.assertRaises(SkinError):
                build(load_rig(root / 'rig.json'))

    def test_empty_layer_is_blocked(self):
        with self.assertRaises(SkinError):
            build_grid_mesh(np.zeros((10, 10), dtype=np.uint8), 4)


class LintTests(unittest.TestCase):
    def lint(self, root, weights, rig=None, mesh=None):
        rig = rig or load_rig(root / 'rig.json')
        mesh = mesh or load_mesh(root / 'mesh.json')
        return lint_weights.lint(rig, mesh, weights)[0]

    def test_clean_weights_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, weights, _ = pipeline(root)
            self.assertEqual(self.lint(root, weights), [])

    def test_detached_influence_island_is_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig, mesh, weights, _ = pipeline(root)
            v = mesh['parts']['limb']['vertices']
            world = forward(rig)
            from skinlib import invert
            inverse = invert(world['lower'])
            rows = weights['parts']['limb']['weights']
            far = int(np.argmin(v[:, 0]))  # deep in the upper bone's rigid zone
            x, y = apply(inverse, v[far])
            rows[far] = [{'bone': 'upper', 'weight': 0.5, 'x': rows[far][0]['x'], 'y': rows[far][0]['y']},
                         {'bone': 'lower', 'weight': 0.5, 'x': float(x), 'y': float(y)}]
            weights['parts']['limb']['handles'] = [h for h in weights['parts']['limb']['handles'] if h != far]
            errors = self.lint(root, weights, rig, mesh)
            self.assertTrue(any('detached islands' in e for e in errors), errors)

    def test_touching_rigid_zones_are_a_seam(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig, mesh, weights, _ = pipeline(root, inset=0.0)
            self.assertEqual(self.lint(root, weights, rig, mesh), [])
            part = weights['parts']['limb']
            v = mesh['parts']['limb']['vertices']
            for index in np.flatnonzero(np.abs(v[:, 0] - 20) < 1e-6):  # the free joint row becomes rigid upper
                upper = next(i for i in part['weights'][index] if i['bone'] == 'upper')
                part['weights'][index] = [dict(upper, weight=1.0)]
                part['handles'].append(int(index))
            self.assertTrue(any('collapses to a seam' in e for e in self.lint(root, weights, rig, mesh)))
            rig['parts'][0]['lint'] = {'minTransition': 6.0}  # declared stricter bound also applies
            _, _, clean, _ = pipeline(root, inset=0.0)
            self.assertTrue(any('collapses to a seam' in e for e in self.lint(root, clean, rig, mesh)))

    def test_unnormalized_unknown_and_stale_bindings_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rig, mesh, weights, _ = pipeline(root)
            rows = weights['parts']['limb']['weights']
            rows[3][0]['weight'] *= 0.5
            rows[4].append({'bone': 'root', 'weight': 0.0, 'x': 0, 'y': 0})
            rig['_bones']['upper']['rotation'] = 5  # setup changed after binding
            errors = self.lint(root, weights, rig, mesh)
            self.assertTrue(any('sum to' in e for e in errors))
            self.assertTrue(any('not an allowed influence' in e for e in errors))
            self.assertTrue(any('bind coordinates drift' in e for e in errors))


class PoseTests(unittest.TestCase):
    def test_two_bone_ik_reaches_target_and_reports_unreachable(self):
        with tempfile.TemporaryDirectory() as tmp:
            rig = load_rig(strip_fixture(Path(tmp)))
            for target, problems in (([25, 12], 0), ([60, 0], 1)):
                motion = {'ik': [{'name': 'arm', 'bones': ['upper', 'lower'], 'target': {'fixed': target}, 'bend': 1}]}
                world, issues, _ = pose_trace.evaluate(rig, motion, 0, 1e-6)
                self.assertEqual(len(issues), problems)
                if not problems:
                    tip = apply(world['lower'], [20, 0])
                    self.assertLess(np.linalg.norm(tip - target), 1e-9)

    def test_trace_is_accepted_by_spine_skeletal_audit_and_rigid_control_is_rejected(self):
        for method, expected in (('harmonic', 0), ('nearest', 1)):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(method=method):
                root = Path(tmp)
                rig, mesh, weights, _ = pipeline(root, spacing=4, method=method)
                weights['meshSHA256'] = __import__('skinlib').sha256(root / 'mesh.json')
                write_json(root / 'weights.json', weights)
                keys = [{'t': 0, 'v': 0}, {'t': 0.5, 'v': 100}, {'t': 1, 'v': 0}]
                write_json(root / 'motion.json', {'schema': 'ogs.skin-motion/1', 'sampleRate': 30, 'duration': 1, 'loop': True,
                                                  'tracks': [{'bone': 'lower', 'property': 'rotate', 'keys': keys}]})
                code = subprocess.run([sys.executable, HERE / 'pose_trace.py', root / 'rig.json', root / 'mesh.json', root / 'weights.json',
                                       root / 'motion.json', '--out', root / 'trace.json'], capture_output=True).returncode
                self.assertEqual(code, 0)
                audit = subprocess.run([sys.executable, AUDIT, root / 'trace.json', '--out', root / 'audit.json'], capture_output=True)
                self.assertEqual(audit.returncode, expected, audit.stdout[-800:])


if __name__ == '__main__':
    unittest.main()
