#!/usr/bin/env python3
"""Independent FX pixel/registration checks. Not anatomy or artistic approval."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    path = Path(path)
    data = json.loads(path.read_text())
    if data.get('schema') != 'ogs.independent-fx/1':
        raise ValueError('expected schema ogs.independent-fx/1')
    ids = [f['id'] for f in data['frames']]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('frames must be nonempty with unique ids')
    return path, data


def frame_image(root, f, issues, side):
    p = root / f['image']
    if digest(p) != f['sha256']:
        issues.append({'code': 'sha256', 'side': side, 'id': f['id']})
    im = Image.open(p).convert('RGBA')
    density = f['density']
    geo = f['frame']
    if (not isinstance(density, (int, float)) or not math.isfinite(density)
            or density <= 0 or not all(math.isfinite(geo[k]) for k in ('ax', 'ay', 'w', 'h'))
            or geo['w'] <= 0 or geo['h'] <= 0):
        raise ValueError('invalid density/geometry')
    if any(abs(im.size[i] - geo[k] * density) > 1e-6 for i, k in enumerate(('w', 'h'))):
        issues.append({'code': 'image-geometry', 'side': side, 'id': f['id']})
    if type(f['durationTicks']) is not int or f['durationTicks'] <= 0:
        raise ValueError('durationTicks must be a positive integer')
    return im


def centroid(im, f):
    total = sx = sy = 0
    for y in range(im.height):
        for x in range(im.width):
            a = im.getpixel((x, y))[3]
            total += a
            sx += a * ((x + .5) / f['density'] - f['frame']['ax'])
            sy += a * ((y + .5) / f['density'] - f['frame']['ay'])
    return [sx / total, sy / total] if total else None


def palette_drift(ref, cand, alpha_threshold):
    # Candidate-to-reference nearest RGB Euclidean distance, weighted by alpha.
    colors = {p[:3] for p in ref.getdata() if p[3] >= alpha_threshold}
    histogram = Counter(cand.getdata())
    if not colors:
        return 0.0 if not any(p[3] >= alpha_threshold for p in histogram) else 441.673
    weight = error = 0
    for p, count in histogram.items():
        if p[3] < alpha_threshold:
            continue
        w = count * p[3]
        error += w * min(math.dist(p[:3], c) for c in colors)
        weight += w
    return error / weight if weight else 0.0


def silhouette(im, f, bounds, sample_density, threshold):
    x0, y0, width, height = bounds
    density = f['density']
    # Common logical canvas, pixel centers mapped into original untrimmed coordinates.
    a = density / sample_density
    matrix = (a, 0, (x0 + f['frame']['ax']) * density,
              0, a, (y0 + f['frame']['ay']) * density)
    mask = im.getchannel('A').transform((width, height), Image.Transform.AFFINE,
                                       matrix, Image.Resampling.NEAREST)
    return mask.point(lambda v: 255 if v >= threshold else 0)


def validate(reference, candidate, thresholds):
    required = ('alphaThreshold', 'sampleDensity', 'minSilhouetteIoU',
                'maxCentroidDrift', 'maxPaletteDrift')
    if any(k not in thresholds for k in required):
        raise ValueError('explicit thresholds required: ' + ', '.join(required))
    t = thresholds
    if (not all(isinstance(t[k], (int, float)) and math.isfinite(t[k]) for k in required)
            or not 0 < t['alphaThreshold'] <= 255 or not 0 < t['sampleDensity'] <= 64
            or not 0 <= t['minSilhouetteIoU'] <= 1
            or t['maxCentroidDrift'] < 0 or t['maxPaletteDrift'] < 0):
        raise ValueError('invalid thresholds')
    rp, r = load(reference)
    cp, c = load(candidate)
    issues, metrics = [], []
    if [f['id'] for f in r['frames']] != [f['id'] for f in c['frames']]:
        issues.append({'code': 'frame-order'})
    if r.get('context') != c.get('context'):
        issues.append({'code': 'context'})
    candidates = {f['id']: f for f in c['frames']}
    # Verify every candidate, including unexpected extra frames.
    images = {f['id']: frame_image(cp.parent, f, issues, 'candidate') for f in c['frames']}
    for rf in r['frames']:
        ri = frame_image(rp.parent, rf, issues, 'reference')
        if rf['id'] not in candidates:
            continue
        cf = candidates[rf['id']]
        ci = images[rf['id']]
        fid = rf['id']
        for key in ('frame', 'durationTicks'):
            if rf[key] != cf[key]:
                issues.append({'code': key, 'id': fid})
        sd = t['sampleDensity']
        x0 = min(-f['frame']['ax'] for f in (rf, cf))
        y0 = min(-f['frame']['ay'] for f in (rf, cf))
        x1 = max(f['frame']['w'] - f['frame']['ax'] for f in (rf, cf))
        y1 = max(f['frame']['h'] - f['frame']['ay'] for f in (rf, cf))
        size = (math.ceil((x1-x0)*sd), math.ceil((y1-y0)*sd))
        if size[0] * size[1] > 16000000:
            raise ValueError('comparison canvas exceeds 16 million samples')
        bounds = (x0, y0, *size)
        rm = silhouette(ri, rf, bounds, sd, t['alphaThreshold'])
        cm = silhouette(ci, cf, bounds, sd, t['alphaThreshold'])
        intersection = union = 0
        for a, b in zip(rm.getdata(), cm.getdata()):
            intersection += bool(a and b)
            union += bool(a or b)
        iou = intersection / union if union else 1.0
        rc, cc = centroid(ri, rf), centroid(ci, cf)
        drift = math.dist(rc, cc) if rc is not None and cc is not None else (0 if rc == cc else None)
        palette = palette_drift(ri, ci, t['alphaThreshold'])
        metrics.append({'id': fid, 'silhouetteIoU': iou, 'referenceCentroid': rc,
                        'candidateCentroid': cc, 'centroidDrift': drift,
                        'paletteDriftMeanRGB': palette})
        for code, failed in [('silhouette', iou < t['minSilhouetteIoU']),
                             ('centroid', drift is None or drift > t['maxCentroidDrift']),
                             ('palette', palette > t['maxPaletteDrift'])]:
            if failed:
                issues.append({'code': code, 'id': fid})
    return {'schema': 'ogs.independent-fx-report/1', 'status': 'fail' if issues else 'pass',
            'scope': 'pixel-registration-only', 'artAccepted': False,
            'referenceManifestSHA256': digest(rp), 'candidateManifestSHA256': digest(cp),
            'thresholds': t, 'metrics': metrics, 'issues': issues}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('reference'); p.add_argument('candidate')
    p.add_argument('--thresholds', required=True); p.add_argument('--out', required=True)
    a = p.parse_args()
    try:
        report = validate(a.reference, a.candidate, json.loads(Path(a.thresholds).read_text()))
    except (OSError, ValueError, KeyError, TypeError) as e:
        report = {'status': 'blocked', 'artAccepted': False, 'issues': [{'code': 'invalid-input', 'detail': str(e)}]}
    Path(a.out).write_text(json.dumps(report, indent=2) + '\n')
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
