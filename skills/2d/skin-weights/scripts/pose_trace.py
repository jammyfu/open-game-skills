"""Evaluate a motion on the rig with linear blend skinning and export the trace.

Output follows `ogs.skin-trace/1` (spine-skeletal audit contract), so
audit_skin.py and measure_surface.py run on it unchanged. Two-bone IK is solved
analytically; an unreachable target is reported, never fixed by stretching.
Follow-contacts (an effector that must stay on a moving target, e.g. a foot on a
pedal) are measured in the companion report. Exit 0 ok, 1 measured failure,
2 invalid input. This evaluator is a reference; the shipping runtime must
export its own trace for final evidence.
"""
import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

from skinlib import (MOTION_SCHEMA, SkinError, apply, forward, load_mesh, load_rig, read_json, require, rotation_of,
                     sha256, write_json)


RIGID_EPSILON = 0.05  # world units


def sample_track(keys, t):
    """Value at time t. A key's value holds from its own timestamp, so a sample exactly on a key returns that key."""
    if t <= keys[0]['t']:
        return keys[0]['v']
    for a, b in zip(keys, keys[1:]):
        if t < b['t']:
            if a.get('curve') == 'stepped':
                return a['v']
            u = (t - a['t']) / (b['t'] - a['t'])
            if a.get('curve') == 'smooth':
                u = u*u*(3 - 2*u)
            return a['v'] + (b['v'] - a['v'])*u
    return keys[-1]['v']


def load_motion(path, rig):
    motion = read_json(path)
    require(motion.get('schema') == MOTION_SCHEMA, f'{path}: expected schema {MOTION_SCHEMA}')
    require(motion.get('sampleRate', 0) > 0 and motion.get('duration', 0) > 0, 'motion needs positive sampleRate and duration')
    for track in motion.get('tracks', []):
        require(track['bone'] in rig['_bones'], f'track bone {track["bone"]} unknown')
        require(track['property'] in ('rotate', 'x', 'y'), 'track property must be rotate, x or y (no scale/shear by design)')
        keys = track['keys']
        require(keys and all(isinstance(k['v'], (int, float)) for k in keys), 'track keys need numeric v')
        require(all(b['t'] > a['t'] for a, b in zip(keys, keys[1:])), 'track key times must increase')
    for ik in motion.get('ik', []):
        upper, lower = ik['bones']
        require(rig['_bones'][lower].get('parent') == upper, f'IK {ik["name"]}: {lower} must be a child of {upper}')
        for name in (upper, lower):
            require(rig['_bones'][name].get('inheritRotation', True),
                    f'IK {ik["name"]}: {name} has inheritRotation false; the analytic solver assumes both bones inherit rotation')
        bone = rig['_bones'][lower]
        require(abs(bone.get('x', 0) - rig['_bones'][upper]['length']) < 1e-6 and abs(bone.get('y', 0)) < 1e-6,
                f'IK {ik["name"]}: {lower} must start at the tip of {upper}')
        require(ik.get('bend', 1) in (1, -1), 'IK bend must be 1 or -1')
    return motion


def target_point(spec, world):
    if 'fixed' in spec:
        return np.array(spec['fixed'], dtype=float)
    return apply(world[spec['bone']], spec.get('point', [0, 0]))


def effector_point(rig, spec, world):
    bone = spec['bone']
    point = spec.get('point', [rig['_bones'][bone].get('length', 0), 0])
    return apply(world[bone], point)


def solve_ik(rig, ik, offsets, world, tolerance):
    upper, lower = ik['bones']
    l1, l2 = rig['_bones'][upper]['length'], rig['_bones'][lower]['length']
    start = world[upper][4:6]
    target = target_point(ik['target'], world)
    delta = target - start
    distance = float(np.hypot(*delta))
    problem = None
    if distance > l1 + l2 + tolerance or distance < abs(l1 - l2) - tolerance:
        problem = f'IK {ik["name"]}: target at {distance:.4f} outside reach [{abs(l1-l2):.4f}, {l1+l2:.4f}]'
    d = min(max(distance, abs(l1 - l2) + 1e-9), l1 + l2 - 1e-9)
    bend = ik.get('bend', 1)
    inner = math.acos(max(-1, min(1, (l1*l1 + d*d - l2*l2) / (2*l1*d))))
    knee = math.acos(max(-1, min(1, (l1*l1 + l2*l2 - d*d) / (2*l1*l2))))
    upper_world = math.degrees(math.atan2(delta[1], delta[0]) - bend*inner)
    parent = rig['_bones'][upper].get('parent')
    parent_rotation = rotation_of(world[parent]) if parent else 0.0
    setup = rig['_bones'][upper].get('rotation', 0)
    offsets.setdefault(upper, {})['rotate'] = upper_world - parent_rotation - setup
    offsets.setdefault(lower, {})['rotate'] = math.degrees(bend*(math.pi - knee)) - rig['_bones'][lower].get('rotation', 0)
    return problem


