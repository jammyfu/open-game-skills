"""Render an ogs.skin-trace/1 with one fixed camera for visual review.

Textured triangles are sampled through their UVs (nearest), composited in the
trace's drawOrder. Optional overlays: mesh wireframe, bones, and inverted
(folded) triangles in red. `--heat BONE` paints that bone's weight instead of
texture. Writes a GIF and/or a contact sheet PNG. Review output is evidence for a
human, not an acceptance verdict.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from skinlib import SkinError, signed_areas


def raster_triangle(canvas, points, uv, texture, colour=None):
    h, w = canvas.shape[:2]
    x0, y0 = np.floor(points.min(0)).astype(int)
    x1, y1 = np.ceil(points.max(0)).astype(int) + 1
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, w), min(y1, h)
    if x1 <= x0 or y1 <= y0:
        return
    ys, xs = np.mgrid[y0:y1, x0:x1] + 0.5
    a, b, c = points
    det = (b[1]-c[1])*(a[0]-c[0]) + (c[0]-b[0])*(a[1]-c[1])
    if abs(det) < 1e-12:
        return
    l1 = ((b[1]-c[1])*(xs-c[0]) + (c[0]-b[0])*(ys-c[1])) / det
    l2 = ((c[1]-a[1])*(xs-c[0]) + (a[0]-c[0])*(ys-c[1])) / det
    l3 = 1 - l1 - l2
    inside = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
    if not inside.any():
        return
    if colour is not None:
        weight = l1*colour[0] + l2*colour[1] + l3*colour[2]
        rgba = np.zeros(weight.shape + (4,))
        rgba[..., 0] = 255*weight
        rgba[..., 2] = 255*(1-weight)
        rgba[..., 1] = 60
        rgba[..., 3] = 255
    else:
        th, tw = texture.shape[:2]
        u = l1*uv[0, 0] + l2*uv[1, 0] + l3*uv[2, 0]
        v = l1*uv[0, 1] + l2*uv[1, 1] + l3*uv[2, 1]
        tx = np.clip((u*tw).astype(int), 0, tw-1)
        ty = np.clip((v*th).astype(int), 0, th-1)
        rgba = texture[ty, tx].astype(float)
    region = canvas[y0:y1, x0:x1]
    alpha = (rgba[..., 3:4]/255.0)*inside[..., None]
    region[..., :3] = rgba[..., :3]*alpha + region[..., :3]*(1-alpha)
    region[..., 3:4] = np.maximum(region[..., 3:4], 255*alpha)


def camera(trace, scale, pad):
    allv = np.concatenate([np.array(f['meshes'][n]).reshape(-1, 2) for f in trace['frames'] for n in trace['meshes']])
    lo, hi = allv.min(0) - pad, allv.max(0) + pad
    size = np.ceil((hi - lo)*scale).astype(int)
    return lo, size


def render(trace_path, frames, scale, pad, wire, bones, heat, background):
    trace_path = Path(trace_path)
    trace = json.loads(trace_path.read_text())
    order = trace.get('drawOrder', list(trace['meshes']))
    textures, data = {}, {}
    for name in order:
        m = trace['meshes'][name]
        with Image.open(trace_path.parent / m['image']) as image:
            textures[name] = np.array(image.convert('RGBA'))
        tri = np.array(m['triangles']).reshape(-1, 3)
        rest = np.array(m['setupVertices']).reshape(-1, 2)
        heat_values = None
        if heat:
            heat_values = np.array([sum(i['weight'] for i in row if i['bone'] == heat) for row in m['weights']])
        data[name] = (tri, np.array(m['uvs']).reshape(-1, 2), np.sign(signed_areas(rest, tri)), heat_values)
    origin, size = camera(trace, scale, pad)
    images = []
    for index in frames:
        frame = trace['frames'][index]
        canvas = np.zeros((size[1], size[0], 4))
        canvas[..., :3] = background
        canvas[..., 3] = 255
        overlay = []
        for name in order:
            tri, uv, rest_sign, heat_values = data[name]
            posed = (np.array(frame['meshes'][name]).reshape(-1, 2) - origin)*scale
            flipped = np.sign(signed_areas(posed, tri)) != rest_sign
            for k, ids in enumerate(tri):
                colour = heat_values[ids] if heat_values is not None else None
                raster_triangle(canvas, posed[ids], uv[ids], textures[name], colour)
            if wire or flipped.any():
                overlay.append((posed, tri, flipped))
        image = Image.fromarray(canvas.clip(0, 255).astype(np.uint8), 'RGBA').convert('RGB')
        draw = ImageDraw.Draw(image)
        for posed, tri, flipped in overlay:
            for k, ids in enumerate(tri):
                if flipped[k]:
                    draw.polygon([tuple(p) for p in posed[ids]], outline=(255, 0, 0), fill=(255, 0, 0))
                elif wire:
                    draw.polygon([tuple(p) for p in posed[ids]], outline=(40, 160, 255))
        if bones:
            for name, m in frame['bones'].items():
                x, y = (np.array([m['x'], m['y']]) - origin)*scale
                draw.ellipse([x-3, y-3, x+3, y+3], outline=(255, 210, 0), width=2)
        images.append(image)
    return images


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace')
    parser.add_argument('--gif')
    parser.add_argument('--sheet')
    parser.add_argument('--every', type=int, default=2, help='frame stride for the GIF')
    parser.add_argument('--sheet-frames', type=int, default=8)
    parser.add_argument('--scale', type=float, default=1.0, help='output pixels per world unit')
    parser.add_argument('--pad', type=float, default=4.0)
    parser.add_argument('--wire', action='store_true')
    parser.add_argument('--bones', action='store_true')
    parser.add_argument('--heat')
    parser.add_argument('--background', default='238,232,220')
    args = parser.parse_args()
    background = [int(v) for v in args.background.split(',')]
    count = len(json.loads(Path(args.trace).read_text())['frames'])
    if not (args.gif or args.sheet):
        raise SystemExit('nothing to write: pass --gif and/or --sheet')
    if args.gif:
        images = render(args.trace, range(0, count, args.every), args.scale, args.pad, args.wire, args.bones, args.heat, background)
        Path(args.gif).parent.mkdir(parents=True, exist_ok=True)
        duration = max(20, int(1000*args.every/json.loads(Path(args.trace).read_text())['sampleRate']))
        images[0].save(args.gif, save_all=True, append_images=images[1:], duration=duration, loop=0)
    if args.sheet:
        picks = np.linspace(0, count-1, args.sheet_frames).round().astype(int)
        images = render(args.trace, picks, args.scale, args.pad, args.wire, args.bones, args.heat, background)
        w, h = images[0].size
        cols = min(4, len(images))
        rows = -(-len(images)//cols)
        sheet = Image.new('RGB', (w*cols, h*rows), tuple(background))
        for k, image in enumerate(images):
            sheet.paste(image, ((k % cols)*w, (k//cols)*h))
            ImageDraw.Draw(sheet).text(((k % cols)*w+4, (k//cols)*h+4), f'f{picks[k]}', fill=(0, 0, 0))
        Path(args.sheet).parent.mkdir(parents=True, exist_ok=True)
        sheet.save(args.sheet)
    print(json.dumps({'status': 'RENDERED', 'gif': args.gif, 'sheet': args.sheet, 'review': 'human visual review required'}))


if __name__ == '__main__':
    try:
        main()
    except SkinError as error:
        raise SystemExit(f'BLOCKED: {error}')
