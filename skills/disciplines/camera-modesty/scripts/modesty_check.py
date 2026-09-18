"""Offline camera-modesty preflight. Not a renderer, cloth sim or collision solve."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

EPS = 1e-7
MAX_BYTES = 4 * 1024 * 1024
MAX_RAY_M = 64.0
ROOT_FIELDS = ['schema_version', 'scene_id', 'units', 'basis', 'policy',
               'characters', 'poses', 'boom_sweeps']
POLICY_FIELDS = ['mode', 'max_upward_elevation_deg', 'min_private_clearance_m',
                 'min_private_screen_distance_m', 'max_private_fov_at_close_deg']
CHARACTER_FIELDS = ['id', 'proxy', 'up', 'landmarks', 'private_zones']
POSE_FIELDS = ['id', 'position', 'forward', 'up', 'fov_v_deg', 'near_m', 'aspect',
               'authored_intent']
ZONE_FIELDS = ['id', 'kind', 'bounds', 'class']
SWEEP_FIELDS = ['id', 'pose_ids']
LANDMARKS = ['hem', 'hip', 'chest']
MODES = {'modest', 'adult', 'medical-exam'}
INTENTS = {'none', 'adult', 'medical-exam'}
ZONE_CLASSES = {'groin', 'chest', 'under-hem'}


def fields(value, required, where):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f'{where}: expected fields {sorted(required)}')


def number(value, where, minimum=None, maximum=None, positive=False):
    if type(value) not in (int, float) or isinstance(value, bool) or not math.isfinite(value):
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


def box(value, where):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f'{where}: expected [min, max] world-space bounds')
    low, high = (vector(v, where) for v in value)
    if any(a >= b for a, b in zip(low, high)):
        raise ValueError(f'{where}: bounds must have positive extent on every axis')
    return low, high


def text(value, where, limit=120):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'{where}: expected nonempty text of at most {limit} characters')
    return value


def add(a, b):
    return [a[i] + b[i] for i in range(3)]


def sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def mul(a, s):
    return [a[i] * s for i in range(3)]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def length(a):
    return math.sqrt(dot(a, a))


def norm(a, where):
    size = length(a)
    if size <= EPS:
        raise ValueError(f'{where}: zero vector')
    return [v / size for v in a]


def clamp(value, lo, hi):
    return lo if value < lo else hi if value > hi else value


def height_along(point, origin, up):
    return dot(sub(point, origin), up)


def project_horizontal(vec, up):
    return sub(vec, mul(up, dot(vec, up)))


def intersects(a, b):
    return all(min(a[1][i], b[1][i]) - max(a[0][i], b[0][i]) > EPS for i in range(3))


def aabb_distance(point, low, high):
    closest = [min(max(point[i], low[i]), high[i]) for i in range(3)]
    return length(sub(point, closest)), closest


def aabb_center(low, high):
    return [(low[i] + high[i]) * 0.5 for i in range(3)]


def ray_aabb(origin, direction, low, high, far=MAX_RAY_M):
    tmin, tmax = 0.0, far
    for i in range(3):
        if abs(direction[i]) <= EPS:
            if origin[i] < low[i] - EPS or origin[i] > high[i] + EPS:
                return False, None
            continue
        inv = 1.0 / direction[i]
        first, second = (low[i] - origin[i]) * inv, (high[i] - origin[i]) * inv
        tmin = max(tmin, min(first, second))
        tmax = min(tmax, max(first, second))
        if tmin - EPS > tmax:
            return False, None
    if tmax < -EPS:
        return False, None
    return True, tmin if tmin >= 0 else 0.0


def unique_id(value, ids, where):
    name = text(value, where)
    if name in ids:
        raise ValueError('duplicate object id: ' + name)
    ids.add(name)
    return name


def validate_proxy(value, where):
    if not isinstance(value, dict) or value.get('kind') not in ('capsule', 'aabb'):
        raise ValueError(f'{where}: proxy.kind must be capsule or aabb')
    if value['kind'] == 'capsule':
        fields(value, ['kind', 'origin', 'height', 'radius'], where)
        origin = vector(value['origin'], where + '.origin')
        height = number(value['height'], where + '.height', positive=True)
        radius = number(value['radius'], where + '.radius', positive=True)
        return {'kind': 'capsule', 'origin': origin, 'height': height, 'radius': radius}
    fields(value, ['kind', 'bounds'], where)
    return {'kind': 'aabb', 'bounds': box(value['bounds'], where + '.bounds')}


def proxy_metrics(proxy, up):
    if proxy['kind'] == 'capsule':
        return proxy['origin'], proxy['radius'], proxy['height']
    low, high = proxy['bounds']
    origin = [(low[0] + high[0]) * 0.5, low[1], (low[2] + high[2]) * 0.5]
    radius = max((high[0] - low[0]) * 0.5, (high[2] - low[2]) * 0.5)
    height = high[1] - low[1]
    number(radius, 'derived proxy radius', positive=True)
    number(height, 'derived proxy height', positive=True)
    if abs(up[1] - 1.0) > 0.05:
        # World AABB still used; non-Y up is accepted but horizontal radius is conservative.
        extent = [high[i] - low[i] for i in range(3)]
        radius = max(extent) * 0.5
    return origin, radius, height


def derived_under_hem(origin, radius, hem, up):
    hem_h = height_along(hem, origin, up)
    if hem_h <= EPS:
        raise ValueError('hem must sit above the proxy origin along character up')
    # Conservative world AABB of a vertical capsule slice from origin to hem.
    low = [origin[0] - radius, min(origin[1], hem[1]), origin[2] - radius]
    high = [origin[0] + radius, max(origin[1], hem[1]), origin[2] + radius]
    if any(a >= b for a, b in zip(low, high)):
        raise ValueError('derived under-hem bounds must have positive extent')
    return low, high


def near_plane_aabb(pose):
    fwd, cam_up = pose['forward'], pose['up']
    right = norm(cross(fwd, cam_up), 'camera right')
    true_up = cross(right, fwd)
    center = add(pose['position'], mul(fwd, pose['near_m']))
    half_h = pose['near_m'] * math.tan(math.radians(pose['fov_v_deg'] * 0.5))
    half_w = half_h * pose['aspect']
    number(half_h, 'derived near half-height', positive=True)
    number(half_w, 'derived near half-width', positive=True)
    corners = [add(add(center, mul(right, sx * half_w)), mul(true_up, sy * half_h))
               for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1))]
    low = [min(c[i] for c in corners) for i in range(3)]
    high = [max(c[i] for c in corners) for i in range(3)]
    for i in range(3):
        if high[i] - low[i] <= EPS:
            low[i] -= EPS
            high[i] += EPS
    return low, high


def validate(data):
    fields(data, ROOT_FIELDS, 'framing')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('unsupported schema_version')
    if data['units'] != 'm' or data['basis'] != 'right-handed-y-up':
        raise ValueError('v1 requires meters and right-handed-y-up world-space bounds')
    text(data['scene_id'], 'scene_id')
    policy = data['policy']
    fields(policy, POLICY_FIELDS, 'policy')
    if policy['mode'] not in MODES:
        raise ValueError('policy.mode must be modest, adult or medical-exam')
    number(policy['max_upward_elevation_deg'], 'max_upward_elevation_deg', minimum=0, maximum=89)
    number(policy['min_private_clearance_m'], 'min_private_clearance_m', positive=True)
    number(policy['min_private_screen_distance_m'], 'min_private_screen_distance_m', positive=True)
    number(policy['max_private_fov_at_close_deg'], 'max_private_fov_at_close_deg', minimum=1, maximum=179)
    characters = data['characters']
    poses = data['poses']
    sweeps = data['boom_sweeps']
    if not isinstance(characters, list) or not 1 <= len(characters) <= 32:
        raise ValueError('characters: invalid list size (maximum 32)')
    if not isinstance(poses, list) or not 1 <= len(poses) <= 256:
        raise ValueError('poses: invalid list size (maximum 256)')
    if not isinstance(sweeps, list) or len(sweeps) > 64:
        raise ValueError('boom_sweeps: invalid list size (maximum 64)')
    ids: set[str] = set()
    parsed_characters = []
    for row in characters:
        fields(row, CHARACTER_FIELDS, 'character')
        cid = unique_id(row['id'], ids, 'character.id')
        up = norm(vector(row['up'], cid + '.up'), cid + '.up')
        proxy = validate_proxy(row['proxy'], cid + '.proxy')
        origin, radius, height = proxy_metrics(proxy, up)
        marks = row['landmarks']
        fields(marks, LANDMARKS, cid + '.landmarks')
        landmarks = {name: vector(marks[name], f'{cid}.{name}') for name in LANDMARKS}
        hem_h = height_along(landmarks['hem'], origin, up)
        hip_h = height_along(landmarks['hip'], origin, up)
        chest_h = height_along(landmarks['chest'], origin, up)
        if hem_h + EPS < 0 or hip_h + EPS < hem_h or chest_h <= hip_h:
            raise ValueError(f'{cid}: landmarks must be ordered hem <= hip < chest along character up')
        if hip_h - EPS > height or chest_h - EPS > height + radius:
            raise ValueError(f'{cid}: landmarks exceed the declared proxy height')
        zones = row['private_zones']
        if not isinstance(zones, list) or not 1 <= len(zones) <= 16:
            raise ValueError(f'{cid}.private_zones: invalid list size (maximum 16)')
        parsed_zones = []
        for zone in zones:
            fields(zone, ZONE_FIELDS, cid + '.zone')
            zid = unique_id(zone['id'], ids, 'zone.id')
            if zone['kind'] != 'aabb' or zone['class'] not in ZONE_CLASSES:
                raise ValueError(f'{zid}: zone kind must be aabb and class groin, chest or under-hem')
            parsed_zones.append({'id': zid, 'class': zone['class'],
                                 'bounds': box(zone['bounds'], zid + '.bounds')})
        parsed_characters.append({
            'id': cid, 'proxy': proxy, 'up': up, 'origin': origin, 'radius': radius,
            'height': height, 'landmarks': landmarks, 'private_zones': parsed_zones,
            'under_hem': derived_under_hem(origin, radius, landmarks['hem'], up),
        })
    parsed_poses = []
    for row in poses:
        fields(row, POSE_FIELDS, 'pose')
        pid = unique_id(row['id'], ids, 'pose.id')
        if row['authored_intent'] not in INTENTS:
            raise ValueError(f'{pid}: authored_intent must be none, adult or medical-exam')
        position = vector(row['position'], pid + '.position')
        forward = norm(vector(row['forward'], pid + '.forward'), pid + '.forward')
        cam_up = norm(vector(row['up'], pid + '.up'), pid + '.up')
        if length(cross(forward, cam_up)) <= EPS:
            raise ValueError(f'{pid}: forward and up must not be parallel')
        parsed_poses.append({
            'id': pid, 'position': position, 'forward': forward, 'up': cam_up,
            'fov_v_deg': number(row['fov_v_deg'], pid + '.fov_v_deg', minimum=1, maximum=179),
            'near_m': number(row['near_m'], pid + '.near_m', positive=True),
            'aspect': number(row['aspect'], pid + '.aspect', positive=True),
            'authored_intent': row['authored_intent'],
        })
        near_plane_aabb(parsed_poses[-1])
    pose_ids = {p['id'] for p in parsed_poses}
    parsed_sweeps = []
    for row in sweeps:
        fields(row, SWEEP_FIELDS, 'boom_sweep')
        sid = unique_id(row['id'], ids, 'boom_sweep.id')
        listed = row['pose_ids']
        if not isinstance(listed, list) or not 1 <= len(listed) <= 256:
            raise ValueError(f'{sid}: pose_ids must be a nonempty list of at most 256 ids')
        if not all(isinstance(v, str) for v in listed):
            raise ValueError(f'{sid}: pose_ids must contain strings')
        if len(listed) != len(set(listed)):
            raise ValueError(f'{sid}: duplicate pose id in boom sweep')
        missing = [v for v in listed if v not in pose_ids]
        if missing:
            raise ValueError(f'{sid}: unknown pose id {missing[0]}')
        parsed_sweeps.append({'id': sid, 'pose_ids': list(listed)})
    return parsed_characters, parsed_poses, parsed_sweeps


def waived(policy_mode, intent):
    return policy_mode != 'modest' and intent == policy_mode


def look_elevation_deg(forward, up):
    return math.degrees(math.asin(clamp(dot(forward, up), -1.0, 1.0)))


def suggest_clamp(pose, character, policy, violations):
    if not violations:
        return None
    up = character['up']
    look = look_elevation_deg(pose['forward'], up)
    hem_h = height_along(character['landmarks']['hem'], character['origin'], up)
    cam_h = height_along(pose['position'], character['origin'], up)
    raise_pitch = 0.0
    raise_boom = 0.0
    pull_back = 0.0
    actions = []
    rules = {row['rule_id'] for row in violations}
    if rules & {'under-hem-look', 'between-legs'}:
        raise_pitch = max(0.0, look - policy['max_upward_elevation_deg'])
        raise_boom = max(0.0, hem_h + policy['min_private_clearance_m'] - cam_h)
        if 'between-legs' in rules:
            pull_back = max(pull_back, character['radius'] + policy['min_private_clearance_m'])
    distances = [row['observed']['distance_m'] for row in violations
                 if isinstance(row.get('observed'), dict) and type(row['observed'].get('distance_m')) is float]
    if rules & {'private-region-zoom', 'private-zone-proximity', 'near-plane-private-zone'}:
        if distances:
            pull_back = max(pull_back, policy['min_private_screen_distance_m'] - min(distances))
        else:
            pull_back = max(pull_back, policy['min_private_screen_distance_m'])
        pull_back = max(0.0, pull_back)
    if raise_pitch > EPS:
        actions.append('raise pitch')
    if pull_back > EPS:
        actions.append('pull back')
    if raise_boom > EPS:
        actions.append('raise boom')
    if not actions:
        actions.append('raise boom')
        raise_boom = max(raise_boom, policy['min_private_clearance_m'])
    return {'raise_pitch_deg': raise_pitch, 'pull_back_m': pull_back,
            'raise_boom_m': raise_boom, 'actions': actions}


def evaluate_pose(pose, characters, policy):
    checks = []
    violations = []
    skip = waived(policy['mode'], pose['authored_intent'])

    def record(rule_id, ok, observed, character_id=None, zone_id=None):
        entry = {'id': rule_id if character_id is None else
                 (f'{rule_id}:{pose["id"]}:{character_id}' if zone_id is None else
                  f'{rule_id}:{pose["id"]}:{character_id}:{zone_id}'),
                 'rule_id': rule_id, 'pose': pose['id'], 'status': 'pass' if ok else 'fail',
                 'observed': observed}
        if character_id is not None:
            entry['character'] = character_id
        if zone_id is not None:
            entry['zone'] = zone_id
        checks.append(entry)
        if not ok:
            violations.append(entry)
        return ok

    if skip:
        record('intent-opt-in', True, {'waived': True, 'mode': policy['mode'],
                                       'authored_intent': pose['authored_intent']})
        return checks, violations, None

    near = near_plane_aabb(pose)
    for character in characters:
        up = character['up']
        origin = character['origin']
        hem = character['landmarks']['hem']
        hip = character['landmarks']['hip']
        cam = pose['position']
        cam_h = height_along(cam, origin, up)
        hem_h = height_along(hem, origin, up)
        hip_h = height_along(hip, origin, up)
        horiz = length(project_horizontal(sub(cam, origin), up))
        look = look_elevation_deg(pose['forward'], up)
        below_hem = cam_h <= hem_h + EPS
        near_axis = horiz <= character['radius'] * 2 + EPS
        hit, hit_t = ray_aabb(cam, pose['forward'], *character['under_hem'])
        under = below_hem and (hit or (look > policy['max_upward_elevation_deg'] and near_axis))
        record('under-hem-look', not under, {
            'camera_below_hem': below_hem, 'look_elevation_deg': look,
            'horizontal_distance_m': horiz, 'ray_hits_under_hem': bool(hit),
            'hit_distance_m': hit_t,
        }, character['id'])
        between = horiz + EPS < character['radius'] and 0 <= cam_h + EPS and cam_h + EPS < hip_h
        record('between-legs', not between, {
            'horizontal_distance_m': horiz, 'height_along_up_m': cam_h, 'hip_height_m': hip_h,
        }, character['id'])
        for zone in character['private_zones']:
            low, high = zone['bounds']
            distance, _ = aabb_distance(cam, low, high)
            center = aabb_center(low, high)
            in_front = dot(sub(center, cam), pose['forward']) > EPS
            record('near-plane-private-zone', not intersects(near, zone['bounds']), {
                'distance_m': distance, 'near_plane_overlap': intersects(near, zone['bounds']),
            }, character['id'], zone['id'])
            record('private-zone-proximity', distance + EPS >= policy['min_private_clearance_m'], {
                'distance_m': distance, 'min_private_clearance_m': policy['min_private_clearance_m'],
            }, character['id'], zone['id'])
            zoom = (zone['class'] in ('groin', 'chest') and in_front
                    and distance < policy['min_private_screen_distance_m']
                    and pose['fov_v_deg'] > policy['max_private_fov_at_close_deg'])
            record('private-region-zoom', not zoom, {
                'distance_m': distance, 'in_front': in_front, 'fov_v_deg': pose['fov_v_deg'],
                'class': zone['class'],
            }, character['id'], zone['id'])
    clamp_hint = suggest_clamp(pose, characters[0], policy, violations)
    return checks, violations, clamp_hint


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    characters, poses, sweeps = validate(data)
    policy = data['policy']
    checks = []
    pose_rows = []
    failed_poses = set()
    for pose in poses:
        pose_checks, violations, clamp_hint = evaluate_pose(pose, characters, policy)
        checks.extend(pose_checks)
        failed = any(row['status'] == 'fail' for row in pose_checks)
        if failed:
            failed_poses.add(pose['id'])
        pose_rows.append({
            'id': pose['id'],
            'status': 'fail' if failed else 'pass',
            'violations': [{'rule_id': row['rule_id'], 'character': row.get('character'),
                            'zone': row.get('zone')} for row in violations],
            'suggested_clamp': clamp_hint,
        })
    sweep_rows = []
    for sweep in sweeps:
        bad = [pid for pid in sweep['pose_ids'] if pid in failed_poses]
        ok = not bad
        checks.append({'id': 'boom-sweep:' + sweep['id'], 'rule_id': 'boom-sweep',
                       'status': 'pass' if ok else 'fail',
                       'observed': {'pose_ids': sweep['pose_ids'], 'failed_pose_ids': bad}})
        sweep_rows.append({'id': sweep['id'], 'status': 'pass' if ok else 'fail',
                           'pose_ids': sweep['pose_ids'], 'failed_pose_ids': bad})
    status = 'pass' if all(c['status'] == 'pass' for c in checks) else 'fail'
    return {
        'schema_version': 1, 'scene_id': data['scene_id'], 'status': status,
        'validation_mode': 'static-modesty-preflight', 'runtime_validation': 'not-run',
        'policy_mode': policy['mode'],
        'limits': [
            'declared AABB/capsule proxies and landmarks only',
            'no mesh, cloth, animation, collision or engine camera solve',
            'boom sweeps aggregate declared poses; they do not sample a curve',
            'inputs are declarations, not verified body measurements',
        ],
        'poses': pose_rows, 'sweeps': sweep_rows, 'checks': checks,
    }


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('non-finite JSON constant: ' + value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('framing', type=Path)
    parser.add_argument('--output', type=Path, help='New JSON report; never overwrite input or previous evidence')
    args = parser.parse_args()
    try:
        with args.framing.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('framing exceeds 4 MiB limit')
        data = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
        result = evaluate(data)
        result.update(input_sha256=hashlib.sha256(raw).hexdigest(),
                      tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
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
