"""Runtime-independent technical audit. Never grants character/art acceptance."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def numbers(value, size, name):
    require(isinstance(value, list) and len(value) == size, f'{name}: expected {size} numbers')
    require(all(finite_number(n) for n in value), f'{name}: nonfinite/nonnumeric value')
    return np.asarray(value, dtype=float)


def area(vertices, triangles):
    a, b, c = (vertices[triangles[:, i]] for i in range(3))
    return (b[:, 0]-a[:, 0])*(c[:, 1]-a[:, 1])-(b[:, 1]-a[:, 1])*(c[:, 0]-a[:, 0])


def audit(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    data = json.loads(raw)
    require(isinstance(data, dict), 'Trace root must be an object')
    require(data.get('schema') == 'ogs.skin-trace/1', 'Unsupported/missing trace schema')
    tolerance = data['tolerances']
    require(isinstance(tolerance, dict), 'Tolerances must be an object')
    for key in ['length', 'scale', 'loop', 'weights', 'area']:
        require(finite_number(tolerance[key]) and tolerance[key] >= 0, f'Invalid tolerance: {key}')
    alpha_threshold = tolerance['alphaThreshold']
    require(type(alpha_threshold) is int and 0 <= alpha_threshold < 255, 'Invalid alpha threshold')
    rate = data['sampleRate']
    require(finite_number(rate) and rate > 0, 'Invalid sample rate')
    frames = data['frames']
    require(isinstance(frames, list) and len(frames) >= 2, 'At least two sampled poses are required')
    expected_scales = data['boneScales']
    require(isinstance(expected_scales, dict) and bool(expected_scales), 'Missing expected bone scales')
    for name, scale in expected_scales.items():
        require(np.all(numbers(scale, 2, name) > 0), f'{name}: expected scales must be positive')
    segments = data['segments']
    require(isinstance(segments, list) and bool(segments), 'Missing pinned segments')
    for segment in segments:
        require(segment['a'] in expected_scales and segment['b'] in expected_scales, 'Unknown segment bone')
        require(finite_number(segment['length']) and segment['length'] > 0, 'Invalid pinned length')
    definitions = data['meshes']
    require(isinstance(definitions, dict) and bool(definitions), 'No meshes declared')
    errors = []
    prepared = {}
    for name, definition in definitions.items():
        require(isinstance(definition, dict), f'{name}: mesh definition must be an object')
        uv = definition['uvs']
        require(isinstance(uv, list) and len(uv) >= 6 and len(uv) % 2 == 0, f'{name}: invalid UV array')
        uv = numbers(uv, len(uv), name).reshape(-1, 2)
        require(np.all((uv >= 0) & (uv <= 1)), f'{name}: UV outside source image')
        count = len(uv)
        tri = definition['triangles']
        require(isinstance(tri, list) and len(tri) >= 3 and len(tri) % 3 == 0, f'{name}: invalid triangles')
        require(all(type(i) is int and 0 <= i < count for i in tri), f'{name}: invalid triangle index')
        tri = np.array(tri, dtype=int).reshape(-1, 3)
        require(np.all(np.abs(area(uv, tri)) > 1e-12), f'{name}: degenerate UV triangles')
        setup = numbers(definition['setupVertices'], count*2, f'{name} setup').reshape(-1, 2)
        rest_area = area(setup, tri)
        require(np.all(np.isfinite(rest_area)), f'{name}: nonfinite computed setup areas')
        require(np.all(np.abs(rest_area) > tolerance['area']), f'{name}: degenerate setup triangles')
        bindings = definition['weights']
        require(isinstance(bindings, list) and len(bindings) == count, f'{name}: missing vertex weights')
        for index, weights in enumerate(bindings):
            require(isinstance(weights, list) and bool(weights), f'{name} vertex {index}: empty bindings')
            seen = set()
            total = 0
            for binding in weights:
                require(isinstance(binding, dict), f'{name} vertex {index}: binding must be an object')
                bone, weight = binding['bone'], binding['weight']
                require(bone in expected_scales and bone not in seen, f'{name} vertex {index}: unknown/duplicate bone')
                require(finite_number(weight) and weight >= 0, f'{name} vertex {index}: invalid weight')
                total += weight
                seen.add(bone)
            if total <= 0 or abs(total-1) > tolerance['weights']:
                errors.append(f'{name} vertex {index}: weights sum to {total}')
        image_path = path.parent / definition['image']
        image_bytes = image_path.read_bytes()
        actual_hash = hashlib.sha256(image_bytes).hexdigest()
        require(actual_hash == definition['sha256'], f'{name}: source hash mismatch')
        with Image.open(image_path) as original:
            image = original.convert('RGBA')
        alpha = np.array(image.getchannel('A'))
        require(bool((alpha > alpha_threshold).any()), f'{name}: source has no visible pixels')
        prepared[name] = dict(uv=uv, tri=tri, rest=rest_area, count=count, alpha=alpha,
                              bad=set(), sha256=actual_hash)
    max_length = max_scale = 0.0
    times = []
    vertices_by_frame = []
    for index, frame in enumerate(frames):
        require(isinstance(frame, dict), f'Frame {index}: pose must be an object')
        t = frame['t']
        require(finite_number(t), f'Frame {index}: invalid time')
        require(not times or t > times[-1], f'Frame {index}: nonincreasing time')
        if times and t-times[-1] > 1/rate + 1e-7:
            errors.append(f'Frame {index}: sample gap exceeds declared rate')
        times.append(t)
        require(isinstance(frame['bones'], dict) and isinstance(frame['meshes'], dict), f'Frame {index}: observations must be objects')
        require(set(frame['bones']) == set(expected_scales), f'Frame {index}: missing/extra bone observations')
        require(set(frame['meshes']) == set(prepared), f'Frame {index}: missing/extra mesh observations')
        for name, expected in expected_scales.items():
            bone = frame['bones'][name]
            require(isinstance(bone, dict), f'Frame {index} bone {name}: observation must be an object')
            a, b, c, d, x, y = numbers([bone[k] for k in ['a','b','c','d','x','y']], 6, f'Frame {index} bone {name}')
            error = max(abs(math.hypot(a, c)-expected[0]), abs(math.hypot(b, d)-expected[1]))
            # Unit column lengths alone do not exclude shear (nonorthogonal columns).
            shear = abs(a*b+c*d)
            max_scale = max(max_scale, error, shear)
            if error > tolerance['scale'] or shear > tolerance['scale']:
                errors.append(f'Frame {index} bone {name}: scale/shear drift')
        for segment in segments:
            a, b = (frame['bones'][segment[key]] for key in ['a','b'])
            error = abs(math.hypot(a['x']-b['x'], a['y']-b['y'])-segment['length'])
            max_length = max(max_length, error)
            if error > tolerance['length']:
                errors.append(f'Frame {index}: segment {segment["a"]}/{segment["b"]} length drift')
        observed = {}
        for name, mesh in prepared.items():
            verts = numbers(frame['meshes'][name], mesh['count']*2, f'Frame {index} mesh {name}').reshape(-1, 2)
            signed = area(verts, mesh['tri'])
            require(np.all(np.isfinite(signed)), f'Frame {index} mesh {name}: nonfinite computed areas')
            bad = np.flatnonzero((np.sign(signed) != np.sign(mesh['rest'])) | (np.abs(signed) <= tolerance['area']))
            mesh['bad'].update(bad.tolist())
            observed[name] = verts
        vertices_by_frame.append(observed)
    fold_report = {}
    for name, mesh in prepared.items():
        height, width = mesh['alpha'].shape
        mask = Image.new('L', (width, height))
        draw = ImageDraw.Draw(mask)
        for triangle in mesh['bad']:
            draw.polygon([(float(u*width), float(v*height)) for u, v in mesh['uv'][mesh['tri'][triangle]]], fill=255)
        visible = int(((np.array(mask) > 0) & (mesh['alpha'] > alpha_threshold)).sum())
        fold_report[name] = dict(badTriangles=len(mesh['bad']), visibleBadUVPixels=visible, sourceSHA256=mesh['sha256'])
        if visible:
            errors.append(f'{name}: {visible} visible source pixels in folded/collapsed triangles')
    def interval(item, allow_single=False):
        first, last = item['first'], item['last']
        require(type(first) is int and type(last) is int and 0 <= first <= last < len(frames)
                and (allow_single or first < last), 'Invalid interval indices')
        return first, last
    loops = data['loops']
    require(isinstance(loops, list), 'Missing loop declarations')
    max_loop = 0.0
    max_loop_bone_position = max_loop_bone_matrix = 0.0
    for loop in loops:
        first, last = interval(loop)
        for name in expected_scales:
            a, b = frames[first]['bones'][name], frames[last]['bones'][name]
            position_error = max(abs(a[k]-b[k]) for k in ['x','y'])
            matrix_error = max(abs(a[k]-b[k]) for k in ['a','b','c','d'])
            max_loop_bone_position = max(max_loop_bone_position, position_error)
            max_loop_bone_matrix = max(max_loop_bone_matrix, matrix_error)
            if position_error > tolerance['loop'] or matrix_error > tolerance['scale']:
                errors.append(f'{name}: loop endpoint bone transform drift')
        for name in prepared:
            residual = float(np.abs(vertices_by_frame[first][name]-vertices_by_frame[last][name]).max())
            max_loop = max(max_loop, residual)
            if residual > tolerance['loop']:
                errors.append(f'{name}: loop endpoint vertex drift')
        require(('firstImage' in loop) == ('lastImage' in loop), 'Both loop image paths are required')
        if 'firstImage' in loop:
            with Image.open(path.parent/loop['firstImage']) as a, Image.open(path.parent/loop['lastImage']) as b:
                if not np.array_equal(np.array(a.convert('RGBA')), np.array(b.convert('RGBA'))):
                    errors.append('Rendered loop endpoint pixels differ')
    contacts = data['contacts']
    require(isinstance(contacts, list), 'Missing contact declarations')
    for contact in contacts:
        first, last = interval(contact, allow_single=True)
        require(contact['bone'] in expected_scales, 'Unknown contact bone')
        target = numbers(contact['target'], 2, 'Contact target')
        limit = contact['tolerance']
        require(finite_number(limit) and limit >= 0, 'Invalid contact tolerance')
        for index in range(first, last+1):
            b = frames[index]['bones'][contact['bone']]
            if np.linalg.norm(np.array([b['x'], b['y']])-target) > limit:
                errors.append(f'Frame {index}: planted contact {contact["bone"]} drift')
    require(all(math.isfinite(v) for v in [max_length,max_scale,max_loop,max_loop_bone_position,max_loop_bone_matrix]), 'Nonfinite computed measurements')
    return dict(schema='ogs.skin-audit/1', technicalStatus='FAIL' if errors else 'PASS',
                inputSHA256=hashlib.sha256(raw).hexdigest(), samples=len(frames), sampleRate=rate,
                maxLengthError=max_length, maxScaleOrShearError=max_scale, maxLoopVertexResidual=max_loop,
                maxLoopBonePositionResidual=max_loop_bone_position, maxLoopBoneMatrixResidual=max_loop_bone_matrix,
                meshes=fold_report, loopsChecked=len(loops), contactIntervalsChecked=len(contacts),
                errors=errors, characterAccepted=False,
                limitations=['Declared trace scope only; exporter correctness is not inferred.',
                             'Visual anatomy, head/body ratios, switch continuity, shoe pixels and native action coverage require independent review.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.trace)
        code = int(report['technicalStatus'] != 'PASS')
    except (ValueError, KeyError, TypeError, OSError, IndexError, OverflowError) as error:
        report = dict(schema='ogs.skin-audit/1', technicalStatus='BLOCKED', errors=[str(error)], characterAccepted=False)
        code = 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps(report, indent=2, allow_nan=False))
    raise SystemExit(code)


if __name__ == '__main__':
    main()
