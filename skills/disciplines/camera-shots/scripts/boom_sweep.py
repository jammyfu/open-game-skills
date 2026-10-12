"""Offline boom-sweep presentation sampler. Not anti-clip, targeting or an engine."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

EPS = 1e-7  # Arithmetic tolerance in meters/degrees, not a design clearance.
MAX_BYTES = 4 * 1024 * 1024
SAMPLE_MIN = 2
SAMPLE_MAX = 64
ELEVATION_ABS_MAX = 90.0
AZIMUTH_SWEEP_ABS_MAX = 360.0
MODES = ('side-plane', 'orbit-third', 'first-person', 'rail', 'lock-follow')
REQUIRED = (
    'schema_version', 'sweep_id', 'units', 'basis', 'angle_units', 'owner',
    'camera_collision_required', 'anchor', 'boom', 'sample_count',
)
OPTIONAL = (
    'trigger', 'mode', 'transition_policy', 'player_control', 'interruption_return',
    'look_target', 'gameplay_lock_target', 'fov_ref', 'offset_ref',
)
BOOM_FIELDS = (
    'length_start', 'length_end', 'elevation_start', 'elevation_end',
    'azimuth_start', 'azimuth_sweep',
)


def fields(value, required, where):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f'{where}: expected fields {sorted(required)}')


def known(value, required, optional, where):
    if not isinstance(value, dict):
        raise ValueError(f'{where}: expected object')
    keys = set(value)
    extra = keys - set(required) - set(optional)
    missing = set(required) - keys
    if extra or missing:
        raise ValueError(f'{where}: expected fields {sorted(required)}; optional {sorted(optional)}')


def number(value, where, minimum=None, maximum=None, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f'{where}: expected finite number, not boolean')
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise ValueError(f'{where}: number out of range')
    if positive and value <= 0:
        raise ValueError(f'{where}: number out of range')
    return float(value)


def vector(value, where):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f'{where}: expected three coordinates')
    return [number(v, where) for v in value]


def text(value, where):
    if not isinstance(value, str) or not value.strip() or len(value) > 120:
        raise ValueError(f'{where}: expected nonempty text of at most 120 characters')
    return value


def target(value, where, *, position_required):
    required = ['id', 'position'] if position_required else ['id']
    fields(value, required, where)
    text(value['id'], where + '.id')
    if position_required:
        vector(value['position'], where + '.position')


def validate(data):
    known(data, REQUIRED, OPTIONAL, 'plan')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('unsupported schema_version')
    if data['units'] != 'm' or data['basis'] != 'right-handed-y-up' or data['angle_units'] != 'deg':
        raise ValueError('v1 requires meters, right-handed-y-up and degree angles')
    text(data['sweep_id'], 'sweep_id')
    text(data['owner'], 'owner')
    if type(data['camera_collision_required']) is not bool:
        raise ValueError('camera_collision_required must be a boolean')
    for key in ('trigger', 'transition_policy', 'player_control', 'interruption_return'):
        if key in data:
            text(data[key], key)
    if 'mode' in data and data['mode'] not in MODES:
        raise ValueError('mode must be a camera-shots compatible mode')
    target(data['anchor'], 'anchor', position_required=True)
    if 'look_target' in data:
        target(data['look_target'], 'look_target', position_required=True)
    if 'gameplay_lock_target' in data:
        target(data['gameplay_lock_target'], 'gameplay_lock_target', position_required=False)
    fields(data['boom'], BOOM_FIELDS, 'boom')
    for key in BOOM_FIELDS:
        number(data['boom'][key], 'boom.' + key)
    if type(data['sample_count']) is not int:
        raise ValueError('sample_count must be an integer, not boolean')
    if 'fov_ref' in data:
        fields(data['fov_ref'], ['comfort_profile_id', 'projection', 'degrees'], 'fov_ref')
        text(data['fov_ref']['comfort_profile_id'], 'fov_ref.comfort_profile_id')
        if data['fov_ref']['projection'] not in ('vertical', 'horizontal'):
            raise ValueError('fov_ref.projection must be vertical or horizontal')
        number(data['fov_ref']['degrees'], 'fov_ref.degrees', positive=True, maximum=179.999)
    if 'offset_ref' in data:
        fields(data['offset_ref'], ['id', 'translation'], 'offset_ref')
        text(data['offset_ref']['id'], 'offset_ref.id')
        vector(data['offset_ref']['translation'], 'offset_ref.translation')


def boom_position(anchor, length, elevation_deg, azimuth_deg, offset):
    # Azimuth 0 = +Z, positive azimuth toward +X, elevation 0 = horizontal, +Y up.
    elevation = math.radians(elevation_deg)
    azimuth = math.radians(azimuth_deg)
    horizontal = length * math.cos(elevation)
    position = [
        anchor[0] + horizontal * math.sin(azimuth) + offset[0],
        anchor[1] + length * math.sin(elevation) + offset[1],
        anchor[2] + horizontal * math.cos(azimuth) + offset[2],
    ]
    return [number(v, 'derived camera position') for v in position]


def look_point(data):
    if 'look_target' in data:
        return list(data['look_target']['position'])
    return list(data['anchor']['position'])


def sample_poses(data):
    boom = data['boom']
    count = data['sample_count']
    offset = data['offset_ref']['translation'] if 'offset_ref' in data else [0.0, 0.0, 0.0]
    look = look_point(data)
    flag = 'required' if data['camera_collision_required'] else 'not-requested'
    poses = []
    last = count - 1
    for index in range(count):
        t = 0.0 if last == 0 else index / last
        length = boom['length_start'] + t * (boom['length_end'] - boom['length_start'])
        elevation = boom['elevation_start'] + t * (boom['elevation_end'] - boom['elevation_start'])
        azimuth = boom['azimuth_start'] + t * boom['azimuth_sweep']
        position = boom_position(data['anchor']['position'], length, elevation, azimuth, offset)
        poses.append({
            'index': index,
            't': t,
            'boom_length': length,
            'elevation_deg': elevation,
            'azimuth_deg': azimuth,
            'position': position,
            'look': look,
            'anti_clip_validation': flag,
        })
    return poses


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    validate(data)
    checks = []

    def check(name, ok, observed):
        checks.append({'id': name, 'status': 'pass' if ok else 'fail', 'observed': observed})
        return ok

    boom = data['boom']
    lengths = [boom['length_start'], boom['length_end']]
    elevations = [boom['elevation_start'], boom['elevation_end']]
    check('boom-length-positive', all(v > 0 for v in lengths), {'length_start': lengths[0], 'length_end': lengths[1]})
    count = data['sample_count']
    check('sample-count-bounds', SAMPLE_MIN <= count <= SAMPLE_MAX,
          {'sample_count': count, 'minimum': SAMPLE_MIN, 'maximum': SAMPLE_MAX})
    check('elevation-range', all(abs(v) <= ELEVATION_ABS_MAX for v in elevations),
          {'elevation_start': elevations[0], 'elevation_end': elevations[1], 'abs_max_deg': ELEVATION_ABS_MAX})
    check('azimuth-sweep-range', abs(boom['azimuth_sweep']) <= AZIMUTH_SWEEP_ABS_MAX,
          {'azimuth_sweep': boom['azimuth_sweep'], 'abs_max_deg': AZIMUTH_SWEEP_ABS_MAX})

    presentation_ids = {data['anchor']['id']}
    if 'look_target' in data:
        presentation_ids.add(data['look_target']['id'])
    gameplay_id = data['gameplay_lock_target']['id'] if 'gameplay_lock_target' in data else None
    identity_ok = gameplay_id is None or gameplay_id not in presentation_ids
    check('presentation-gameplay-identity-distinct', identity_ok,
          {'presentation_ids': sorted(presentation_ids), 'gameplay_lock_target_id': gameplay_id})

    poses = sample_poses(data) if SAMPLE_MIN <= count <= SAMPLE_MAX else []
    look = look_point(data)
    coincident = []
    for pose in poses:
        delta = [look[i] - pose['position'][i] for i in range(3)]
        distance = math.sqrt(sum(v * v for v in delta))
        number(distance, 'derived look distance')
        if distance <= EPS:
            coincident.append(pose['index'])
    check('look-separated-from-camera', not coincident,
          {'coincident_pose_indexes': coincident, 'look': look})

    return {
        'schema_version': 1,
        'sweep_id': data['sweep_id'],
        'status': 'pass' if all(c['status'] == 'pass' for c in checks) else 'fail',
        'validation_mode': 'static-boom-sweep-presentation',
        'runtime_validation': 'not-run',
        'collision_validation': 'not-run',
        'comfort_validation': 'not-run',
        'limits': [
            'authored boom-arm length/elevation/azimuth sampling only',
            'no world collision, mesh probe, or camera-anti-clip solve',
            'no gameplay targeting, lock eligibility, hit or movement rules',
            'FOV/offset references are recorded, not fov-comfort validated',
            'inputs are authored declarations, not measured camera traces',
        ],
        'pose_count': len(poses),
        'poses': poses,
        'checks': checks,
    }


def unique(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key: ' + k)
        result[k] = v
    return result


def reject_constant(value):
    raise ValueError('non-finite JSON constant: ' + value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', type=Path, help='New JSON report; never overwrite input or previous evidence')
    args = parser.parse_args()
    try:
        with args.plan.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('plan exceeds 4 MiB limit')
        data = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
        result = evaluate(data)
        result.update(
            input_sha256=hashlib.sha256(raw).hexdigest(),
            tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        )
        output = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(output)
        else:
            print(output, end='')
        return 0 if result['status'] == 'pass' else 1
    except (ValueError, OSError, TypeError, OverflowError, RecursionError) as error:
        print(json.dumps({'status': 'blocked', 'reason': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
