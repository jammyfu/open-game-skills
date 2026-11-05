"""Measure a whole-figure image's silhouette once and propose a small-motion rig. Writes ogs.skin-anatomy/1.

For whole-figure mode (one image, no cut parts). From the alpha alone it finds:
  - the body axis (alpha centroid of the lower body, not the head or a long beak),
  - the row-wise half-width of the central run around that axis,
  - the neck: the most prominent bottleneck of that width profile in the upper body,
  - the torso half-width, appendage rows (wings, arms reaching past 1.3x the torso) and the foot band.
Everything is measured ONCE on the setup image and frozen into the rig; never re-measure per frame
(that is what makes generated idles jitter). If no neck is found it says so and stops unless you
pass --neck-row. `--rig-out` writes an ogs.skin-rig/1 proposal: a planted ground bar, a spine that can
lean, a zero-length chest for breathing and a rigid head above the neck. Review it before solving:
the measurement is geometry, not anatomy. Exit 0 ok, 2 invalid/insufficient.
Inspired by sprite-gen's silhouette anatomy (aldegad/sprite-gen, Apache-2.0); independent implementation.
"""
import argparse
import sys
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from skinlib import RIG_SCHEMA, SkinError, require, sha256, write_json

ANATOMY_SCHEMA = 'ogs.skin-anatomy/1'
APPENDAGE_RATIO = 1.30       # a row whose extent passes this multiple of the torso half-width carries an appendage
NECK_PROMINENCE = 0.06       # a bottleneck must be this fraction of the widest row below the neighbouring maxima
NECK_SEARCH = (0.12, 0.62)   # share of the figure height (from the top) where a neck may sit
FOOT_BAND = 0.08             # bottom share of the figure treated as planted feet


