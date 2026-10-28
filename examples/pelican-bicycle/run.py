"""Reproduce the pelican-on-a-bicycle skinning case end to end.

Pipeline: make_art -> build_mesh -> solve_weights (harmonic) -> lint_weights ->
pose_trace (IK pedalling) -> spine-skeletal audit_skin + measure_surface -> render.
A negative control repeats the deformation with rigid nearest-bone weights and
must be rejected. Exit 0 means every expected outcome was reproduced; it is not a
character/art acceptance.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SKIN = ROOT / 'skills/2d/skin-weights/scripts'
AUDIT = ROOT / 'skills/2d/spine-skeletal/scripts'


def run(*args, expect=(0,)):
    result = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if result.returncode not in expect:
        sys.stderr.write(result.stdout[-3000:] + result.stderr[-3000:])
        raise SystemExit(f'unexpected exit {result.returncode}: {Path(str(args[0])).name}')
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    rig, motion = HERE / 'source/rig.json', HERE / 'source/motion.json'
    run(HERE / 'make_art.py')
    run(SKIN / 'build_mesh.py', rig, '--out', out / 'mesh.json')
    summary = {}
    for method, expected in (('harmonic', 'PASS'), ('nearest', 'FAIL')):
        weights, trace = out / f'{method}.weights.json', out / f'{method}.trace.json'
        run(SKIN / 'solve_weights.py', rig, out / 'mesh.json', '--out', weights, '--method', method)
        lint_code = run(SKIN / 'lint_weights.py', rig, out / 'mesh.json', weights, '--out', out / f'{method}.lint.json', expect=(0, 1))
        run(SKIN / 'pose_trace.py', rig, out / 'mesh.json', weights, motion, '--out', trace, '--report', out / f'{method}.pose.json')
        audit_code = run(AUDIT / 'audit_skin.py', trace, '--out', out / f'{method}.audit.json', expect=(0, 1))
        run(AUDIT / 'measure_surface.py', trace, '--out', out / f'{method}.surface.json', expect=(0,))
        audit = json.loads((out / f'{method}.audit.json').read_text())
        lint = json.loads((out / f'{method}.lint.json').read_text())
        pose = json.loads((out / f'{method}.pose.json').read_text())
        surface = json.loads((out / f'{method}.surface.json').read_text())
        folds = {k: v['visibleBadUVPixels'] for k, v in audit['meshes'].items() if v['visibleBadUVPixels']}
        summary[method] = {'lint': lint['status'], 'audit': audit['technicalStatus'], 'visibleFoldPixels': folds,
                           'maxContactGap': max(c['maxGap'] for c in pose['followContacts']),
                           'softLengthFraction': {b: v['softLengthFraction'] for part in ('leg_n', 'leg_f') for b, v in pose['rigidityDeviation'].get(part, {}).items()},
                           'p95Stretch': {k: round(v['visiblePixelWeightedP95Stretch'], 4) for k, v in surface['meshes'].items() if k.startswith(('leg', 'neck'))},
                           'minAreaRatio': {k: round(v['minimumSignedAreaRatio'], 4) for k, v in surface['meshes'].items() if k.startswith(('leg', 'neck'))},
                           'p05Compression': {k: round(v['visiblePixelWeightedP05Compression'], 4) for k, v in surface['meshes'].items() if k.startswith(('leg', 'neck'))}}
        got = 'PASS' if lint_code == 0 and audit_code == 0 else 'FAIL'
        if got != expected:
            print(json.dumps(summary, indent=1))
            raise SystemExit(f'{method}: expected {expected}, got lint={lint["status"]} audit={audit["technicalStatus"]}')
        if not args.no_render:
            run(SKIN / 'render_skin.py', trace, '--gif', out / f'{method}.gif', '--sheet', out / f'{method}.sheet.png', '--scale', '4', '--every', '2')
    (out / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
    print(json.dumps(summary, indent=1))
    print('Reproduced: harmonic weights PASS lint+audit; rigid nearest-bone control is rejected. Visual review still required.')


if __name__ == '__main__':
    main()