def evaluate(rig, motion, t, tolerance):
    offsets = {}
    for track in motion.get('tracks', []):
        offsets.setdefault(track['bone'], {})[track['property']] = offsets.get(track['bone'], {}).get(track['property'], 0) + sample_track(track['keys'], t)
    world = forward(rig, offsets)
    problems = []
    for ik in motion.get('ik', []):
        problem = solve_ik(rig, ik, offsets, world, tolerance)
        if problem:
            problems.append(problem)
        world = forward(rig, offsets)
    return world, problems, offsets


def deform(part_weights, world):
    out = np.zeros((len(part_weights), 2))
    for index, row in enumerate(part_weights):
        for item in row:
            out[index] += item['weight']*apply(world[item['bone']], [item['x'], item['y']])
    return out


def trace(rig, mesh, weights, motion, out_path, tolerances):
    rate, duration = motion['sampleRate'], motion['duration']
    count = int(round(duration*rate))
    require(abs(count/rate - duration) < 1e-9, 'duration must be a whole number of samples')
    setup_world = forward(rig)
    frames, problems, contact_rows = [], [], []
    rigidity = {}  # part -> bone -> worst distance of its dominated vertices from that bone's rigid motion
    dominated = {}
    for name in rig['drawOrder']:
        rows = weights['parts'][name]['weights']
        if len({i['bone'] for row in rows for i in row}) < 2:
            continue
        for bone in {i['bone'] for row in rows for i in row}:
            radius = weights['parts'][name].get('options', {}).get('handleRadius')
            radius = radius.get(bone) if isinstance(radius, dict) else radius
            picks = [(k, next(i for i in row if i['bone'] == bone)) for k, row in enumerate(rows)
                     if any(i['bone'] == bone and i['weight'] >= 0.5 and (radius is None or abs(i['y']) <= radius) for i in row)]
            ids = [k for k, _ in picks]
            local = np.array([[i['x'], i['y']] for _, i in picks]).reshape(-1, 2)
            length = rig['_bones'][bone].get('length', 0)
            along = np.clip(local[:, 0]/length, 0, 1) if length else np.zeros(len(ids))
            dominated[(name, bone)] = (ids, local, along, np.zeros(len(ids)))
    contacts = motion.get('contacts', [])
    worst = {c['name']: 0.0 for c in contacts}
    for index in range(count + 1):
        t = index / rate
        world, issues, _ = evaluate(rig, motion, t, tolerances['ik'])
        problems += [f'frame {index}: {issue}' for issue in issues]
        posed = {name: deform(weights['parts'][name]['weights'], world) for name in rig['drawOrder']}
        for (name, bone), (ids, local, along, peak) in dominated.items():
            if ids:
                np.maximum(peak, np.linalg.norm(posed[name][ids] - apply(world[bone], local), axis=1), out=peak)
        meshes = {name: v.round(7).ravel().tolist() for name, v in posed.items()}
        frames.append({'t': round(t, 9), 'bones': {b: dict(zip('abcdxy', np.round(m, 9).tolist())) for b, m in world.items()}, 'meshes': meshes})
        for contact in contacts:
            if contact['first'] <= index <= contact['last']:
                gap = float(np.linalg.norm(effector_point(rig, contact['effector'], world) - target_point(contact['target'], world)))
                worst[contact['name']] = max(worst[contact['name']], gap)
    for (name, bone), (ids, local, along, deviation) in dominated.items():
        if not ids:
            continue
        bins = np.minimum((along*20).astype(int), 19)
        occupied = set(bins.tolist())
        soft = set(bins[deviation > RIGID_EPSILON].tolist())
        rigidity.setdefault(name, {})[bone] = {'softLengthFraction': round(len(soft)/len(occupied), 3),
                                               'maxDeviation': round(float(deviation.max()), 6)}
    for contact in contacts:
        passed = worst[contact['name']] <= contact['tolerance']
        contact_rows.append({'name': contact['name'], 'maxGap': worst[contact['name']], 'tolerance': contact['tolerance'], 'passed': passed})
    segments = []
    translated = {t['bone'] for t in motion.get('tracks', []) if t['property'] in ('x', 'y')}
    for bone in rig['bones']:
        parent = bone.get('parent')
        if parent and bone['name'] not in translated:  # animated offsets are not pinned lengths
            length = float(np.linalg.norm(setup_world[bone['name']][4:6] - setup_world[parent][4:6]))
            if length > 1e-9:
                segments.append({'a': parent, 'b': bone['name'], 'length': length})
    base = Path(out_path).resolve().parent
    meshes = {}
    for name in rig['drawOrder']:
        m, part = mesh['parts'][name], next(p for p in rig['parts'] if p['name'] == name)
        image = rig['_path'].parent / part['image']
        require(sha256(image) == m.get('sha256'), f'part {name}: {part["image"]} changed after the mesh was built; rebuild mesh and weights')
        meshes[name] = {'image': os.path.relpath(image, base), 'sha256': sha256(image), 'uvs': m['uvs'].ravel().tolist(),
                        'triangles': m['triangles'].ravel().tolist(), 'weights': weights['parts'][name]['weights'],
                        'setupVertices': m['vertices'].ravel().tolist()}
    result = {'schema': 'ogs.skin-trace/1', 'sampleRate': rate,
              'tolerances': {k: tolerances[k] for k in ('length', 'scale', 'loop', 'weights', 'area', 'alphaThreshold')},
              'boneScales': {b['name']: [1, 1] for b in rig['bones']}, 'segments': segments, 'meshes': meshes, 'frames': frames,
              'loops': [{'first': 0, 'last': count}] if motion.get('loop') else [], 'contacts': motion.get('fixedContacts', []),
              'drawOrder': rig['drawOrder'],
              # review-only extras (the audit ignores them): hierarchy/lengths and the constraints that drove the pose
              'skeleton': [{'name': b['name'], 'parent': b.get('parent'), 'length': b.get('length', 0)} for b in rig['bones']],
              'constraints': {'ik': motion.get('ik', []), 'contacts': motion.get('contacts', [])},
              'provenance': {'exporter': 'skin-weights/pose_trace.py reference LBS evaluator', 'rigSHA256': sha256(rig['_path']),
                             'scope': motion.get('scope', 'technical-deformation-study'), 'runtimeTrace': False}}
    report = {'status': 'FAIL' if problems or not all(r['passed'] for r in contact_rows) else 'PASS',
              'samples': count + 1, 'ikProblems': problems[:50], 'ikProblemCount': len(problems), 'followContacts': contact_rows,
              'rigidityDeviation': rigidity,
              'rigidityNote': f'per bone, over vertices it dominates (w>=0.5) inside its handleRadius tube: softLengthFraction = share of the bone length (20 bins) whose vertices leave that bone\'s rigid motion by more than {RIGID_EPSILON} world units at some sample; a high value on a thin limb means it visibly bends like rubber'}
    return result, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('rig', 'mesh', 'weights', 'motion'):
        parser.add_argument(name)
    parser.add_argument('--out', required=True)
    parser.add_argument('--report')
    parser.add_argument('--alpha-threshold', type=int, default=32)
    args = parser.parse_args()
    tolerances = {'length': 1e-5, 'scale': 1e-6, 'loop': 1e-5, 'weights': 1e-6, 'area': 1e-10,
                  'alphaThreshold': args.alpha_threshold, 'ik': 1e-6}
    try:
        rig = load_rig(args.rig)
        mesh = load_mesh(args.mesh)
        weights = read_json(args.weights)
        require(weights.get('rigSHA256') == sha256(rig['_path']) and mesh.get('rigSHA256') == sha256(rig['_path']), 'mesh/weights belong to a different rig file')
        require(weights.get('meshSHA256') == sha256(args.mesh), 'weights belong to a different mesh file')
        motion = load_motion(args.motion, rig)
        result, report = trace(rig, mesh, weights, motion, args.out, tolerances)
    except (SkinError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'BLOCKED', 'errors': [str(error)]}, indent=1))
        sys.exit(2)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, separators=(',', ':'), allow_nan=False) + '\n')
    if args.report:
        write_json(args.report, report)
    print(json.dumps(report, indent=1))
    sys.exit(0 if report['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
