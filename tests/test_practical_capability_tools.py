"""Executable tool tests; synthetic layout/trace inputs, not engine or LLM tests."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / 'skills/disciplines/scene-assembly/scripts/scene_preflight.py'
TRACE = ROOT / 'skills/disciplines/gameplay-harness/scripts/trace_compare.py'


def layout():
    return {
        'schema_version': 1, 'layout_id': 'two-room-v1', 'units': 'm',
        'basis': 'right-handed-y-up',
        'player': {'radius': .35, 'height': 1.8, 'clearance': .1, 'max_step': .3},
        'rooms': [
            {'id': 'start', 'bounds': [[0, 0, 0], [6, 3, 6]]},
            {'id': 'exit', 'bounds': [[6, 0, 0], [12, 3, 6]]},
        ],
        'solids': [{'id': 'crate', 'bounds': [[2, 0, 1], [3, 1, 2]]}],
        'spawns': [{'id': 'player', 'room': 'start', 'position': [1, 0, 3]}],
        'portals': [{'id': 'door', 'rooms': ['start', 'exit'], 'axis': 'x',
                     'center': [6, 0, 3], 'width': 1.5, 'height': 2.3}],
        'required_rooms': ['exit'],
    }


def trace():
    return {
        'schema_version': 1, 'build': 'a' * 40,
        'context': {'adapter': 'test-v1', 'oracle': 'move-v1', 'clock': '100hz-v1',
                    'tape_sha256': 'b' * 64, 'initial_state_sha256': 'c' * 64,
                    'rng': 'none'},
        'frames': [{'tick': i, 'state': {'x_mm': i * 10, 'hp': 100},
                    'events': []} for i in range(4)],
    }


class ToolCase(unittest.TestCase):
    def module(self, path):
        self.assertTrue(path.is_file(), f'missing capability tool: {path.name}')
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def cli(self, path, *args):
        self.assertTrue(path.is_file(), f'missing capability tool: {path.name}')
        return subprocess.run([sys.executable, str(path), *map(str, args)],
                              capture_output=True, text=True, timeout=8)


class SceneTests(ToolCase):
    def report(self, data):
        return self.module(SCENE).evaluate(data)

    def test_valid_layout_is_static_only(self):
        result = self.report(layout())
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['runtime_validation'], 'not-run')
        self.assertEqual(result['validation_mode'], 'static-layout-preflight')

    def test_door_too_narrow_fails_fit_and_reachability(self):
        data = layout(); data['portals'][0]['width'] = .7
        result = self.report(data)
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(r['id'] == 'portal-fit:door' and r['status'] == 'fail' for r in result['checks']))
        self.assertTrue(any(r['id'] == 'reachable:player:exit' and r['status'] == 'fail' for r in result['checks']))

    def test_decoration_cannot_block_spawn(self):
        data = layout(); data['solids'][0]['bounds'] = [[.8, 0, 2.8], [1.2, 1, 3.2]]
        result = self.report(data)
        self.assertTrue(any(r['id'] == 'spawn-clear:player' and r['status'] == 'fail' for r in result['checks']))

    def test_decoration_cannot_block_door_sweep(self):
        data = layout(); data['solids'][0]['bounds'] = [[5.8, 0, 2.8], [6, 2, 3.2]]
        self.assertEqual(self.report(data)['status'], 'fail')

    def test_door_must_be_on_shared_boundary(self):
        for axis, center in [('x', [3, 0, 3]), ('z', [6, 0, 3])]:
            with self.subTest(axis=axis):
                data = layout(); data['portals'][0].update(axis=axis, center=center)
                self.assertEqual(self.report(data)['status'], 'fail')

    def test_high_step_or_insufficient_headroom_fails(self):
        for change in ['step', 'height', 'floor']:
            with self.subTest(change=change):
                data = layout()
                if change == 'step':
                    data['rooms'][1]['bounds'][0][1] = 1
                    data['portals'][0]['center'][1] = 1
                elif change == 'height': data['portals'][0]['height'] = 1.7
                else: data['spawns'][0]['position'][1] = .4
                self.assertEqual(self.report(data)['status'], 'fail')

    def test_exact_clearance_and_reversed_room_order_pass(self):
        data = layout(); data['portals'][0]['width'] = .9
        data['portals'][0]['rooms'].reverse()
        self.assertEqual(self.report(data)['status'], 'pass')

    def test_z_axis_and_negative_coordinates_pass(self):
        data = layout()
        for group in ['rooms', 'solids']:
            for item in data[group]:
                item['bounds'] = [[v[2] - 10, v[1], v[0] - 10] for v in item['bounds']]
        for item in data['spawns']:
            v = item['position']; item['position'] = [v[2] - 10, v[1], v[0] - 10]
        p = data['portals'][0]; v = p['center']; p['center'] = [v[2] - 10, v[1], v[0] - 10]; p['axis'] = 'z'
        self.assertEqual(self.report(data)['status'], 'pass')

    def test_disconnected_goal_is_not_silently_dropped(self):
        data = layout(); data['portals'] = []
        self.assertEqual(self.report(data)['status'], 'fail')

    def test_invalid_contracts_rejected(self):
        bad = []
        for key, value in [('units', 'cm'), ('schema_version', True), ('runtime_validation', 'pass')]:
            data = layout(); data[key] = value; bad.append(data)
        data = layout(); data['rooms'][1]['id'] = 'start'; bad.append(data)
        data = layout(); data['rooms'][0]['bounds'][1][0] = float('nan'); bad.append(data)
        data = layout(); data['player']['radius'] = True; bad.append(data)
        data = layout(); data['spawns'][0]['room'] = 'missing'; bad.append(data)
        data = layout(); data['required_rooms'] = ['missing']; bad.append(data)
        data = layout(); data['rooms'][0]['rotation'] = [0, 90, 0]; bad.append(data)
        data = layout(); data['solids'][0]['bounds'][0][0] = 8; bad.append(data)
        data = layout(); data['spawns'] = []; bad.append(data)
        for i, data in enumerate(bad):
            with self.subTest(case=i):
                with self.assertRaises(ValueError): self.report(data)

    def test_overlapping_rooms_and_uncontained_solid_fail(self):
        for kind in ['overlap', 'solid']:
            data = layout()
            if kind == 'overlap': data['rooms'][1]['bounds'][0][0] = 5
            else: data['solids'][0]['bounds'] = [[20, 0, 1], [21, 1, 2]]
            with self.subTest(kind=kind): self.assertEqual(self.report(data)['status'], 'fail')

    def test_cli_outputs_identity_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'; source.write_text(json.dumps(layout()))
            out = Path(tmp) / 'report.json'
            result = self.cli(SCENE, source, '--output', out)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(out.read_text()); before = out.read_bytes()
            self.assertEqual(len(report['input_sha256']), 64)
            self.assertEqual(len(report['tool_sha256']), 64)
            self.assertEqual(self.cli(SCENE, source, '--output', out).returncode, 2)
            self.assertEqual(out.read_bytes(), before)

    def test_duplicate_json_and_nonfinite_are_errors_not_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            for raw in ['{"schema_version":1,"schema_version":1}', '{"x": NaN}']:
                source.write_text(raw)
                with self.subTest(raw=raw): self.assertEqual(self.cli(SCENE, source).returncode, 2)


class TraceTests(ToolCase):
    def compare(self, a, b): return self.module(TRACE).compare(a, b)

    def test_identical_stable_state_across_different_builds_passes(self):
        a = trace(); b = trace(); b['build'] = 'd' * 40
        result = self.compare(a, b)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['frames_compared'], 4)
        self.assertEqual(result['failure_attribution'], 'unknown')

    def test_first_divergent_tick_and_state_path(self):
        a = trace(); b = trace(); b['frames'][2]['state']['x_mm'] = 999
        b['frames'][3]['state']['hp'] = 0
        result = self.compare(a, b)
        self.assertEqual(result['status'], 'fail')
        self.assertEqual(result['first_difference']['tick'], 2)
        self.assertEqual(result['first_difference']['path'], '/state/x_mm')
        self.assertEqual(result['first_difference']['expected'], 20)
        self.assertEqual(result['first_difference']['observed'], 999)

    def test_dictionary_order_ignored_but_event_order_preserved(self):
        a = trace(); b = trace(); b['frames'][1]['state'] = {'hp': 100, 'x_mm': 10}
        self.assertEqual(self.compare(a, b)['status'], 'pass')
        a['frames'][1]['events'] = [{'id': 'hit'}, {'id': 'grant'}]
        b['frames'][1]['events'] = list(reversed(a['frames'][1]['events']))
        self.assertEqual(self.compare(a, b)['status'], 'fail')

    def test_bool_is_not_number_and_missing_is_not_null(self):
        a = trace(); b = trace(); a['frames'][0]['state']['x_mm'] = 1
        b['frames'][0]['state']['x_mm'] = True
        self.assertEqual(self.compare(a, b)['status'], 'fail')
        a = trace(); b = trace(); a['frames'][0]['state']['optional'] = None
        result = self.compare(a, b)
        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['first_difference']['observed_present'])
        self.assertTrue(result['first_difference']['expected_present'])

    def test_incompatible_context_blocks_comparison(self):
        for key in trace()['context']:
            a = trace(); b = trace(); b['context'][key] = 'e' * 64 if key.endswith('sha256') else 'different'
            with self.subTest(key=key):
                result = self.compare(a, b)
                self.assertEqual(result['status'], 'blocked')
                self.assertEqual(result['frames_compared'], 0)

    def test_truncation_and_extra_frames_fail(self):
        for side in ['a', 'b']:
            a = trace(); b = trace(); (a if side == 'a' else b)['frames'].pop()
            with self.subTest(side=side):
                result = self.compare(a, b)
                self.assertEqual(result['status'], 'fail')
                self.assertEqual(result['first_difference']['tick'], 3)

    def test_invalid_trace_rejected(self):
        for kind in ['empty', 'gap', 'duplicate', 'nan', 'unknown-context', 'bool-tick', 'missing-build']:
            b = trace()
            if kind == 'empty': b['frames'] = []
            elif kind == 'gap': b['frames'][2]['tick'] = 9
            elif kind == 'duplicate': b['frames'][2]['tick'] = 1
            elif kind == 'nan': b['frames'][1]['state']['hp'] = float('nan')
            elif kind == 'unknown-context': b['context']['ignored'] = 'v1'
            elif kind == 'bool-tick': b['frames'][0]['tick'] = False
            else: del b['build']
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.compare(trace(), b)

    def test_cli_exit_codes_and_inputs_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / 'golden.json'; b = Path(tmp) / 'candidate.json'
            a.write_text(json.dumps(trace())); original = a.read_bytes()
            for status in ['pass', 'fail', 'blocked']:
                data = trace()
                if status == 'fail': data['frames'][1]['state']['hp'] = 1
                if status == 'blocked': data['context']['oracle'] = 'other-v1'
                b.write_text(json.dumps(data))
                result = self.cli(TRACE, a, b)
                with self.subTest(status=status):
                    self.assertEqual(result.returncode, {'pass': 0, 'fail': 1, 'blocked': 2}[status], result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['status'], status)
                    self.assertEqual(len(report['baseline_sha256']), 64)
            self.assertEqual(a.read_bytes(), original)


class IntegrationAndBoundaryTests(ToolCase):
    def test_scene_assembly_preparation_returns_candidates_not_a_ready_scene(self):
        tool = ROOT / 'skills/assets/open-asset-fixture/scripts/prepare_assets.py'
        result = self.cli(tool, '--skill', 'scene-assembly')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'needs-acquisition')
        self.assertEqual(report['runtime_validation'], 'not-run')
        roles = report['skills'][0]['roles']
        self.assertEqual(len(roles), 1)
        self.assertEqual(roles[0]['role'], 'modular-environment-candidates')
        self.assertEqual(roles[0]['request']['requires'], ['static-geometry'])
        self.assertTrue(roles[0]['selection']['matches'])

    def test_scene_assembly_pinned_only_never_silently_acquires(self):
        tool = ROOT / 'skills/assets/open-asset-fixture/scripts/prepare_assets.py'
        result = self.cli(tool, '--skill', 'scene-assembly', '--pinned-only')
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['skills'][0]['status'], 'blocked')
        self.assertEqual(report['skills'][0]['roles'][0]['selection']['matches'], [])

    def test_published_examples_execute_in_declared_tool_scope(self):
        scene = json.loads((SCENE.parents[1] / 'assets/layout.example.json').read_text())
        record = json.loads((TRACE.parents[1] / 'assets/trace.example.json').read_text())
        self.assertEqual(self.module(SCENE).evaluate(scene)['status'], 'pass')
        result = self.module(TRACE).compare(record, record)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['runtime_validation'], 'not-run')

    def test_room_graph_pass_is_not_an_interior_path_proof(self):
        data = layout()
        data['solids'] = [{'id': 'partition', 'bounds': [[3, 0, 0], [3.5, 3, 6]]}]
        result = self.module(SCENE).evaluate(data)
        self.assertEqual(result['status'], 'pass')  # Deliberately outside the tool's oracle.
        self.assertEqual(result['runtime_validation'], 'not-run')
        self.assertTrue(any('no within-room pathfinding' in v for v in result['limits']))

    def test_nonfinite_derived_scene_dimensions_are_rejected(self):
        for radius, x in [(9e307, 1), (1e307, 1.79e308)]:
            data = layout(); data['player']['radius'] = radius
            data['spawns'][0]['position'][0] = x
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                self.module(SCENE).evaluate(data)

    def test_json_pointer_escapes_field_names(self):
        a = trace(); b = trace()
        a['frames'][0]['state']['a/b~c'] = 1
        b['frames'][0]['state']['a/b~c'] = 2
        result = self.module(TRACE).compare(a, b)
        self.assertEqual(result['first_difference']['path'], '/state/a~1b~0c')

    def test_trace_reports_cannot_overwrite_inputs_or_follow_output_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / 'baseline.json'; b = Path(tmp) / 'candidate.json'
            a.write_text(json.dumps(trace())); b.write_bytes(a.read_bytes())
            original = a.read_bytes(); link = Path(tmp) / 'report.json'
            for out in [a, link]:
                if out == link: link.symlink_to(a)
                result = self.cli(TRACE, a, b, '--output', out)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(a.read_bytes(), original)

    def test_cli_size_limits_block_instead_of_reading_unbounded_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            small = Path(tmp) / 'small.json'; small.write_text(json.dumps(trace()))
            large = Path(tmp) / 'large.json'
            for tool in [SCENE, TRACE]:
                maximum = self.module(tool).MAX_BYTES
                large.write_bytes(b' ' * (maximum + 1))
                args = [large] if tool == SCENE else [small, large]
                result = self.cli(tool, *args)
                self.assertEqual(result.returncode, 2)
                self.assertIn('limit', json.loads(result.stderr)['reason'])

    def test_nested_trace_and_duplicate_keys_are_blocked(self):
        module = self.module(TRACE)
        data = trace(); state = data['frames'][0]['state']
        for _ in range(66): state['next'] = {}; state = state['next']
        with self.assertRaises(ValueError): module.compare(trace(), data)
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / 'a.json'; b = Path(tmp) / 'b.json'
            a.write_text(json.dumps(trace())); b.write_text('{"frames":[],"frames":[]}')
            result = self.cli(TRACE, a, b)
            self.assertEqual(result.returncode, 2)
            self.assertIn('duplicate JSON key', json.loads(result.stderr)['reason'])


if __name__ == '__main__': unittest.main()
