"""Render an ogs.skin-trace/1 with one fixed camera for visual review.

Textured triangles are sampled through their UVs (bilinear, premultiplied alpha),
supersampled, and composited in the trace's drawOrder. Overlays: mesh wireframe,
Spine-style bones (`--bones`, from the trace's `skeleton`; origins only when it is
absent), IK chains/targets and follow-contacts (`--constraints`), and inverted
(folded) triangles in red. `--heat BONE` paints one
bone's weight; `--weights` tints every weighted part by its bones (a Spine-style
weights view, rigid parts greyed). Writes a GIF and/or a contact sheet PNG.
Review output is evidence for a human, not an acceptance verdict.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from skinlib import SkinError, signed_areas


def bilinear(texture, u, v):
    """Premultiplied-alpha bilinear sample; texture is float RGBA with RGB premultiplied."""
    th, tw = texture.shape[:2]
    x = np.clip(u*tw - 0.5, 0, tw - 1)
    y = np.clip(v*th - 0.5, 0, th - 1)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    x1, y1 = np.minimum(x0 + 1, tw - 1), np.minimum(y0 + 1, th - 1)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    top = texture[y0, x0]*(1 - fx) + texture[y0, x1]*fx
    bottom = texture[y1, x0]*(1 - fx) + texture[y1, x1]*fx
    rgba = top*(1 - fy) + bottom*fy
    alpha = rgba[..., 3:4]
    rgba[..., :3] = np.where(alpha > 1e-6, rgba[..., :3]*255/np.maximum(alpha, 1e-6), 0)
    return rgba


def visible_triangles(uv, triangles, alpha, threshold=32):
    """True for triangles whose UV area touches visible ink; folds over transparent canvas are not drawn red."""
    height, width = alpha.shape
    pixels = uv*[width, height]
    out = np.zeros(len(triangles), dtype=bool)
    for k, ids in enumerate(triangles):
        q = pixels[ids]
        x0, y0 = np.maximum(np.floor(q.min(0)).astype(int), 0)
        x1, y1 = np.minimum(np.ceil(q.max(0)).astype(int) + 1, [width, height])
        if x1 <= x0 or y1 <= y0:
            continue
        mask = Image.new('L', (int(x1 - x0), int(y1 - y0)))
        ImageDraw.Draw(mask).polygon([tuple(v - [x0, y0]) for v in q], fill=255)
        out[k] = bool(((np.array(mask) > 0) & (alpha[y0:y1, x0:x1] > threshold)).any())
    return out


def premultiply(image):
    data = np.array(image.convert('RGBA'), dtype=float)
    data[..., :3] *= data[..., 3:4]/255
    return data


def raster_triangle(canvas, points, uv, texture, colour=None, tint=None):
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
        u = l1*uv[0, 0] + l2*uv[1, 0] + l3*uv[2, 0]
        v = l1*uv[0, 1] + l2*uv[1, 1] + l3*uv[2, 1]
        rgba = bilinear(texture, u, v)
        if tint is not None:
            t = l1[..., None]*tint[0] + l2[..., None]*tint[1] + l3[..., None]*tint[2]
            rgba[..., :3] = 0.35*rgba[..., :3] + 0.65*t
    region = canvas[y0:y1, x0:x1]
    alpha = (rgba[..., 3:4]/255.0)*inside[..., None]
    region[..., :3] = rgba[..., :3]*alpha + region[..., :3]*(1-alpha)
    region[..., 3:4] = np.maximum(region[..., 3:4], 255*alpha)


def camera(trace, scale, pad, view=None):
    if view is not None:   # explicit world window: scrolling backdrops would otherwise stretch the fitted camera
        lo = np.array(view[:2], float)
        return lo, np.ceil((np.array(view[2:], float) - lo)*scale).astype(int)
    allv = np.concatenate([np.array(f['meshes'][n]).reshape(-1, 2) for f in trace['frames'] for n in trace['meshes']])
    lo, hi = allv.min(0) - pad, allv.max(0) + pad
    size = np.ceil((hi - lo)*scale).astype(int)
    return lo, size


PALETTE = [(232, 72, 85), (50, 140, 230), (250, 190, 40), (60, 180, 120), (160, 90, 220), (240, 130, 50), (30, 180, 190), (150, 110, 80)]


BONE, BONE_EDGE, IK, IK_EDGE, CONTACT = (70, 150, 235, 150), (20, 70, 150, 255), (235, 70, 170, 170), (150, 20, 100, 255), (20, 170, 120, 255)


def _point(matrix, local):
    return np.array([matrix['a']*local[0] + matrix['b']*local[1] + matrix['x'], matrix['c']*local[0] + matrix['d']*local[1] + matrix['y']])


def draw_skeleton(image, trace, frame, origin, scale, line, bones, constraints, bone_names=None):
    """Spine-style overlay: tapered bones from origin to tip, zero-length bones as rings; IK chains in magenta with a
    dashed root->target line and a target crosshair; follow-contacts as green squares on their targets."""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    skeleton = {b['name']: b for b in trace.get('skeleton', [])}
    world = frame['bones']
    to_px = lambda p: (np.asarray(p, float) - origin)*scale
    chain = {b for ik in (trace.get('constraints', {}).get('ik', []) if constraints else []) for b in ik['bones']}
    if bones:
        for name, m in world.items():
            if bone_names is not None and name not in bone_names:
                continue
            o = to_px([m['x'], m['y']])
            length = skeleton.get(name, {}).get('length', 0)
            fill, edge = (IK, IK_EDGE) if name in chain else (BONE, BONE_EDGE)
            if length > 0:
                tip = to_px(_point(m, [length, 0]))
                u = tip - o
                n = np.array([-u[1], u[0]])/max(1e-9, float(np.hypot(*u)))
                w = min(max(2.0*line, 0.1*float(np.hypot(*u))), 7.0*line)
                shape = [tuple(o), tuple(o + 0.2*u + n*w), tuple(tip), tuple(o + 0.2*u - n*w)]
                draw.polygon(shape, fill=fill, outline=edge, width=line)
            r = 2.2*line
            draw.ellipse([o[0]-r, o[1]-r, o[0]+r, o[1]+r], fill=(255, 255, 255, 230), outline=edge, width=line)
    if constraints:
        rig_c = trace.get('constraints', {})
        def target_px(spec):
            if 'fixed' in spec:
                return to_px(spec['fixed'])
            return to_px(_point(world[spec['bone']], spec.get('point', [0, 0])))
        for ik in rig_c.get('ik', []):
            root, target = to_px([world[ik['bones'][0]]['x'], world[ik['bones'][0]]['y']]), target_px(ik['target'])
            seg = target - root
            steps = max(2, int(float(np.hypot(*seg))/(6*line)))
            for k in range(0, steps, 2):
                a, b = root + seg*k/steps, root + seg*min(k + 1, steps)/steps
                draw.line([tuple(a), tuple(b)], fill=IK_EDGE, width=line)
            r = 5*line
            draw.ellipse([target[0]-r, target[1]-r, target[0]+r, target[1]+r], outline=IK_EDGE, width=line)
            draw.line([(target[0]-1.6*r, target[1]), (target[0]+1.6*r, target[1])], fill=IK_EDGE, width=line)
            draw.line([(target[0], target[1]-1.6*r), (target[0], target[1]+1.6*r)], fill=IK_EDGE, width=line)
            try:
                font = ImageFont.load_default(size=max(10, 9*line))
            except TypeError:          # Pillow < 10.1 has no sized default font
                font = ImageFont.load_default()
            draw.text((target[0] + 1.8*r, target[1] - 2.6*r), f'IK {ik["name"]}', fill=IK_EDGE, font=font)
        for contact in rig_c.get('contacts', []):
            p = target_px(contact['target'])
            r = 2.6*line
            draw.rectangle([p[0]-r, p[1]-r, p[0]+r, p[1]+r], outline=CONTACT, width=line)
    return Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')


def render(trace_path, frames, scale, pad, wire, bones, heat, background, weights_view=False, supersample=2, rings=False, view=None,
           constraints=False, bone_names=None, fade=0.0):
    scale = scale*supersample
    trace_path = Path(trace_path)
    trace = json.loads(trace_path.read_text())
    order = trace.get('drawOrder', list(trace['meshes']))
    textures, data = {}, {}
    for name in order:
        m = trace['meshes'][name]
        with Image.open(trace_path.parent / m['image']) as image:
            textures[name] = premultiply(image)
        tri = np.array(m['triangles']).reshape(-1, 3)
        rest = np.array(m['setupVertices']).reshape(-1, 2)
        heat_values = tint = None
        if heat:
            heat_values = np.array([sum(i['weight'] for i in row if i['bone'] == heat) for row in m['weights']])
        if weights_view:
            influences = sorted({i['bone'] for row in m['weights'] for i in row})
            tint = np.zeros((len(m['weights']), 3))
            for index, row in enumerate(m['weights']):
                for item in row:
                    colour = PALETTE[influences.index(item['bone']) % len(PALETTE)] if len(influences) > 1 else (150, 150, 160)
                    tint[index] += item['weight']*np.array(colour)
        uv = np.array(m['uvs']).reshape(-1, 2)
        ink = visible_triangles(uv, tri, np.array(Image.open(trace_path.parent / m['image']).convert('RGBA').getchannel('A')))
        data[name] = (tri, uv, np.sign(signed_areas(rest, tri)), heat_values, tint, ink)
    origin, size = camera(trace, scale, pad, view)
    images = []
    for index in frames:
        frame = trace['frames'][index]
        canvas = np.zeros((size[1], size[0], 4))
        canvas[..., :3] = background
        canvas[..., 3] = 255
        overlay = []
        for name in order:
            tri, uv, rest_sign, heat_values, tint, ink = data[name]
            posed = (np.array(frame['meshes'][name]).reshape(-1, 2) - origin)*scale
            flipped = (np.sign(signed_areas(posed, tri)) != rest_sign) & ink
            for k, ids in enumerate(tri):
                colour = heat_values[ids] if heat_values is not None else None
                raster_triangle(canvas, posed[ids], uv[ids], textures[name], colour, tint[ids] if tint is not None else None)
            if wire or flipped.any():
                overlay.append((posed, tri, flipped))
        if fade:   # wash the art toward the background so overlays read clearly
            canvas[..., :3] = canvas[..., :3]*(1 - fade) + np.array(background, float)*fade
        image = Image.fromarray(canvas.clip(0, 255).astype(np.uint8), 'RGBA').convert('RGB')
        draw = ImageDraw.Draw(image)
        line = max(1, supersample)
        for posed, tri, flipped in overlay:
            for k, ids in enumerate(tri):
                if flipped[k]:
                    draw.polygon([tuple(p) for p in posed[ids]], outline=(255, 0, 0), fill=(255, 0, 0), width=line)
                elif wire:
                    draw.polygon([tuple(p) for p in posed[ids]], outline=(40, 160, 255), width=line)
            if rings:
                for k in np.flatnonzero(flipped):
                    cx, cy = posed[tri[k]].mean(0)
                    r = 14*supersample
                    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(220, 30, 30), width=2*line)
        if bones or constraints:
            image = draw_skeleton(image, trace, frame, origin, scale, line, bones, constraints, bone_names)
        if supersample > 1:
            image = image.resize((max(1, round(image.width/supersample)), max(1, round(image.height/supersample))), Image.LANCZOS)
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
    parser.add_argument('--bones', action='store_true', help='Spine-style bones from the trace skeleton')
    parser.add_argument('--constraints', action='store_true', help='IK chains, IK targets and follow-contact targets')
    parser.add_argument('--bone-names', help='comma list: draw only these bones (default all)')
    parser.add_argument('--fade', type=float, default=0.0, help='0..1, wash the art toward the background under overlays')
    parser.add_argument('--heat')
    parser.add_argument('--weights', action='store_true', help='tint weighted parts by bone influence')
    parser.add_argument('--supersample', type=int, default=2)
    parser.add_argument('--rings', action='store_true', help='circle every folded triangle')
    parser.add_argument('--view', help='fixed world window x0,y0,x1,y1 (default: fit every mesh at every sample)')
    parser.add_argument('--background', default='238,232,220')
    args = parser.parse_args()
    background = [int(v) for v in args.background.split(',')]
    view = [float(v) for v in args.view.split(',')] if args.view else None
    names = set(args.bone_names.split(',')) if args.bone_names else None
    assert view is None or len(view) == 4, '--view needs x0,y0,x1,y1'
    count = len(json.loads(Path(args.trace).read_text())['frames'])
    if not (args.gif or args.sheet):
        raise SystemExit('nothing to write: pass --gif and/or --sheet')
    if args.gif:
        images = render(args.trace, range(0, count, args.every), args.scale, args.pad, args.wire, args.bones, args.heat, background, args.weights, args.supersample, args.rings, view, args.constraints, names, args.fade)
        Path(args.gif).parent.mkdir(parents=True, exist_ok=True)
        duration = max(20, int(1000*args.every/json.loads(Path(args.trace).read_text())['sampleRate']))
        images[0].save(args.gif, save_all=True, append_images=images[1:], duration=duration, loop=0)
    if args.sheet:
        picks = np.linspace(0, count-1, args.sheet_frames).round().astype(int)
        images = render(args.trace, picks, args.scale, args.pad, args.wire, args.bones, args.heat, background, args.weights, args.supersample, args.rings, view, args.constraints, names, args.fade)
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
