"""Reproduce the whole-figure idle case end to end (one image, no cut parts).

make_art -> measure_anatomy (frozen once, proposes the rig) -> idle_motion -> build_mesh -> solve_weights
-> lint_weights -> pose_trace -> audit_skin + measure_surface -> motion_qa -> render.
Two controls must be rejected: a config with a fractional breath count (refused before any motion is
written) and the same idle with per-sample head jitter (fails motion QA). Exit 0 means every expected
outcome was reproduced; it is not an art or animation acceptance.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SKIN = ROOT / 'skills/2d/skin-weights/scripts'
AUDIT = ROOT / 'skills/2d/spine-skeletal/scripts'
sys.path.insert(0, str(SKIN))
from skinlib import forward, load_rig  # noqa: E402


def run(*args, expect=(0,)):
    result = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if result.returncode not in expect:
        sys.stderr.write(result.stdout[-3000:] + result.stderr[-3000:])
        raise SystemExit(f'unexpected exit {result.returncode}: {Path(str(args[0])).name}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    src = HERE / 'source'
    run(HERE / 'make_art.py')
    run(SKIN / 'measure_anatomy.py', src / 'duck.png', '--out', src / 'anatomy.json', '--rig-out', src / 'rig.json')
    rig_path = src / 'rig.json'
    # planted feet: the ground bar must not move (passed to the audit as a fixed contact)
    rig = load_rig(rig_path)
    ground = forward(rig)['ground']
    config = json.loads((HERE / 'idle.json').read_text())
    config['fixedContacts'] = [{'bone': 'ground', 'first': 0, 'last': int(config['duration']*config['sampleRate']),
                                'target': [float(ground[4]), float(ground[5])], 'tolerance': 1e-6}]
    (out / 'idle.json').write_text(json.dumps(config))
    run(SKIN / 'idle_motion.py', rig_path, out / 'idle.json', '--out', src / 'motion.json')
    run(SKIN / 'build_mesh.py', rig_path, '--out', out / 'mesh.json')
    run(SKIN / 'solve_weights.py', rig_path, out / 'mesh.json', '--out', out / 'weights.json')
    lint = run(SKIN / 'lint_weights.py', rig_path, out / 'mesh.json', out / 'weights.json', '--out', out / 'lint.json', expect=(0, 1))
    run(SKIN / 'pose_trace.py', rig_path, out / 'mesh.json', out / 'weights.json', src / 'motion.json', '--out', out / 'trace.json', '--report', out / 'pose.json')
    audit = run(AUDIT / 'audit_skin.py', out / 'trace.json', '--out', out / 'audit.json', expect=(0, 1))
    run(AUDIT / 'measure_surface.py', out / 'trace.json', '--out', out / 'surface.json')
    qa = run(SKIN / 'motion_qa.py', out / 'trace.json', '--out', out / 'motion-qa.json', expect=(0, 1))

    # control 1: a fractional breath count would stretch the loop; it must be refused, not rounded
    bad = dict(config, breaths=2.5)
    (out / 'idle-fractional.json').write_text(json.dumps(bad))
    refused = run(SKIN / 'idle_motion.py', rig_path, out / 'idle-fractional.json', '--out', out / 'unused.json', expect=(0, 1, 2))
    # control 2: the same idle with per-sample head jitter must fail motion QA
    motion = json.loads((src / 'motion.json').read_text())
    rng = np.random.default_rng(7)
    for track in motion['tracks']:
        if track['bone'] == 'head':
            for key in track['keys'][1:-1]:
                key['v'] += float(rng.normal(0, 1.2))
    (out / 'motion-jitter.json').write_text(json.dumps(motion))
    run(SKIN / 'pose_trace.py', rig_path, out / 'mesh.json', out / 'weights.json', out / 'motion-jitter.json', '--out', out / 'trace-jitter.json')
    jitter = run(SKIN / 'motion_qa.py', out / 'trace-jitter.json', '--out', out / 'motion-qa-jitter.json', expect=(0, 1))

    lint_doc, audit_doc = json.loads((out / 'lint.json').read_text()), json.loads((out / 'audit.json').read_text())
    surface, qa_doc = json.loads((out / 'surface.json').read_text()), json.loads((out / 'motion-qa.json').read_text())
    summary = {'anatomy': {k: json.loads((src / 'anatomy.json').read_text())[k] for k in ('neckRow', 'neckSource', 'torsoHalfWidth', 'appendages')},
               'lint': lint_doc['status'], 'audit': audit_doc['technicalStatus'],
               'visibleFoldPixels': {k: v['visibleBadUVPixels'] for k, v in audit_doc['meshes'].items()},
               'surface': {k: {'p05': round(v['visiblePixelWeightedP05Compression'], 4), 'p95': round(v['visiblePixelWeightedP95Stretch'], 4),
                               'minArea': round(v['minimumSignedAreaRatio'], 4)} for k, v in surface['meshes'].items()},
               'motionQA': {'status': qa_doc['status'], 'figure': qa_doc['meshes']['figure']},
               'controls': {'fractionalBreaths': 'REFUSED' if refused.returncode == 2 else 'ACCEPTED',
                            'jitteredHead': json.loads((out / 'motion-qa-jitter.json').read_text())['status']}}
    (out / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
    print(json.dumps(summary, indent=1))
    expected = (lint.returncode == 0 and audit.returncode == 0 and qa.returncode == 0
                and summary['controls'] == {'fractionalBreaths': 'REFUSED', 'jitteredHead': 'FAIL'})
    if not expected:
        raise SystemExit('expected: lint/audit/motion QA PASS, fractional breaths REFUSED, jittered head FAIL')
    if not args.no_render:
        view = '-1,-1,65,73'
        run(SKIN / 'render_skin.py', out / 'trace.json', '--gif', out / 'idle.gif', '--sheet', out / 'idle.sheet.png', '--scale', '6', '--every', '1', f'--view={view}')
        run(SKIN / 'render_skin.py', out / 'trace.json', '--gif', out / 'idle-rig.gif', '--scale', '6', '--every', '1', f'--view={view}',
            '--bones', '--constraints', '--fade', '0.5', '--weights')
    print('Reproduced: whole-figure idle passes lint, fold audit and motion QA; both controls are rejected. Visual review still required.')


if __name__ == '__main__':
    main()
