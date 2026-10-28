"""Render the README figures for this case from a run.py output directory.

  python examples/pelican-bicycle/make_figures.py --run /tmp/pelican-review

Writes into docs/:
  preview.gif   the whole scene, one 2 s loop
  fish.gif      close-up of the fish skinned in the pouch
  wheel.gif     the rear tyre squashing over stones
  layers.png    every layer, back to front
  weights.png   Spine-style weights views (leg, neck, fish, tyre)
  compare.png   harmonic vs rigid nearest-bone weights, worst frame, folds circled
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'skills/2d/skin-weights/scripts'))
from render_skin import PALETTE, render, visible_triangles  # noqa: E402
from skinlib import signed_areas  # noqa: E402

BG = (238, 232, 220)
INK = (46, 40, 56)
DOCS = HERE / 'docs'
SCENE = [-62, -40, 62, 68]


def font(size):
    for name in ('/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def subset(trace_path, names):
    """Write a trace holding only some meshes, beside the original so image paths still resolve."""
    trace = json.loads(Path(trace_path).read_text())
    trace['meshes'] = {k: v for k, v in trace['meshes'].items() if k in names}
    trace['drawOrder'] = [k for k in trace['drawOrder'] if k in names]
    for frame in trace['frames']:
        frame['meshes'] = {k: frame['meshes'][k] for k in trace['drawOrder']}
    out = Path(trace_path).with_name('_subset.trace.json')
    out.write_text(json.dumps(trace))
    return out


def label(image, text, sub=None):
    draw = ImageDraw.Draw(image)
    draw.text((18, 14), text, fill=INK, font=font(26))
    if sub:
        draw.text((18, 46), sub, fill=(110, 104, 120), font=font(18))
    return image


def inverted_per_frame(trace_path, names):
    """Visible inverted triangles per frame over the named meshes."""
    trace = json.loads(Path(trace_path).read_text())
    counts = np.zeros(len(trace['frames']), dtype=int)
    for name in names:
        m = trace['meshes'][name]
        tri = np.array(m['triangles']).reshape(-1, 3)
        rest = np.sign(signed_areas(np.array(m['setupVertices']).reshape(-1, 2), tri))
        alpha = np.array(Image.open(Path(trace_path).parent / m['image']).convert('RGBA').getchannel('A'))
        ink = visible_triangles(np.array(m['uvs']).reshape(-1, 2), tri, alpha)
        for k, f in enumerate(trace['frames']):
            counts[k] += int(((np.sign(signed_areas(np.array(f['meshes'][name]).reshape(-1, 2), tri)) != rest) & ink).sum())
    return counts


def most_deformed_frame(trace_path, name):
    trace = json.loads(Path(trace_path).read_text())
    rest = np.array(trace['meshes'][name]['setupVertices']).reshape(-1, 2)
    return int(np.argmax([np.abs(np.array(f['meshes'][name]).reshape(-1, 2) - rest).mean() for f in trace['frames']]))


def gif(path, frames, duration):
    palette = frames[0].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    quant = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    quant[0].save(path, save_all=True, append_images=quant[1:], duration=duration, loop=0, optimize=True)


def layers_sheet(rig_path):
    rig = json.loads(rig_path.read_text())
    tiles = []
    for name in rig['drawOrder']:
        part = next(p for p in rig['parts'] if p['name'] == name)
        art = Image.open(rig_path.parent / part['image']).convert('RGBA')
        art.thumbnail((210, 170), Image.LANCZOS)
        tile = Image.new('RGB', (240, 250), (250, 247, 240))
        checker = Image.new('RGB', (220, 180), (244, 240, 232))
        d = ImageDraw.Draw(checker)
        for y in range(0, 180, 12):
            for x in range(0, 220, 12):
                if (x//12 + y//12) % 2:
                    d.rectangle([x, y, x + 11, y + 11], fill=(234, 229, 219))
        tile.paste(checker, (10, 10))
        tile.paste(art, (10 + (220 - art.width)//2, 10 + (180 - art.height)//2), art)
        draw = ImageDraw.Draw(tile)
        draw.text((12, 196), name, fill=INK, font=font(19))
        many = len(part['bones']) > 1
        kind = f'weighted · {len(part["bones"])} bones' if many else 'rigid · ' + part['bones'][0]
        draw.text((12, 222), kind, fill=(46, 120, 128) if many else (120, 114, 130), font=font(13))
        tiles.append(tile)
    cols = 6
    rows = -(-len(tiles)//cols)
    sheet = Image.new('RGB', (cols*250 + 10, rows*260 + 80), BG)
    label(sheet, f'{len(tiles)} layers, back to front', 'weighted meshes bend across joints; rigid layers follow one bone')
    for k, tile in enumerate(tiles):
        sheet.paste(tile, (10 + (k % cols)*250, 80 + (k//cols)*260))
    return sheet


def legend(canvas, entries):
    draw = ImageDraw.Draw(canvas)
    x = 20
    for colour, text in entries:
        draw.rectangle([x, canvas.height - 34, x + 20, canvas.height - 14], fill=colour)
        draw.text((x + 28, canvas.height - 36), text, fill=INK, font=font(18))
        x += 40 + int(draw.textlength(text, font=font(18)))


def weights_panel(harmonic, names, title, frame, scale):
    sub = subset(harmonic, names)
    image = render(sub, [frame], scale, 2, False, False, None, BG, weights_view=True, supersample=2)[0]
    sub.unlink()
    canvas = Image.new('RGB', (max(image.width, 440), image.height + 120), BG)
    canvas.paste(image, ((canvas.width - image.width)//2, 80))
    label(canvas, title)
    meshes = json.loads(Path(harmonic).read_text())['meshes']
    entries = []
    for name in names:
        influences = sorted({i['bone'] for row in meshes[name]['weights'] for i in row})
        if len(influences) == 1:
            entries.append(((150, 150, 160), f'{influences[0]} (rigid)'))
        elif len(influences) > 5:
            entries += [(PALETTE[k % len(PALETTE)], influences[k].rsplit('_', 1)[-1]) for k in range(len(influences))]
        else:
            entries += [(PALETTE[k % len(PALETTE)], bone) for k, bone in enumerate(influences)]
    legend(canvas, entries)
    return canvas


def compare_row(harmonic, nearest, names, view, scale, title):
    counts = inverted_per_frame(nearest, names)
    frame = int(counts.argmax())
    panels = []
    for path, head in ((harmonic, 'Harmonic weights · PASS'), (nearest, 'Rigid nearest bone · FAIL')):
        sub = subset(path, names)
        image = render(sub, [frame], scale, 0, False, False, None, BG, supersample=2, rings=True, view=view)[0]
        sub.unlink()
        canvas = Image.new('RGB', (image.width, image.height + 74), BG)
        canvas.paste(image, (0, 74))
        total = int(counts[frame]) if 'FAIL' in head else 0
        panels.append(label(canvas, f'{title}: {head}', f'frame {frame} · {total} inverted triangles' + (', circled' if total else '')))
    return panels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True, help='output directory of run.py')
    args = parser.parse_args()
    DOCS.mkdir(exist_ok=True)
    harmonic, nearest = args.run / 'harmonic.trace.json', args.run / 'nearest.trace.json'

    gif(DOCS / 'preview.gif', render(harmonic, range(0, 120, 3), 3.4, 0, False, False, None, BG, supersample=2, view=SCENE), 50)

    close = subset(harmonic, ['pouch', 'fish', 'head', 'neck'])
    gif(DOCS / 'fish.gif', render(close, range(0, 120, 3), 11, 0, False, False, None, BG, supersample=2, view=[8, -44, 56, -2]), 50)
    close.unlink()

    wheel_scene = subset(harmonic, ['sky', 'hills', 'road', 'stones', 'shadow', 'wheel_r', 'tyre_r', 'frame', 'crank', 'pebble_r', 'leg_n', 'foot_n', 'pedal_n'])
    gif(DOCS / 'wheel.gif', render(wheel_scene, range(0, 36, 1), 9, 0, False, False, None, BG, supersample=2, view=[-62, 14, -8, 66]), 60)
    wheel_scene.unlink()

    layers_sheet(HERE / 'source/rig.json').save(DOCS / 'layers.png', optimize=True)

    panels = [weights_panel(harmonic, ['leg_n', 'foot_n'], 'Near leg: thigh, shin + rigid foot', 87, 11),
              weights_panel(harmonic, ['neck'], 'Neck: neck1, neck2', 30, 11),
              weights_panel(harmonic, ['fish'], 'Fish: four-bone spine', 14, 16),
              weights_panel(harmonic, ['tyre_r'], 'Tyre: eight ring bones, max squash', most_deformed_frame(harmonic, 'tyre_r'), 11)]
    cells = [(0, 1), (2, 3)]
    rows = [(max(panels[a].height, panels[b].height), panels[a], panels[b]) for a, b in cells]
    width = max(a.width + b.width for _, a, b in rows) + 30
    sheet = Image.new('RGB', (width, sum(h for h, _, _ in rows) + 100), BG)
    label(sheet, 'Weights view (Spine-style)', 'one colour per bone; blends mark the harmonic transition between rigid cores')
    y = 90
    for h, a, b in rows:
        sheet.paste(a, (10, y))
        sheet.paste(b, (20 + a.width, y))
        y += h
    sheet.save(DOCS / 'weights.png', optimize=True)

    rows = [compare_row(harmonic, nearest, ['leg_f', 'foot_f', 'pedal_f', 'crank', 'pedal_n', 'foot_n', 'leg_n'], [-24, -4, 20, 50], 10, 'Legs'),
            compare_row(harmonic, nearest, ['tyre_r', 'wheel_r', 'stones', 'road'], [-60, 18, -12, 62], 10, 'Rear tyre'),
            compare_row(harmonic, nearest, ['pouch', 'fish', 'head'], [14, -40, 50, -6], 12, 'Fish')]
    width = max(a.width + b.width for a, b in rows) + 30
    out = Image.new('RGB', (width, sum(max(a.height, b.height) for a, b in rows) + 20), BG)
    y = 10
    for a, b in rows:
        out.paste(a, (10, y))
        out.paste(b, (20 + a.width, y))
        y += max(a.height, b.height)
    out.save(DOCS / 'compare.png', optimize=True)
    print(json.dumps({'written': sorted(p.name for p in DOCS.iterdir())}))


if __name__ == '__main__':
    main()
