"""Re-skin the redistributable arm with skin-weights' harmonic solver.

Same source pixels, same bones and same 0 -> 90 -> 0 degree sweep as the rig-c
traces in cases/, converted from rig-c's y-up space to the skill's y-down space.
Only the weights and mesh are regenerated, so the result is directly comparable
with the narrow (FAIL) and revised (PASS) hand-authored envelopes.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SKIN = ROOT / 'skills/2d/skin-weights/scripts'
AUDIT = ROOT / 'skills/2d/spine-skeletal/scripts'
UNIT = 0.018248  # world units per source pixel, fitted from cases/current.trace.json.gz (residual < 1e-6)


def call(*args, expect=(0,)):
    result = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if result.returncode not in expect:
        sys.stderr.write(result.stdout[-2000:] + result.stderr[-2000:])
        raise SystemExit(f'unexpected exit {result.returncode} from {Path(str(args[0])).name}')
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--spacing', type=int, default=24, help='mesh spacing in source pixels')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    source = json.loads((HERE / 'source/current.rig.json').read_text())
    bones = []
    for bone in source['bones']:
        item = {'name': bone['name']}
        if 'parent' in bone:
            item['parent'] = bone['parent']
        # rig-c is y-up; flipping y also flips the rotation sense.
        item.update(x=bone.get('x', 0), y=-bone.get('y', 0), rotation=-bone.get('rotation', 0), length=bone.get('length', 0))
        bones.append(item)
    rig = {'schema': 'ogs.skin-rig/1', 'units': 'rig-c world units, y down', 'bones': bones,
           'parts': [{'name': 'arm', 'image': os.path.relpath(HERE / 'source/arm-setup.png', out),
                      'origin': [0, 0], 'at': [0, -16.186132], 'density': 1/UNIT, 'bones': ['upper_arm', 'forearm', 'wrist'],
                      'mesh': {'spacing': args.spacing, 'alphaThreshold': 32, 'margin': 3},
                      'weights': {'handleRadius': {'upper_arm': 4.0, 'forearm': 3.2, 'wrist': 2.2},
                                  'coreInset': {'upper_arm': 0.45, 'forearm': 0.3, 'wrist': 0.0}, 'maxInfluences': 3, 'pruneBelow': 0.01}}]}
    (out / 'arm.rig.json').write_text(json.dumps(rig, indent=1) + '\n')
    keys = [{'t': t, 'v': -v, 'curve': 'linear'} for t, v in ((0, 0), (0.5, 45), (1, 90), (1.5, 45), (2, 0))]
    motion = {'schema': 'ogs.skin-motion/1', 'sampleRate': 60, 'duration': 2, 'loop': True,
              'scope': 'technical elbow sweep matching cases/*.trace.json.gz',
              'tracks': [{'bone': 'forearm', 'property': 'rotate', 'keys': keys}]}
    (out / 'arm.motion.json').write_text(json.dumps(motion, indent=1) + '\n')
    rig_path, mesh, weights, trace = out / 'arm.rig.json', out / 'arm.mesh.json', out / 'arm.weights.json', out / 'arm.trace.json'
    call(SKIN / 'build_mesh.py', rig_path, '--out', mesh)
    call(SKIN / 'solve_weights.py', rig_path, mesh, '--out', weights)
    lint = call(SKIN / 'lint_weights.py', rig_path, mesh, weights, '--out', out / 'arm.lint.json', expect=(0, 1))
    call(SKIN / 'pose_trace.py', rig_path, mesh, weights, out / 'arm.motion.json', '--out', trace, '--report', out / 'arm.pose.json')
    audit = call(AUDIT / 'audit_skin.py', trace, '--out', out / 'arm.audit.json', expect=(0, 1))
    call(AUDIT / 'measure_surface.py', trace, '--out', out / 'arm.surface.json')
    report = json.loads((out / 'arm.audit.json').read_text())
    surface = json.loads((out / 'arm.surface.json').read_text())['meshes']['arm']
    summary = {'lint': 'PASS' if lint == 0 else 'FAIL', 'audit': report['technicalStatus'],
               'visibleFoldPixels': report['meshes']['arm']['visibleBadUVPixels'],
               'minAreaRatio': round(surface['minimumSignedAreaRatio'], 4),
               'p05Compression': round(surface['visiblePixelWeightedP05Compression'], 4),
               'p95Stretch': round(surface['visiblePixelWeightedP95Stretch'], 4)}
    print(json.dumps(summary, indent=1))
    sys.exit(0 if lint == 0 and audit == 0 else 1)


if __name__ == '__main__':
    main()
