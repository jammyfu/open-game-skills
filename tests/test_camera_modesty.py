"""P0 unit/CLI paths for camera-modesty; synthetic poses, not engine or LLM tests."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/disciplines/camera-modesty/SKILL.md'
SCRIPT = ROOT / 'skills/disciplines/camera-modesty/scripts/modesty_check.py'
EXAMPLE = ROOT / 'skills/disciplines/camera-modesty/assets/framing.example.json'


def load():
    spec = importlib.util.spec_from_file_location('modesty_check', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def framing():
    return json.loads(EXAMPLE.read_text(encoding='utf-8'))


def cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True, timeout=8)


def low_under_hem(data):
    data['poses'].append({
        'id': 'invasive-low',
        'position': [0.04, 0.12, 0.16],
        'forward': [0.0, 1.0, 0.0],
        'up': [0.0, 0.0, -1.0],
        'fov_v_deg': 60,
        'near_m': 0.08,
        'aspect': 1.7778,
        'authored_intent': 'none',
    })
    return data


def groin_zoom(data):
    data['poses'].append({
        'id': 'groin-zoom',
        'position': [0.0, 0.88, 0.42],
        'forward': [0.0, 0.0, -1.0],
        'up': [0.0, 1.0, 0.0],
        'fov_v_deg': 70,
        'near_m': 0.05,
        'aspect': 1.7778,
        'authored_intent': 'none',
    })
    return data


class CameraModestyOwnershipTests(unittest.TestCase):
    def test_skill_owns_modesty_not_collision_or_shot_grammar(self):
        text = SKILL.read_text(encoding='utf-8')
        front = yaml.safe_load(text.split('---', 2)[1])
        self.assertEqual(front['name'], 'camera-modesty')
        self.assertTrue(front['description'].strip().lower().startswith('use when '))
        body = text.lower()
        for token in ('modesty', 'dignity', 'camera-shots', 'camera-anti-clip', 'fov-comfort',
                      'modest', 'adult', 'medical-exam', 'authored_intent'):
            with self.subTest(token=token):
                self.assertIn(token, body)
        self.assertIn('one specialized slot', body)
        self.assertIn('phase limit', body)
        self.assertNotIn('tutorial', body)


class CameraModestyEvaluateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load()

    def report(self, data):
        return self.module.evaluate(data)

    def test_published_example_is_static_pass(self):
        result = self.report(framing())
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['runtime_validation'], 'not-run')
        self.assertEqual(result['validation_mode'], 'static-modesty-preflight')
        self.assertEqual(result['policy_mode'], 'modest')
        self.assertTrue(result['poses'])
        self.assertTrue(any('no mesh' in item for item in result['limits']))

    def test_under_hem_look_fails_and_suggests_clamp(self):
        result = self.report(low_under_hem(framing()))
        self.assertEqual(result['status'], 'fail')
        pose = next(row for row in result['poses'] if row['id'] == 'invasive-low')
        self.assertEqual(pose['status'], 'fail')
        self.assertTrue(any(v['rule_id'] == 'under-hem-look' for v in pose['violations']))
        self.assertIsNotNone(pose['suggested_clamp'])
        self.assertTrue(pose['suggested_clamp']['actions'])
        self.assertTrue(set(pose['suggested_clamp']['actions']) <= {'raise pitch', 'pull back', 'raise boom'})

    def test_between_legs_fails(self):
        data = framing()
        data['poses'].append({
            'id': 'between-legs',
            'position': [0.05, 0.4, 0.04],
            'forward': [0.0, 0.0, 1.0],
            'up': [0.0, 1.0, 0.0],
            'fov_v_deg': 40,
            'near_m': 0.05,
            'aspect': 1.7778,
            'authored_intent': 'none',
        })
        result = self.report(data)
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(c['rule_id'] == 'between-legs' and c['status'] == 'fail' for c in result['checks']))

    def test_private_region_zoom_fails(self):
        result = self.report(groin_zoom(framing()))
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(c['rule_id'] == 'private-region-zoom' and c['status'] == 'fail'
                            for c in result['checks']))

    def test_boom_sweep_fails_when_a_sample_fails(self):
        data = low_under_hem(framing())
        data['boom_sweeps'][0]['pose_ids'].append('invasive-low')
        result = self.report(data)
        sweep = next(row for row in result['sweeps'] if row['id'] == 'intro-orbit')
        self.assertEqual(sweep['status'], 'fail')
        self.assertIn('invasive-low', sweep['failed_pose_ids'])

    def test_adult_without_intent_stays_modest(self):
        data = groin_zoom(framing())
        data['policy']['mode'] = 'adult'
        result = self.report(data)
        self.assertEqual(result['status'], 'fail')
        self.assertEqual(result['policy_mode'], 'adult')

    def test_matching_adult_intent_waives_private_rules(self):
        data = groin_zoom(framing())
        data['policy']['mode'] = 'adult'
        data['poses'][-1]['authored_intent'] = 'adult'
        result = self.report(data)
        self.assertEqual(result['status'], 'pass')
        self.assertTrue(any(c['rule_id'] == 'intent-opt-in' and c['observed'].get('waived')
                            for c in result['checks']))

    def test_medical_exam_intent_mismatch_does_not_waive(self):
        data = groin_zoom(framing())
        data['policy']['mode'] = 'medical-exam'
        data['poses'][-1]['authored_intent'] = 'adult'
        self.assertEqual(self.report(data)['status'], 'fail')

    def test_invalid_contracts_rejected(self):
        bad = []
        data = framing(); data['units'] = 'cm'; bad.append(data)
        data = framing(); data['schema_version'] = True; bad.append(data)
        data = framing(); data['policy']['mode'] = 'cinematic'; bad.append(data)
        data = framing(); data['poses'][0]['fov_v_deg'] = float('nan'); bad.append(data)
        data = framing(); data['characters'][0]['proxy']['radius'] = True; bad.append(data)
        data = framing(); data['characters'][0]['rotation'] = [0, 90, 0]; bad.append(data)
        data = framing(); data['poses'][0]['forward'] = [0, 1, 0]; data['poses'][0]['up'] = [0, 1, 0]; bad.append(data)
        data = framing(); data['boom_sweeps'][0]['pose_ids'] = ['missing']; bad.append(data)
        data = framing(); data['characters'][0]['landmarks']['chest'] = [0, 0.2, 0]; bad.append(data)
        data = framing(); data['poses'] = []; bad.append(data)
        for i, data in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                self.report(data)

    def test_hero_low_angle_in_front_is_not_under_hem(self):
        data = framing()
        data['poses'].append({
            'id': 'hero-low',
            'position': [0.0, 0.55, 2.2],
            'forward': [0.0, 0.42, -0.91],
            'up': [0.0, 1.0, 0.0],
            'fov_v_deg': 40,
            'near_m': 0.12,
            'aspect': 1.7778,
            'authored_intent': 'none',
        })
        result = self.report(data)
        self.assertEqual(result['status'], 'pass')
        self.assertFalse(any(c['rule_id'] == 'under-hem-look' and c['status'] == 'fail' for c in result['checks']))


class CameraModestyCliTests(unittest.TestCase):
    def test_cli_pass_fail_and_blocked_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'framing.json'
            source.write_text(json.dumps(framing()))
            result = cli(source)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'pass')
            self.assertEqual(len(report['input_sha256']), 64)
            self.assertEqual(len(report['tool_sha256']), 64)
            source.write_text(json.dumps(low_under_hem(framing())))
            result = cli(source)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'fail')
            result = cli(Path(tmp) / 'absent.json')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)['status'], 'blocked')

    def test_cli_outputs_identity_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            source.write_text(json.dumps(framing()))
            out = Path(tmp) / 'report.json'
            result = cli(source, '--output', out)
            self.assertEqual(result.returncode, 0, result.stderr)
            before = out.read_bytes()
            self.assertEqual(cli(source, '--output', out).returncode, 2)
            self.assertEqual(out.read_bytes(), before)
            result = cli(source, '--output', source)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_text(), json.dumps(framing()))

    def test_duplicate_json_nonfinite_and_size_limit_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            for raw in ['{"schema_version":1,"schema_version":1}', '{"x": NaN}']:
                source.write_text(raw)
                with self.subTest(raw=raw):
                    self.assertEqual(cli(source).returncode, 2)
            large = Path(tmp) / 'large.json'
            large.write_bytes(b' ' * (load().MAX_BYTES + 1))
            result = cli(large)
            self.assertEqual(result.returncode, 2)
            self.assertIn('limit', json.loads(result.stderr)['reason'])


if __name__ == '__main__':
    unittest.main()
