"""Export a skin-weights rig + weights (+ baked motion) to rig-c specs (rigc-rig/1, rigc-motion/1).

rig-c (MIT, optional) compiles these to Spine 4.x skeleton JSON. Space conversion:
this skill is y-down; rig-c/Spine are y-up, so y and rotation change sign.
The motion is *baked*: every sample's evaluated local offsets (tracks, easing and
two-bone IK) become linear keys, so rig-c reproduces this evaluator exactly at
sample times. Baked IK is not a live IK constraint; re-author it in the target
tool if gameplay must drive it.

--verify-rigc PACKAGE --bun BUN builds the export with that rig-c, poses it with
rig-c's own core and compares every mesh vertex with pose_trace. Exit 0 ok,
1 verification mismatch, 2 invalid input or toolchain failure.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import pose_trace
from skinlib import SkinError, forward, load_mesh, load_rig, read_json, require, sha256

POSER = r'''
const [tool, candidate, animation, steps, rate] = process.argv.slice(2);
const {readModel, underNoSkin, poseRawAnimation} = await import(tool + '/src/core/entry.ts');
const model = underNoSkin(readModel(await Bun.file(candidate + '/skeleton.model.json').text()));
const poses = poseRawAnimation(model, animation, Array.from({length: Number(steps)}, () => 1 / Number(rate)));
console.log(JSON.stringify(poses.map((p) => Object.fromEntries(p.drawn.map((d) => [d.slot, d.vertices])))));
'''


def export(rig, mesh, weights, motion, out_dir, name):
    out_dir = Path(out_dir).resolve()
    rig_dir = rig['_path'].parent
    bones = []
    for bone in rig['bones']:
        item = {'name': bone['name']}
        if bone.get('parent'):
            item['parent'] = bone['parent']
        for key, sign in (('x', 1), ('y', -1), ('rotation', -1)):
            if bone.get(key, 0):
                item[key] = sign*bone[key]
        if bone.get('length', 0):
            item['length'] = bone['length']
        if not bone.get('inheritRotation', True):
            item['inherit'] = 'noRotationOrReflection'
        bones.append(item)
    skins, setup = {}, []
    for part_name in rig['drawOrder']:
        part = next(p for p in rig['parts'] if p['name'] == part_name)
        m = mesh['parts'][part_name]
        require(m.get('hull'), f'part {part_name}: mesh has no single outline (hull); split islands before exporting')
        rows = [[{'bone': i['bone'], 'x': i['x'], 'y': -i['y'], 'weight': i['weight']} for i in row] for row in weights['parts'][part_name]['weights']]
        skins[part_name] = {part_name: {'type': 'mesh', 'image': part['image'], 'uvs': m['uvs'].ravel().tolist(),
                                        'triangles': m['triangles'].ravel().tolist(), 'weights': rows}}
        setup.append(m['vertices'])
    allv = np.concatenate(setup)
    lo, hi = allv.min(0), allv.max(0)
    spec = {'spec': 'rigc-rig/1', 'name': name, 'images': os.path.relpath(rig_dir, out_dir),
            'skeleton': {'x': float(lo[0]), 'y': float(-hi[1]), 'width': float(hi[0]-lo[0]), 'height': float(hi[1]-lo[1]),
                         'fps': motion['sampleRate'] if motion else 30},
            'bones': bones,
            'slots': [{'name': p, 'bone': next(x for x in rig['parts'] if x['name'] == p)['bones'][0], 'attachment': p} for p in rig['drawOrder']],
            'skins': {'default': skins}}
    result = {'rig': spec}
    if motion:
        rate, count = motion['sampleRate'], int(round(motion['duration']*motion['sampleRate']))
        series = {}
        for index in range(count + 1):
            _, problems, offsets = pose_trace.evaluate(rig, motion, index/rate, 1e-6)
            if problems:
                raise SkinError(f'cannot bake motion with unreachable IK: {problems[0]}')
            for bone, values in offsets.items():
                for prop, value in values.items():
                    series.setdefault((bone, prop), np.zeros(count + 1))[index] = value
        tracks = []
        for bone in [b['name'] for b in rig['bones']]:
            rotate = series.get((bone, 'rotate'))
            if rotate is not None and np.any(rotate):
                values = -np.degrees(np.unwrap(np.radians(rotate)))
                tracks.append({'bone': bone, 'property': 'rotate', 'keys': [{'t': round(i/rate, 9), 'v': [float(v)]} for i, v in enumerate(values)]})
            x, y = series.get((bone, 'x')), series.get((bone, 'y'))
            if (x is not None and np.any(x)) or (y is not None and np.any(y)):
                x = x if x is not None else np.zeros(count + 1)
                y = y if y is not None else np.zeros(count + 1)
                tracks.append({'bone': bone, 'property': 'translate', 'keys': [{'t': round(i/rate, 9), 'v': [float(a), float(-b)]} for i, (a, b) in enumerate(zip(x, y))]})
        result['motion'] = {'spec': 'rigc-motion/1', 'archetype': name, 'cut': 'baked', 'easings': {},
                            'animations': {'main': {'duration': motion['duration'], 'loop': bool(motion.get('loop')),
                                                    'note': 'Baked by skin-weights/export_rigc.py from ogs.skin-motion/1; IK baked, not live.',
                                                    'tracks': tracks}}}
    return result


def verify(rig, mesh, weights, motion, out_dir, package, bun, tolerance):
    out_dir = Path(out_dir).resolve()
    build = out_dir / 'rigc-build'
    command = [bun, str(Path(package) / 'cli_core.ts'), 'build', '--rig', str(out_dir / 'rig.rigc.json'), '--out', str(build)]
    if motion:
        command += ['--motion', str(out_dir / 'motion.rigc.json')]
    built = subprocess.run(command, capture_output=True, text=True)
    require(built.returncode == 0, f'rig-c build failed: {(built.stdout + built.stderr)[-1500:]}')
    rate = motion['sampleRate']
    count = int(round(motion['duration']*rate))
    with tempfile.NamedTemporaryFile('w', suffix='.ts', delete=False, dir=out_dir) as handle:
        handle.write(POSER)
    try:
        posed = subprocess.run([bun, handle.name, str(Path(package).resolve()), str(build), 'main', str(count), str(rate)], capture_output=True, text=True)
    finally:
        os.unlink(handle.name)
    require(posed.returncode == 0, f'rig-c pose failed: {posed.stderr[-1500:]}')
    frames = json.loads(posed.stdout)
    require(len(frames) == count + 1, f'rig-c returned {len(frames)} poses, expected {count + 1}')
    worst = {}
    for index, frame in enumerate(frames):
        world, _, _ = pose_trace.evaluate(rig, motion, index/rate, 1e-6)
        for part in rig['drawOrder']:
            ours = pose_trace.deform(weights['parts'][part]['weights'], world)
            theirs = np.array(frame[part]).reshape(-1, 2)*[1, -1]
            worst[part] = max(worst.get(part, 0.0), float(np.abs(ours - theirs).max()))
    return {'rigc': str(package), 'samples': count + 1, 'maxVertexDeviation': worst,
            'tolerance': tolerance, 'passed': all(v <= tolerance for v in worst.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rig')
    parser.add_argument('mesh')
    parser.add_argument('weights')
    parser.add_argument('--motion')
    parser.add_argument('--out', required=True, help='output directory')
    parser.add_argument('--name', default='skin-weights-export')
    parser.add_argument('--verify-rigc')
    parser.add_argument('--bun', default='bun')
    parser.add_argument('--tolerance', type=float, default=1e-3, help='world units; rig-c stores float32')
    args = parser.parse_args()
    try:
        rig, mesh, weights = load_rig(args.rig), load_mesh(args.mesh), read_json(args.weights)
        require(weights.get('rigSHA256') == sha256(rig['_path']) and weights.get('meshSHA256') == sha256(args.mesh), 'weights/mesh/rig hashes disagree')
        motion = pose_trace.load_motion(args.motion, rig) if args.motion else None
        result = export(rig, mesh, weights, motion, args.out, args.name)
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'rig.rigc.json').write_text(json.dumps(result['rig'], separators=(',', ':')) + '\n')
        if motion:
            (out / 'motion.rigc.json').write_text(json.dumps(result['motion'], separators=(',', ':')) + '\n')
        report = {'status': 'EXPORTED', 'files': sorted(p.name for p in out.glob('*.rigc.json')), 'officialSpineParser': 'not-run'}
        if args.verify_rigc:
            require(motion is not None, '--verify-rigc needs --motion')
            report['verification'] = verify(rig, mesh, weights, motion, out, args.verify_rigc, args.bun, args.tolerance)
            report['status'] = 'VERIFIED' if report['verification']['passed'] else 'MISMATCH'
    except (SkinError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'status': 'BLOCKED', 'errors': [str(error)]}, indent=1))
        sys.exit(2)
    print(json.dumps(report, indent=1))
    sys.exit(1 if report['status'] == 'MISMATCH' else 0)


if __name__ == '__main__':
    main()
