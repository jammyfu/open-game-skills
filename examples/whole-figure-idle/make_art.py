"""Paint ONE whole-figure image of a standing duck (repository-authored, MIT). No cut parts.

The figure is a single RGBA image, the input of whole-figure mode: the rig, weights and idle are
derived from it afterwards (measure_anatomy -> idle_motion -> solve). Supersampled for clean edges.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / 'source'
DENSITY, SS = 8, 3                 # source px per world unit, supersampling
W, H = 64, 72                      # world units; ground at y = 66
INK = (46, 40, 56, 255)
BODY, BODY_SHADE, WING, WING_DEEP = (250, 247, 238, 255), (226, 222, 212, 255), (236, 232, 222, 255), (204, 198, 190, 255)
ORANGE, ORANGE_DEEP, CHEEK = (242, 160, 70, 255), (214, 120, 46, 255), (246, 186, 178, 255)


class Canvas:
    def __init__(self):
        self.image = Image.new('RGBA', (W*DENSITY*SS, H*DENSITY*SS), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def p(self, q):
        return (q[0]*DENSITY*SS, q[1]*DENSITY*SS)

    def u(self, v):
        return max(1, int(round(v*DENSITY*SS)))

    def poly(self, pts, fill, outline=INK, width=0.45):
        pts = [self.p(q) for q in pts]
        self.draw.polygon(pts, fill=fill)
        if outline:
            self.draw.line(pts + [pts[0]], fill=outline, width=self.u(width), joint='curve')

    def ellipse(self, c, rx, ry, fill, outline=INK, width=0.45, n=96, angle=0.0):
        ca, sa = math.cos(angle), math.sin(angle)
        pts = [(c[0] + ca*rx*math.cos(t) - sa*ry*math.sin(t), c[1] + sa*rx*math.cos(t) + ca*ry*math.sin(t)) for t in np.linspace(0, 2*math.pi, n, endpoint=False)]
        self.poly(pts, fill, outline, width)

    def arc(self, c, r, a0, a1, fill, width):
        x, y = self.p(c)
        k = r*DENSITY*SS
        self.draw.arc([x - k, y - k, x + k, y + k], a0, a1, fill=fill, width=self.u(width))

    def line(self, pts, fill, width):
        self.draw.line([self.p(q) for q in pts], fill=fill, width=self.u(width), joint='curve')


def tube(a, b, wa, wb, n=24):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a)/np.linalg.norm(b - a)
    nrm = np.array([-d[1], d[0]])
    left = [a + (b - a)*t + nrm*(wa + (wb - wa)*t)/2 for t in np.linspace(0, 1, n)]
    right = [a + (b - a)*t - nrm*(wa + (wb - wa)*t)/2 for t in np.linspace(1, 0, n)]
    return left + right


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    c = Canvas()
    for x in (27.0, 37.0):                                                     # legs and webbed feet
        c.poly(tube((x, 54), (x - 0.6, 64.2), 2.2, 1.8), ORANGE)
        c.poly([(x - 4.6, 66.2), (x + 4.4, 66.2), (x + 3.0, 64.0), (x - 0.4, 63.4), (x - 3.4, 64.2)], ORANGE, width=0.4)
        for dx in (-2.2, 0.4, 2.8):
            c.line([(x - 0.4, 64.4), (x + dx, 66.0)], ORANGE_DEEP, 0.18)
    c.poly([(20.0, 37.0), (9.5, 32.5), (12.0, 38.6), (8.4, 41.4), (19.0, 46.0)], BODY_SHADE, width=0.4)    # tail tuft, tucked under the body
    c.ellipse((31.5, 44.0), 16.0, 12.0, BODY, width=0.5)                            # body
    c.ellipse((31.0, 50.5), 12.0, 4.6, BODY_SHADE, outline=None)                    # belly shade
    c.poly(tube((35.5, 34.5), (37.0, 21.0), 8.2, 6.4), BODY)                         # neck (a real bottleneck)
    c.ellipse((37.5, 15.5), 7.6, 7.0, BODY, width=0.5)                               # head
    c.poly(tube((35.5, 33.0), (37.0, 23.0), 7.0, 5.6), BODY, outline=None)          # hide the neck/head/body seams
    c.ellipse((31.5, 44.0), 15.4, 11.4, BODY, outline=None)
    t = np.linspace(0, 2*math.pi, 80, endpoint=False)                                # folded wing: a teardrop pointing back
    wing = [(30.0 + 11.5*math.cos(a)*(1 + 0.25*math.cos(a)), 42.5 + 6.4*math.sin(a) - 1.2*math.cos(a)) for a in t]
    c.poly(wing, WING, width=0.45)
    for row, (y, r) in enumerate(((40.0, 1.6), (43.4, 1.7), (46.6, 1.6))):
        for x in np.arange(23.0 + row, 37.0 - row, 2.6):
            c.arc((x, y), r, 20, 160, WING_DEEP, 0.24)
    c.poly([(43.6, 15.0), (52.4, 16.6), (52.8, 18.2), (44.0, 19.6)], ORANGE, width=0.4)   # beak
    c.line([(44.2, 17.4), (52.0, 17.4)], ORANGE_DEEP, 0.2)
    c.ellipse((40.4, 13.4), 1.15, 1.25, INK, outline=None)                           # eye
    c.ellipse((40.75, 13.0), 0.35, 0.35, (255, 255, 255, 255), outline=None)
    c.ellipse((39.6, 17.4), 1.6, 1.0, CHEEK, outline=None)
    for dx in (-1.2, 0.4, 1.8):                                                       # head tuft
        c.line([(36.0 + dx, 8.8), (35.0 + 1.6*dx, 5.8)], INK, 0.32)
    image = c.image.resize((W*DENSITY, H*DENSITY), Image.LANCZOS)
    image.save(OUT / 'duck.png', optimize=True)
    print(f'wrote {OUT / "duck.png"} ({image.width}x{image.height})')


if __name__ == '__main__':
    main()
