"""Judge a trace as motion: loop seam, pops, jitter and parts that must stay still. Writes ogs.skin-motion-qa/1.

A trace can pass every fold and length check and still animate badly. Per mesh (and per bone origin) this
measures, at every sample:
  step   = largest vertex move between consecutive samples,
  accel  = largest second difference (how abruptly the motion changes),
and reports
  seam      the accel across the loop wrap against the 95th percentile elsewhere (a hitch at the loop point),
            or, when the trace does not close, the jump from the last sample to the first,
  pop       the largest step against the median step (one frame leaps),
  jitter    mean accel / mean step (high = shaky, near 0 = smooth),
  still     for parts named with --still: the largest move away from sample 0 (should be 0).
Thresholds are fixed before looking at the result and printed in the report; pass a part to --allow-jitter
when it is meant to shake (a fluttering tail). Exit 0 PASS, 1 FAIL, 2 invalid. Review evidence for a human;
it does not approve the animation's design. Motion-as-motion QA after sprite-gen (aldegad/sprite-gen, Apache-2.0).
"""
import argparse
import json

import numpy as np

from skinlib import SkinError, read_json, require, write_json

DEFAULTS = {'seam': 3.0, 'pop': 6.0, 'jitter': 0.6, 'still': 1e-6, 'minMotion': 1e-6}


def series(frames, key, name):
    if key == 'meshes':
        return np.array([np.array(f['meshes'][name]).reshape(-1, 2) for f in frames])
    return np.array([[[f['bones'][name]['x'], f['bones'][name]['y']]] for f in frames])


def judge(points, loop, limits, allow_jitter=False, still=False):
    """points: (frames, vertices, 2). Returns metrics and failure strings."""
    step = np.linalg.norm(np.diff(points, axis=0), axis=2).max(1)              # (F-1,)
    fails, row = [], {}
    moved = float(np.linalg.norm(points - points[0], axis=2).max())
    row['maxDisplacement'] = round(moved, 7)
    if still:
        row['still'] = moved <= limits['still']
        if not row['still']:
            fails.append(f'moves {moved:.4g} from sample 0 but is declared still')
        return row, fails
    if moved <= limits['minMotion']:
        row['static'] = True
        return row, fails
    body = points[:-1] if loop else points                                      # drop the duplicated end sample
    ext = np.concatenate([body[-1:], body, body[:1]]) if loop else body
    accel = np.linalg.norm(ext[2:] - 2*ext[1:-1] + ext[:-2], axis=2).max(1)    # loop: index 0 is the wrap
    median = float(np.median(step)) or 1e-12
    row.update({'maxStep': round(float(step.max()), 7), 'medianStep': round(median, 7),
                'pop': round(float(step.max())/median, 3),
                'jitter': round(float(accel.mean())/max(float(step.mean()), 1e-12), 4)})
    if loop:
        inner = accel[1:]
        ref = float(np.percentile(inner, 95)) if len(inner) else 0.0
        row['seam'] = round(float(accel[0])/max(ref, 1e-12), 3) if accel[0] > 1e-9 else 0.0
        if row['seam'] > limits['seam']:
            fails.append(f'loop seam hitch: wrap accel {accel[0]:.4g} is {row["seam"]}x the 95th percentile elsewhere')
    else:
        gap = float(np.linalg.norm(points[-1] - points[0], axis=1).max())
        row['openGap'] = round(gap, 7)
    if row['pop'] > limits['pop']:
        fails.append(f'pop: one step {row["maxStep"]:.4g} is {row["pop"]}x the median step')
    if row['jitter'] > limits['jitter'] and not allow_jitter:
        fails.append(f'jitter {row["jitter"]} > {limits["jitter"]} (mean accel / mean step)')
    return row, fails


def qa(trace, limits, still=(), allow_jitter=()):
    frames = trace['frames']
    require(len(frames) >= 4, 'need at least four samples to judge motion')
    loop = any(l.get('first') == 0 and l.get('last') == len(frames) - 1 for l in trace.get('loops', []))
    unknown = (set(still) | set(allow_jitter)) - set(trace['meshes'])
    require(not unknown, f'unknown parts: {sorted(unknown)}')
    report, failures = {'meshes': {}, 'bones': {}}, []
    for name in trace['meshes']:
        row, fails = judge(series(frames, 'meshes', name), loop, limits, name in allow_jitter, name in still)
        report['meshes'][name] = row
        failures += [f'{name}: {f}' for f in fails]
    for name in frames[0]['bones']:
        row, fails = judge(series(frames, 'bones', name), loop, limits, True, False)
        report['bones'][name] = row
        failures += [f'bone {name}: {f}' for f in fails]
    return {'schema': 'ogs.skin-motion-qa/1', 'status': 'FAIL' if failures else 'PASS', 'loop': loop, 'samples': len(frames),
            'limits': limits, 'still': sorted(still), 'allowJitter': sorted(allow_jitter), 'failures': failures, **report,
            'note': 'Motion evidence only. Watch the GIF too: a smooth loop can still read as the wrong motion.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('trace')
    parser.add_argument('--out', required=True)
    parser.add_argument('--still', default='', help='comma list of parts that must not move at all')
    parser.add_argument('--allow-jitter', default='', help='comma list of parts that are meant to shake')
    for key, value in DEFAULTS.items():
        parser.add_argument(f'--{key}', type=float, default=value)
    args = parser.parse_args()
    split = lambda s: [x for x in s.split(',') if x]
    limits = {k: getattr(args, k) for k in DEFAULTS}
    report = qa(read_json(args.trace), limits, split(args.still), split(args.allow_jitter))
    write_json(args.out, report)
    print(json.dumps({'status': report['status'], 'failures': report['failures'][:10]}))
    raise SystemExit(0 if report['status'] == 'PASS' else 1)


if __name__ == '__main__':
    try:
        main()
    except SkinError as error:
        raise SystemExit(f'BLOCKED: {error}')
