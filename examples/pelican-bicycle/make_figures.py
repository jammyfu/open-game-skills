"""Render the README figures for this case from a run.py output directory.

  python examples/pelican-bicycle/make_figures.py --run /tmp/pelican-review

Writes docs/preview.gif (one pedal cycle), docs/layers.png (every layer with its
influence bones), docs/weights.png (Spine-style weights view) and
docs/compare.png (harmonic vs rigid nearest-bone weights at the worst frame,
folded triangles in red).
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'skills/2d/skin-weights/scripts'))
from render_skin import PALETTE, render  # noqa: E402
from skinlib import signed_areas  # noqa: E402

BG = (238, 232, 220)
INK = (46, 40, 56)
DOCS = HERE / 'docs'


def font(size):
    for name in ('/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def worst_frame(trace_path):
    trace = json.loads(Path(trace_path).read_text())
    worst, frame = 0, 0
    for index, f in enumerate(trace['frames']):
        bad = 0
        for name, m in trace['meshes'].items():
            tri = np.array(m['triangles']).reshape(-1, 3)
            rest = np.sign(signed_areas(np.array(m['setupVertices']).reshape(-1, 2), tri))
            bad += int((np.sign(signed_areas(np.array(f['meshes'][name]).reshape(-1, 2), tri)) != rest).sum())
        if bad > worst:
            worst, frame = bad, index
    return frame, worst


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
        kind = 'weighted · ' + ', '.join(part['bones']) if len(part['bones']) > 1 else 'rigid · ' + part['bones'][0]
        draw.text((12, 222), kind, fill=(46, 120, 128) if len(part['bones']) > 1 else (120, 114, 130), font=font(13))
        tiles.append(tile)
    cols = 5
    rows = -(-len(tiles)//cols)
    sheet = Image.new('RGB', (cols*250 + 10, rows*260 + 80), BG)
    label(sheet, f'{len(tiles)} layers, back to front', 'weighted meshes bend across joints; rigid layers follow one bone')
    for k, tile in enumerate(tiles):
        sheet.paste(tile, (10 + (k % cols)*250, 80 + (k//cols)*260))
    return sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True, help='output directory of run.py')
    args = parser.parse_args()
    DOCS.mkdir(exist_ok=True)
    harmonic, nearest = args.run / 'harmonic.trace.json', args.run / 'nearest.trace.json'

    frames = render(harmonic, range(0, 120, 3), 3.6, 3, False, False, None, BG, supersample=2)
    palette = frames[0].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    gif = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    gif[0].save(DOCS / 'preview.gif', save_all=True, append_images=gif[1:], duration=50, loop=0, optimize=True)

    layers_sheet(HERE / 'source/rig.json').save(DOCS / 'layers.png', optimize=True)

    panels = []
    for names, title, frame in ((['leg_n', 'foot_n'], 'Near leg: thigh, shin + rigid foot', 87), (['neck'], 'Neck: neck1, neck2', 30)):
        sub = subset(harmonic, names)
        image = render(sub, [frame], 11, 2, False, False, None, BG, weights_view=True, supersample=2)[0]
        sub.unlink()
        canvas = Image.new('RGB', (max(image.width, 440), image.height + 120), BG)
        canvas.paste(image, ((canvas.width - image.width)//2, 80))
        label(canvas, title)
        meshes = json.loads(harmonic.read_text())['meshes']
        entries = []
        for name in names:
            influences = sorted({i['bone'] for row in meshes[name]['weights'] for i in row})
            if len(influences) > 1:
                entries += [(PALETTE[k % len(PALETTE)], bone) for k, bone in enumerate(influences)]
            else:
                entries.append(((150, 150, 160), f'{influences[0]} (rigid)'))
        draw = ImageDraw.Draw(canvas)
        x = 20
        for colour, text in entries:
            draw.rectangle([x, canvas.height - 34, x + 20, canvas.height - 14], fill=colour)
            draw.text((x + 28, canvas.height - 36), text, fill=INK, font=font(18))
            x += 40 + int(draw.textlength(text, font=font(18)))
        panels.append(canvas)
    height = max(p.height for p in panels)
    sheet = Image.new('RGB', (sum(p.width for p in panels) + 30, height + 90), BG)
    label(sheet, 'Weights view (Spine-style)', 'one colour per bone; the blend band is the harmonic transition between rigid cores')
    x = 10
    for panel in panels:
        sheet.paste(panel, (x, 84))
        x += panel.width + 10
    sheet.save(DOCS / 'weights.png', optimize=True)

    frame, bad = worst_frame(nearest)
    crops = []
    for path, title in ((harmonic, 'Harmonic weights · PASS'), (nearest, f'Rigid nearest bone · FAIL')):
        sub = subset(path, ['leg_f', 'foot_f', 'pedal_f', 'crank', 'pedal_n', 'foot_n', 'leg_n'])
        image = render(sub, [frame], 10, 3, False, False, None, BG, supersample=2, rings=True)[0]
        sub.unlink()
        canvas = Image.new('RGB', (image.width, image.height + 70), BG)
        canvas.paste(image, (0, 70))
        crops.append(label(canvas, title, f'frame {frame}' + (f' · {bad} inverted triangles, circled' if 'FAIL' in title else ' · 0 inverted triangles')))
    out = Image.new('RGB', (sum(c.width for c in crops) + 30, crops[0].height + 20), BG)
    x = 10
    for crop in crops:
        out.paste(crop, (x, 10))
        x += crop.width + 10
    out.save(DOCS / 'compare.png', optimize=True)
    print(json.dumps({'written': sorted(p.name for p in DOCS.iterdir()), 'compareFrame': frame}))


if __name__ == '__main__':
    main()
