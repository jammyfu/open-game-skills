#!/usr/bin/env python3
"""Offline, hash-bound sprite identity/sequence checks. No generation or gameplay."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from PIL import Image, ImageDraw

REQUIRED = {'head_height', 'head_width', 'face_width', 'face_height', 'torso', 'shoulders'}

class Invalid(ValueError):
    pass

def unique(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise Invalid('duplicate JSON key: ' + k)
        result[k] = v
    return result

def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique,
                      parse_constant=lambda s: (_ for _ in ()).throw(Invalid('nonfinite JSON: ' + s)))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def number(v, positive=False):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or (positive and v <= 0):
        raise Invalid('expected finite ' + ('positive ' if positive else '') + 'number')
    return float(v)

def point(v):
    if not isinstance(v, list) or len(v) != 2:
        raise Invalid('expected [x,y]')
    return [number(x) for x in v]

def length(points, pair):
    return math.dist(points[pair[0]], points[pair[1]])

def relative(actual, expected):
    return abs(actual / expected - 1)

def validate(root, lock_path, obs_path, out):
    root, lock_path, obs_path, out = (Path(p).resolve() for p in (root, lock_path, obs_path, out))
    report = {'schema': 'ogs.hd-sprite-report/1', 'scope': 'offline annotated sprite geometry; not automatic face recognition or engine evidence',
              'status': 'blocked', 'lock_sha256': sha(lock_path), 'observations_sha256': sha(obs_path),
              'issues': [], 'frames': {}, 'edges': [], 'artifacts': []}
    pictures, points_for_preview = {}, {}
    unsafe_output = False
    def issue(code, detail, frame=None, severity='fail'):
        report['issues'].append(dict(code=code, frame=frame, severity=severity, detail=detail))
    def resource(name):
        nonlocal unsafe_output
        if not isinstance(name, str) or not name:
            raise Invalid('image path is required')
        p = (root / name).resolve()
        if p == out or out in p.parents:
            unsafe_output = True
            raise Invalid('source input is inside output directory')
        if not p.is_relative_to(root):
            raise Invalid('image must be beneath root')
        if not p.is_file():
            raise Invalid('missing image: ' + name)
        return p
    try:
        if out in lock_path.parents or out in obs_path.parents or out in root.parents or out == root:
            raise Invalid('output directory must not contain source inputs')
        lock, obs = read(lock_path), read(obs_path)
        if lock['schema'] != 'ogs.hd-sprite-lock/1' or obs['schema'] != 'ogs.hd-sprite-observations/1':
            raise Invalid('unsupported schema')
        report['build'] = obs.get('build')
        if not isinstance(obs.get('build'), str) or not obs['build'].strip():
            raise Invalid('art build identity is required')
        if obs.get('lock_sha256') != report['lock_sha256']:
            issue('lock-changed', 'observations refer to different lock bytes', severity='blocked')
        model = lock['model']; mp = resource(model['image'])
        if model.get('sha256') != sha(mp) or model.get('review') != 'approved' or not str(model.get('reviewer', '')).strip():
            raise Invalid('approved model image/reviewer/hash is missing or stale')
        limits = {k: number(lock['limits'][k]) for k in ('length_rel', 'ratio_rel', 'position_px', 'delta_px')}
        if any(v < 0 for v in limits.values()):
            raise Invalid('negative tolerance')
        canvas = lock['canvas']; size = [number(canvas[k], True) for k in ('width', 'height')]; pivot = point(canvas['pivot'])
        if any(v != int(v) for v in size) or any(p < 0 or p > s for p, s in zip(pivot, size)):
            raise Invalid('invalid source canvas or pivot')
        segments = lock['segments']; canonical = {k: number(lock['lengths'][k], True) for k in segments}
        if not REQUIRED.issubset(segments) or not lock['ratios']:
            raise Invalid('head/face/body segment and ratio contract required')
        for pair in segments.values():
            if not isinstance(pair, list) or len(pair) != 2 or any(not isinstance(x, str) for x in pair):
                raise Invalid('segment must name two landmarks')
        for pair in lock['ratios'].values():
            if len(pair) != 2 or any(k not in segments for k in pair):
                raise Invalid('ratio must name two declared segments')
        if not any(set(pair) == {'face_width', 'head_width'} for pair in lock['ratios'].values()) or not any('head_height' in pair and 'torso' in pair for pair in lock['ratios'].values()):
            raise Invalid('face/head and head/torso ratios required')
        model_density = number(model['density'], True)
        model_points = {k: [v / model_density for v in point(p)] for k, p in model['landmarks'].items()}
        with Image.open(mp) as model_image:
            model_image.load()
            for p in model['landmarks'].values():
                if any(v < 0 or v >= bound for v, bound in zip(point(p), model_image.size)):
                    raise Invalid('model landmark outside pinned image')
        for name, pair in segments.items():
            if any(k not in model_points for k in pair) or relative(length(model_points, pair), canonical[name]) > limits['length_rel']:
                raise Invalid('canonical lengths disagree with model landmarks: ' + name)
        hz = number(lock['logical_tick_hz'], True)
        refs, actual = lock['frames'], obs['frames']
        if not refs or not lock['clips']:
            raise Invalid('required poses and clips must be nonempty')
        for fid in sorted(set(refs) - set(actual)):
            issue('missing-frame', 'required pose has no observations', fid, 'blocked')
        for fid in sorted(set(actual) - set(refs)):
            issue('unexpected-frame', 'pose is outside locked inventory', fid)
        measured, expected = {}, {}
        for fid, ref in refs.items():
            if fid not in actual:
                continue
            try:
                f = actual[fid]; image = resource(f['image']); digest = sha(image)
                if digest != f['sha256']:
                    issue('image-changed', 'annotated image bytes changed', fid, 'blocked'); continue
                review = f.get('review', {})
                if review.get('image_sha256') != digest or not str(review.get('reviewer', '')).strip() or any(review.get(k) is not True for k in ('identity', 'pose', 'alpha', 'temporal')):
                    issue('unreviewed-image', 'hash-bound identity/pose/alpha/temporal review incomplete', fid, 'blocked')
                density = number(f['density'], True); trim = point(f['trim_offset'])
                if point(f['source_size']) != size or point(f['pivot']) != pivot:
                    issue('source-geometry', 'source canvas/pivot differs from character lock', fid)
                with Image.open(image) as opened:
                    opened.load(); im = opened.convert('RGBA')
                if any(v < 0 for v in trim) or any(t + p / density > s + 1e-8 for t, p, s in zip(trim, im.size, size)):
                    issue('trim-outside-source', 'decoded image/trim does not fit locked canvas', fid)
                alpha = im.getchannel('A'); ink = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
                if not ink or alpha.getextrema()[0] != 0:
                    issue('alpha-invalid', 'nonempty artwork with transparent alpha required', fid)
                elif ink[0] == 0 or ink[1] == 0 or ink[2] == im.width or ink[3] == im.height:
                    issue('clipped-border', 'visible pixels touch decoded image border', fid)
                target = {k: point(v) for k, v in ref['landmarks'].items()}
                raw = {k: point(v) for k, v in f['landmarks'].items()}
                for k, p in raw.items():
                    if any(v < 0 or v >= bound for v, bound in zip(p, im.size)):
                        issue('landmark-outside-image', k, fid)
                world = {k: [p[i] / density + trim[i] - pivot[i] for i in (0, 1)] for k, p in raw.items()}
                occluded = ref.get('occluded', {})
                evidence = ref.get('reference_evidence', {})
                if not isinstance(evidence, dict) or not ref.get('view'):
                    raise Invalid('pinned source-pose evidence and view are required')
                if sha(resource(evidence['path'])) != evidence['sha256']:
                    raise Invalid('source-pose evidence changed')
                if any(not isinstance(v, str) or not v.strip() for v in occluded.values()):
                    raise Invalid('occluded landmarks require an authored reason')
                absent = set(target) - set(world) - set(occluded)
                for k in sorted(absent):
                    issue('missing-landmark', k, fid, 'blocked')
                values, reference_values = {}, {}
                for name, pair in segments.items():
                    if any(k in occluded for k in pair):
                        if name not in ('face_width', 'face_height') or ref['view'] != 'back':
                            issue('unobservable-anatomy', name, fid, 'blocked')
                        continue
                    if any(k not in target or k not in world for k in pair):
                        issue('unmeasured-segment', name, fid, 'blocked'); continue
                    proj = number(ref.get('projection', {}).get(name, 1), True)
                    if proj > 1:
                        raise Invalid('projection >1 would enlarge anatomy')
                    wanted = canonical[name] * proj; reference_length = length(target, pair)
                    if relative(reference_length, wanted) > limits['length_rel']:
                        issue('invalid-reference-proportion', name, fid)
                    value = length(world, pair)
                    if relative(value, wanted) > limits['length_rel']:
                        issue('anatomy-length', {'segment': name, 'actual': value, 'expected': wanted}, fid)
                    values[name] = value / proj; reference_values[name] = wanted / proj
                ratios = {}
                for name, pair in lock['ratios'].items():
                    if any(k not in values for k in pair):
                        continue
                    if values[pair[1]] <= 0:
                        issue('degenerate-anatomy', name, fid); continue
                    ratio = values[pair[0]] / values[pair[1]]; wanted = canonical[pair[0]] / canonical[pair[1]]
                    ratios[name] = ratio
                    if relative(ratio, wanted) > limits['ratio_rel']:
                        issue('anatomy-ratio', {'ratio': name, 'actual': ratio, 'expected': wanted}, fid)
                errors = {k: math.dist(world[k], target[k]) for k in sorted(set(world) & set(target) - set(occluded))}
                for k, error in errors.items():
                    if error > limits['position_px']:
                        issue('pose-landmark', {'landmark': k, 'error_px': error}, fid)
                measured[fid], expected[fid] = world, target
                report['frames'][fid] = dict(image_sha256=digest, lengths=values, ratios=ratios, position_errors=errors, occluded=occluded)
                pictures[fid] = (im, density, trim); points_for_preview[fid] = (world, target)
            except (KeyError, TypeError, ValueError, OSError, AttributeError, ZeroDivisionError, OverflowError) as exc:
                issue('frame-evidence-invalid', str(exc), fid, 'blocked')
        used = set()
        for cid, clip in lock['clips'].items():
            frames, ticks, track = clip['frames'], clip['ticks'], clip['track']
            if not isinstance(clip.get('loop'), bool) or not frames or len(frames) != len(ticks) or not track or any(type(v) is not int or v <= 0 for v in ticks):
                raise Invalid('invalid clip inventory/timing/track: ' + cid)
            if any(fid not in refs for fid in frames):
                raise Invalid('clip refers to unknown frame: ' + cid)
            used.update(frames)
            edges = list(zip(frames, frames[1:])) + ([(frames[-1], frames[0])] if clip['loop'] else [])
            for a, b in edges:
                edge = dict(clip=cid, a=a, b=b, residuals={})
                for k in track:
                    if any(fid not in measured or k not in measured[fid] or k not in expected[fid] for fid in (a, b)):
                        issue('unmeasured-transition', dict(clip=cid, a=a, b=b, landmark=k), severity='blocked'); continue
                    error = math.dist([measured[b][k][i] - measured[a][k][i] for i in (0, 1)], [expected[b][k][i] - expected[a][k][i] for i in (0, 1)])
                    edge['residuals'][k] = error
                    if error > limits['delta_px']:
                        issue('temporal-residual', dict(clip=cid, a=a, b=b, landmark=k, error_px=error))
                report['edges'].append(edge)
        if used != set(refs):
            issue('unplayed-frames', sorted(set(refs) - used), severity='blocked')
        # Visual review artifact: one shared scale and actor origin, never per-cell fitting.
        display = min(4, 512 / max(size)); cw, ch = math.ceil(size[0] * display), math.ceil(size[1] * display) + 24
        names = list(refs); columns = min(4, len(names)); sheet = Image.new('RGBA', (cw * columns, ch * math.ceil(len(names) / columns)), '#29292e')
        tiles = {}
        for index, fid in enumerate(names):
            tile = Image.new('RGBA', (cw, ch), '#29292e'); draw = ImageDraw.Draw(tile)
            if fid in pictures:
                im, density, trim = pictures[fid]; scaled = im.resize((max(1, round(im.width * display / density)), max(1, round(im.height * display / density))), Image.Resampling.LANCZOS)
                tile.alpha_composite(scaled, (round(trim[0] * display), round(trim[1] * display)))
                for points, color in zip(points_for_preview[fid], ('#ff4444', '#00ffff')):
                    for p in points.values():
                        x, y = ((p[i] + pivot[i]) * display for i in (0, 1)); draw.ellipse((x-2, y-2, x+2, y+2), outline=color)
            x, y = (v * display for v in pivot); draw.line((x-5,y,x+5,y),fill='white');draw.line((x,y-5,x,y+5),fill='white');draw.text((4,ch-20),fid,fill='white')
            tiles[fid] = tile.convert('RGB'); sheet.alpha_composite(tile, ((index % columns) * cw, (index // columns) * ch))
        out.mkdir(parents=True, exist_ok=True); sheet.save(out / 'overlay.png')
        report['artifacts'].append(dict(path='overlay.png', sha256=sha(out/'overlay.png')))
        for index, (cid, clip) in enumerate(lock['clips'].items()):
            images = [tiles[fid] for fid in clip['frames']]
            # GIF is a visual aid only; durations in the lock remain project ticks.
            loop_option = {'loop': 0} if clip['loop'] else {}
            clip_path = out / ('clip-' + str(index) + '-' + re.sub(r'[^a-zA-Z0-9_-]', '_', cid) + '.gif')
            images[0].save(clip_path, save_all=True, append_images=images[1:], duration=[max(10, round(t*1000/hz)) for t in clip['ticks']], **loop_option)
            report['artifacts'].append(dict(path=clip_path.name, sha256=sha(clip_path)))
    except (KeyError, TypeError, ValueError, OSError, AttributeError, ZeroDivisionError, OverflowError) as exc:
        issue('contract-invalid', str(exc), severity='blocked')
    report['status'] = 'fail' if any(x['severity'] == 'fail' for x in report['issues']) else 'blocked' if report['issues'] else 'pass'
    report['first_violation'] = report['issues'][0] if report['issues'] else None
    # Do not write an output that could overwrite source evidence after invalid configuration.
    if unsafe_output or out == root or out in root.parents or out in lock_path.parents or out in obs_path.parents:
        return report
    out.mkdir(parents=True, exist_ok=True); (out/'report.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('root', 'lock', 'observations', 'out'):
        p.add_argument('--'+key, required=True)
    a = p.parse_args(); root = Path(a.root)
    try:
        report = validate(root, root/a.lock, root/a.observations, a.out)
    except (ValueError, OSError) as exc:
        print(json.dumps(dict(status='blocked', error=str(exc)))); return 2
    print(json.dumps({k: report[k] for k in ('status', 'first_violation')}))
    return {'pass': 0, 'fail': 1, 'blocked': 2}[report['status']]

if __name__ == '__main__':
    sys.exit(main())