def smooth(values, size=5):
    kernel = np.ones(size)/size
    padded = np.pad(values, size//2, mode='edge')
    return np.convolve(padded, kernel, mode='valid')


def central_run(row, cx):
    """Half-width of the opaque run containing column cx (or the nearest run when cx is transparent)."""
    xs = np.flatnonzero(row)
    if not len(xs):
        return 0.0, None
    breaks = np.flatnonzero(np.diff(xs) > 1)
    starts, ends = np.r_[xs[0], xs[breaks + 1]], np.r_[xs[breaks], xs[-1]]
    inside = np.flatnonzero((starts <= cx) & (ends >= cx))
    k = inside[0] if len(inside) else int(np.argmin(np.minimum(abs(starts - cx), abs(ends - cx))))
    return (ends[k] - starts[k] + 1)/2.0, (starts[k] + ends[k])/2.0


def measure(alpha, threshold=32, neck_row=None):
    mask = alpha > threshold
    require(mask.any(), 'image has no visible pixels above the alpha threshold')
    rows, cols = np.flatnonzero(mask.any(1)), np.flatnonzero(mask.any(0))
    top, bottom, left, right = int(rows[0]), int(rows[-1]) + 1, int(cols[0]), int(cols[-1]) + 1
    height = bottom - top
    require(height >= 24, f'figure is only {height} px tall; measure a larger source')
    lower = mask[top + int(0.4*height):bottom]
    ys, xs = np.nonzero(lower)
    axis = float(xs.mean())
    half, centre = np.zeros(height), np.full(height, axis)
    extent = np.zeros((height, 2))
    for k, y in enumerate(range(top, bottom)):
        h, c = central_run(mask[y], int(round(axis)))
        half[k] = h
        centre[k] = c if c is not None else axis
        xs_row = np.flatnonzero(mask[y])
        extent[k] = (xs_row.min() - axis, xs_row.max() - axis) if len(xs_row) else (0, 0)
    profile = smooth(half)
    source = 'manual'
    if neck_row is None:
        lo, hi = int(NECK_SEARCH[0]*height), int(NECK_SEARCH[1]*height)
        best, best_prom = None, 0.0
        for k in range(lo + 1, hi - 1):
            if not (profile[k] <= profile[k - 1] and profile[k] <= profile[k + 1]):
                continue
            prom = min(profile[:k].max(), profile[k:].max()) - profile[k]
            if prom > best_prom:
                best, best_prom = k, prom
        if best is None or best_prom < NECK_PROMINENCE*profile.max():
            raise SkinError(f'no neck bottleneck found (best prominence {best_prom:.1f} px < {NECK_PROMINENCE:.0%} of the widest row); '
                            'pass --neck-row from the image instead of guessing')
        neck, source = best, 'bottleneck'
    else:
        neck = int(neck_row) - top
        require(0 < neck < height - 1, '--neck-row must lie inside the figure')
    foot = int(round((1 - FOOT_BAND)*height))
    hip = int(round(neck + 0.72*(foot - neck)))
    torso_rows = range(neck + int(0.1*(foot - neck)), neck + int(0.6*(foot - neck)))
    torso_half = float(np.median(profile[list(torso_rows)]))
    reach = np.maximum(-extent[:, 0], extent[:, 1])
    flags = reach > APPENDAGE_RATIO*torso_half
    flags[:neck] = False                       # the head's own width is not an appendage
    appendages, k = [], 0
    while k < height:
        if flags[k]:
            j = k
            while j + 1 < height and flags[j + 1]:
                j += 1
            side = 'left' if (-extent[k:j + 1, 0]).max() > extent[k:j + 1, 1].max() else 'right'
            appendages.append({'rows': [top + k, top + j + 1], 'side': side, 'reachPx': round(float(reach[k:j + 1].max()), 2)})
            k = j + 1
        else:
            k += 1
    head_rows = np.arange(0, neck)
    head_cx = float(np.mean([centre[r] for r in head_rows])) if len(head_rows) else axis
    head_half = float(profile[:neck].max()) if neck else torso_half
    feet = mask[top + foot:bottom]
    fx = np.flatnonzero(feet.any(0))
    return {'box': [left, top, right, bottom], 'axisX': round(axis, 3), 'neckRow': top + neck, 'neckSource': source,
            'neckHalfWidth': round(float(profile[neck]), 3), 'headCentreX': round(head_cx, 3), 'headHalfWidth': round(head_half, 3),
            'torsoHalfWidth': round(torso_half, 3), 'hipRow': top + hip, 'footRow': top + foot,
            'feetSpan': [int(fx.min()), int(fx.max()) + 1] if len(fx) else [left, right],
            'appendages': appendages, 'halfWidthProfile': [round(float(v), 2) for v in profile]}


def propose_rig(anatomy, image_name, density, threshold=32):
    """A small-motion rig in world units (pixel p -> p/density): ground bar, leaning spine, breathing chest, rigid head."""
    d = float(density)
    w = lambda px: px/d
    axis, neck, hip, foot, bottom = anatomy['axisX'], anatomy['neckRow'], anatomy['hipRow'], anatomy['footRow'], anatomy['box'][3]
    torso = anatomy['torsoHalfWidth']
    chest = neck + 0.32*(hip - neck)
    spine_len = hip - chest
    head_top = anatomy['box'][1]
    head_len = max(neck - head_top, 1)            # neck line to the crown: the whole head is one rigid core
    left, right = anatomy['feetSpan']
    ground_y = (foot + bottom)/2
    bones = [
        {'name': 'root', 'x': w(axis), 'y': w(bottom)},
        {'name': 'ground', 'parent': 'root', 'x': w(left - axis), 'y': w(ground_y - bottom), 'rotation': 0, 'length': w(right - left)},
        {'name': 'spine', 'parent': 'root', 'x': 0, 'y': w(hip - bottom), 'rotation': -90, 'length': w(spine_len)},
        {'name': 'chest', 'parent': 'spine', 'x': w(spine_len), 'y': 0},
        {'name': 'head', 'parent': 'spine', 'x': w(hip - neck), 'y': w(anatomy['headCentreX'] - axis), 'rotation': 0, 'length': w(head_len)},
    ]
    weights = {'handleRadius': {'ground': w(max(bottom - foot, 2)*0.6), 'spine': w(torso*0.35), 'chest': w(torso*0.38),
                                'head': w(anatomy['headHalfWidth']*1.15)},
               'coreInset': {'ground': 0.0, 'spine': [0.0, 0.55], 'chest': 0.0, 'head': 0.0},
               'maxInfluences': 3, 'pruneBelow': 0.01}
    part = {'name': 'figure', 'image': image_name, 'origin': [0, 0], 'at': [0, 0], 'density': d,
            'bones': ['ground', 'spine', 'chest', 'head'], 'mesh': {'spacing': 6, 'alphaThreshold': threshold, 'margin': 2},
            'weights': weights}
    return {'schema': RIG_SCHEMA, 'units': f'world units, y down; {d:g} source px per unit',
            'bones': bones, 'parts': [part], 'drawOrder': ['figure'],
            'provenance': 'proposed by skin-weights/measure_anatomy.py from the frozen setup silhouette; review before solving'}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('image')
    parser.add_argument('--out', required=True, help='anatomy JSON')
    parser.add_argument('--rig-out', help='also write a proposed whole-figure ogs.skin-rig/1 here (image path is made relative to it)')
    parser.add_argument('--density', type=float, default=8.0, help='source pixels per world unit for the proposed rig')
    parser.add_argument('--alpha-threshold', type=int, default=32)
    parser.add_argument('--neck-row', type=int, help='source row of the neck when the silhouette has no bottleneck')
    args = parser.parse_args()
    image = Path(args.image).resolve()
    with Image.open(image) as source:
        alpha = np.array(source.convert('RGBA').getchannel('A'))
    anatomy = measure(alpha, args.alpha_threshold, args.neck_row)
    report = {'schema': ANATOMY_SCHEMA, 'image': str(image.name), 'sha256': sha256(image), 'size': [int(alpha.shape[1]), int(alpha.shape[0])],
              'alphaThreshold': args.alpha_threshold, **anatomy,
              'note': 'measured once on the setup image; freeze it, do not re-measure per frame. Geometry, not anatomy acceptance.'}
    write_json(args.out, report)
    if args.rig_out:
        rig_path = Path(args.rig_out).resolve()
        rel = Path(__import__('os').path.relpath(image, rig_path.parent)).as_posix()
        write_json(rig_path, propose_rig(anatomy, rel, args.density, args.alpha_threshold))
    print(json.dumps({k: report[k] for k in ('neckRow', 'neckSource', 'axisX', 'torsoHalfWidth', 'hipRow', 'footRow', 'appendages')}))


if __name__ == '__main__':
    try:
        main()
    except SkinError as error:
        print(f'BLOCKED: {error}', file=sys.stderr)
        raise SystemExit(2)
