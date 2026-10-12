"""Offline AABB layout preflight. Not a mesh importer, physics test or clear proof."""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

EPS = 1e-7  # Arithmetic tolerance in meters, not a design clearance.
MAX_BYTES = 4 * 1024 * 1024


def fields(value, required, where):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f'{where}: expected fields {sorted(required)}')


def number(value, where, minimum=None, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f'{where}: expected finite number, not boolean')
    if (minimum is not None and value < minimum) or (positive and value <= 0):
        raise ValueError(f'{where}: number out of range')
    return value


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


def text(value, where):
    if not isinstance(value, str) or not value.strip() or len(value) > 120:
        raise ValueError(f'{where}: expected nonempty text of at most 120 characters')


def contains(outer, inner):
    return all(outer[0][i] - EPS <= inner[0][i] and inner[1][i] <= outer[1][i] + EPS for i in range(3))


def intersects(a, b):
    return all(min(a[1][i], b[1][i]) - max(a[0][i], b[0][i]) > EPS for i in range(3))


def validate(data):
    fields(data, ['schema_version', 'layout_id', 'units', 'basis', 'player',
                  'rooms', 'solids', 'spawns', 'portals', 'required_rooms'], 'layout')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('unsupported schema_version')
    if data['units'] != 'm' or data['basis'] != 'right-handed-y-up':
        raise ValueError('v1 requires meters and right-handed-y-up world-space bounds')
    text(data['layout_id'], 'layout_id')
    fields(data['player'], ['radius', 'height', 'clearance', 'max_step'], 'player')
    for k in ['radius', 'height']:
        number(data['player'][k], k, positive=True)
    for k in ['clearance', 'max_step']:
        number(data['player'][k], k, minimum=0)
    shapes = {
        'rooms': (['id', 'bounds'], 128, True),
        'solids': (['id', 'bounds'], 512, False),
        'spawns': (['id', 'room', 'position'], 64, True),
        'portals': (['id', 'rooms', 'axis', 'center', 'width', 'height'], 256, False),
    }
    ids = set()
    for group, (keys, limit, nonempty) in shapes.items():
        rows = data[group]
        if not isinstance(rows, list) or len(rows) > limit or (nonempty and not rows):
            raise ValueError(f'{group}: invalid list size (maximum {limit})')
        for row in rows:
            fields(row, keys, group)
            text(row['id'], group + '.id')
            if row['id'] in ids: raise ValueError('duplicate object id: ' + row['id'])
            ids.add(row['id'])
            if 'bounds' in row: box(row['bounds'], row['id'])
    rooms = {r['id']: r['bounds'] for r in data['rooms']}
    for row in data['spawns']:
        text(row['room'], 'spawn.room')
        if row['room'] not in rooms: raise ValueError('unknown spawn room')
        vector(row['position'], 'spawn.position')
    for row in data['portals']:
        links = row['rooms']
        if not isinstance(links, list) or len(links) != 2 or not all(isinstance(v, str) for v in links):
            raise ValueError('portal.rooms must contain two room ids')
        if links[0] == links[1] or any(k not in rooms for k in links):
            raise ValueError('portal needs two distinct known rooms')
        if row['axis'] not in ('x', 'z'): raise ValueError('portal.axis must be x or z')
        vector(row['center'], 'portal.center')
        number(row['width'], 'portal.width', positive=True)
        number(row['height'], 'portal.height', positive=True)
    goals = data['required_rooms']
    if not isinstance(goals, list) or not goals or not all(isinstance(v, str) and v in rooms for v in goals):
        raise ValueError('required_rooms must be nonempty and reference known rooms')
    if len(goals) != len(set(goals)): raise ValueError('duplicate required room')
    # Catch overflowing derived dimensions even for adversarial finite inputs.
    p = data['player']
    number(p['radius'] + p['clearance'], 'derived radius')
    number(2 * (p['radius'] + p['clearance']), 'derived width')
    number(p['height'] + p['clearance'], 'derived height')
    return rooms


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    rooms = validate(data)
    checks = []

    def check(name, ok, observed):
        checks.append({'id': name, 'status': 'pass' if ok else 'fail', 'observed': observed})
        return ok

    player = data['player']; radius = player['radius'] + player['clearance']
    height = player['height'] + player['clearance']
    keys = list(rooms)
    overlaps = [[a, b] for i, a in enumerate(keys) for b in keys[i + 1:] if intersects(rooms[a], rooms[b])]
    check('room-interiors-disjoint', not overlaps, {'overlaps': overlaps})
    for row in data['solids']:
        check('solid-contained:' + row['id'], any(contains(r, row['bounds']) for r in rooms.values()), {'solid': row['id']})
    for row in data['spawns']:
        x, y, z = row['position']; room = rooms[row['room']]
        body = [[x - radius, y, z - radius], [x + radius, y + height, z + radius]]
        box(body, 'derived spawn body')
        collisions = [s['id'] for s in data['solids'] if intersects(body, s['bounds'])]
        check('spawn-clear:' + row['id'], contains(room, body) and abs(y - room[0][1]) <= EPS and not collisions,
              {'body_aabb': body, 'blocking_solids': collisions, 'on_declared_floor': abs(y - room[0][1]) <= EPS})
    adjacency = {k: set() for k in rooms}
    for row in data['portals']:
        aid, bid = row['rooms']; a, b = rooms[aid], rooms[bid]
        axis = 0 if row['axis'] == 'x' else 2; lateral = 2 if axis == 0 else 0
        center = row['center']; at = center[axis]; side = center[lateral]; y = center[1]
        shared = ((abs(a[1][axis] - b[0][axis]) <= EPS and abs(at - a[1][axis]) <= EPS)
                  or (abs(b[1][axis] - a[0][axis]) <= EPS and abs(at - b[1][axis]) <= EPS))
        lateral_fit = all(r[0][lateral] - EPS <= side - row['width'] / 2 and
                          side + row['width'] / 2 <= r[1][lateral] + EPS for r in [a, b])
        floor_fit = abs(y - max(a[0][1], b[0][1])) <= EPS
        step_fit = abs(a[0][1] - b[0][1]) <= player['max_step'] + EPS
        ceiling_fit = y + row['height'] <= min(a[1][1], b[1][1]) + EPS
        size_fit = row['width'] + EPS >= 2 * radius and row['height'] + EPS >= height
        # Centered crossing; not a navmesh or a search for alternate lateral routes.
        sweep = [[v - radius for v in center], [v + radius for v in center]]
        sweep[0][1] = min(a[0][1], b[0][1]); sweep[1][1] = y + height
        union = [[min(a[0][i], b[0][i]) for i in range(3)], [max(a[1][i], b[1][i]) for i in range(3)]]
        depth_fit = union[0][axis] - EPS <= at - radius and at + radius <= union[1][axis] + EPS
        collisions = [s['id'] for s in data['solids'] if intersects(sweep, s['bounds'])]
        valid = all([shared, lateral_fit, floor_fit, step_fit, ceiling_fit, size_fit, depth_fit, not collisions])
        check('portal-fit:' + row['id'], valid, {'shared_boundary': shared, 'lateral_fit': lateral_fit,
              'floor_fit': floor_fit, 'step_fit': step_fit, 'ceiling_fit': ceiling_fit, 'size_fit': size_fit,
              'depth_fit': depth_fit, 'blocking_solids': collisions, 'required_width_m': 2 * radius,
              'required_height_m': height})
        if valid: adjacency[aid].add(bid); adjacency[bid].add(aid)
    for spawn in data['spawns']:
        seen = {spawn['room']}; pending = deque(seen)
        while pending:
            for other in sorted(adjacency[pending.popleft()]):
                if other not in seen: seen.add(other); pending.append(other)
        for goal in data['required_rooms']:
            check(f"reachable:{spawn['id']}:{goal}", goal in seen, {'room_graph_reachable': goal in seen})
    return {'schema_version': 1, 'layout_id': data['layout_id'],
            'status': 'pass' if all(c['status'] == 'pass' for c in checks) else 'fail',
            'validation_mode': 'static-layout-preflight', 'runtime_validation': 'not-run',
            'limits': ['declared solid AABBs and flat room floors only', 'centered, bidirectional portals only',
                       'no within-room pathfinding, locks, jumping, slopes, camera or collision-engine simulation',
                       'inputs are declarations, not verified mesh measurements'], 'checks': checks}


def unique(pairs):
    result = {}
    for k, v in pairs:
        if k in result: raise ValueError('duplicate JSON key: ' + k)
        result[k] = v
    return result


def reject_constant(value): raise ValueError('non-finite JSON constant: ' + value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('layout', type=Path)
    parser.add_argument('--output', type=Path, help='New JSON report; never overwrite input or previous evidence')
    args = parser.parse_args()
    try:
        with args.layout.open('rb') as stream: raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES: raise ValueError('layout exceeds 4 MiB limit')
        data = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
        result = evaluate(data)
        result.update(input_sha256=hashlib.sha256(raw).hexdigest(), tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        output = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream: stream.write(output)
        else: print(output, end='')
        return 0 if result['status'] == 'pass' else 1
    except (ValueError, OSError, TypeError, OverflowError, RecursionError) as error:
        print(json.dumps({'status': 'blocked', 'reason': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__': raise SystemExit(main())
