"""Generate the layered pelican-on-a-bicycle test character (repository-authored, MIT).

Writes source/rig.json, source/motion.json and one RGBA PNG per layer. The setup
skeleton is solved first (both ankles reach their pedals at crank angle 0); every
layer is then painted in its own bones' local space, so drawing and skeleton agree
by construction. Layers are painted with hidden overlap at the knee, ankle, neck
base and head socket, and supersampled for clean anti-aliased edges.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'skills/2d/skin-weights/scripts'))
from skinlib import apply, forward  # noqa: E402

DENSITY = 8          # source pixels per world unit
SS = 3               # supersampling factor while painting
OUT = HERE / 'source'

INK = (46, 40, 56, 255)
FEATHER = (251, 249, 244, 255)
FEATHER_SHADE = (226, 224, 219, 255)
FEATHER_DEEP = (198, 196, 196, 255)
NECK = (252, 246, 228, 255)
CREST = (250, 222, 140, 255)
BEAK = (242, 160, 78, 255)
BEAK_TIP = (212, 76, 62, 255)
POUCH = (247, 190, 116, 255)
LEG = (244, 150, 62, 255)
LEG_SHADE = (214, 118, 44, 255)
LEG_FAR = (205, 121, 55, 255)
LEG_FAR_SHADE = (172, 96, 40, 255)
PRIMARY = (66, 62, 74, 255)
FRAME = (32, 132, 140, 255)
FRAME_LIGHT = (118, 204, 204, 255)
STEEL = (196, 202, 210, 255)
STEEL_DARK = (128, 134, 146, 255)
TYRE = (44, 42, 50, 255)
SADDLE = (96, 62, 46, 255)
GRIP = (58, 52, 60, 255)

TYRE_R, RIM_R, RING_R, TYRE_T = 17.6, 12.8, 15.2, 2.4   # tyre outer / rim / ring-bone radius / half thickness
P = 2*math.pi*TYRE_R            # road period: exactly one tyre revolution
V = P                           # ride speed, world units per second (one revolution per second)
GROUND = 57.6                   # road surface y
STONES = [(-19.4, 6.5, 4.2), (30.0, 4.2, 2.5), (74.0, 5.2, 3.1)]   # centre x at t=0, half width, height
PEBBLE_HOME = {'r': (-44.0, 60.0), 'f': (44.0, 60.0)}
CRANK = 7.0
HIP = (2.0, 3.0)                 # hip, local to pelvis
PEDAL_GRIP = (-2.2, -1.1)        # ankle target on each pedal (local): foot crosses the pedal


def two_bone(start, target, l1, l2, bend=1):
    dx, dy = target[0]-start[0], target[1]-start[1]
    d = math.hypot(dx, dy)
    inner = math.acos((l1*l1 + d*d - l2*l2)/(2*l1*d))
    knee = math.acos((l1*l1 + l2*l2 - d*d)/(2*l1*l2))
    return math.degrees(math.atan2(dy, dx) - bend*inner), math.degrees(bend*(math.pi - knee))


def bones():
    pelvis = (-11.0, 6.0)
    bb = (-2.0, 38.0)
    hip = (pelvis[0]+HIP[0], pelvis[1]+HIP[1])
    near = two_bone(hip, (bb[0]+CRANK+PEDAL_GRIP[0], bb[1]+PEDAL_GRIP[1]), 19, 19)
    far = two_bone(hip, (bb[0]-CRANK+PEDAL_GRIP[0], bb[1]+PEDAL_GRIP[1]), 19, 19)
    rig = [
        {'name': 'root'},
        {'name': 'bike', 'parent': 'root'},
        {'name': 'wheel_r', 'parent': 'bike', 'x': -36, 'y': 40},
        {'name': 'wheel_f', 'parent': 'bike', 'x': 36, 'y': 40},
        {'name': 'tyre_r', 'parent': 'bike', 'x': -36, 'y': 40},
        {'name': 'tyre_f', 'parent': 'bike', 'x': 36, 'y': 40},
        {'name': 'crank', 'parent': 'bike', 'x': bb[0], 'y': bb[1], 'length': CRANK},
        {'name': 'pedal_n', 'parent': 'crank', 'x': CRANK, 'y': 0, 'inheritRotation': False},
        {'name': 'pedal_f', 'parent': 'crank', 'x': -CRANK, 'y': 0, 'inheritRotation': False},
        {'name': 'pelvis', 'parent': 'root', 'x': pelvis[0], 'y': pelvis[1]},
        {'name': 'body', 'parent': 'pelvis', 'x': 0, 'y': -2, 'rotation': -14, 'length': 22},
        {'name': 'neck1', 'parent': 'body', 'x': 20, 'y': -4, 'rotation': -68, 'length': 12},
        {'name': 'neck2', 'parent': 'neck1', 'x': 12, 'y': 0, 'rotation': 36, 'length': 11},
        {'name': 'head', 'parent': 'neck2', 'x': 11, 'y': 0, 'rotation': 52, 'length': 6},
        {'name': 'wing', 'parent': 'body', 'x': 15, 'y': -3, 'rotation': 172, 'length': 24},
        # fish held in the pouch: four-bone spine, each bone 4.6 long
        {'name': 'fish_root', 'parent': 'head', 'x': 6.5, 'y': 3.6, 'rotation': 6, 'length': 4.6},
        {'name': 'fish_b1', 'parent': 'fish_root', 'x': 4.6, 'length': 4.6},
        {'name': 'fish_b2', 'parent': 'fish_b1', 'x': 4.6, 'length': 4.6},
        {'name': 'fish_b3', 'parent': 'fish_b2', 'x': 4.6, 'length': 4.8},
        # scrolling backdrop (fixed in world, translated by tracks) and kicked-up pebbles
        {'name': 'clouds', 'parent': 'root'},
        {'name': 'hills', 'parent': 'root'},
        {'name': 'road', 'parent': 'root'},
        {'name': 'pebble_r', 'parent': 'root', 'x': PEBBLE_HOME['r'][0], 'y': PEBBLE_HOME['r'][1]},
        {'name': 'pebble_f', 'parent': 'root', 'x': PEBBLE_HOME['f'][0], 'y': PEBBLE_HOME['f'][1]},
    ]
    for wheel, cx in (('r', -36), ('f', 36)):   # eight zero-length ring bones around each tyre
        for j in range(8):
            a = math.radians(45*j)
            rig.append({'name': f'tyre_{wheel}_{j}', 'parent': f'tyre_{wheel}', 'x': RING_R*math.cos(a), 'y': RING_R*math.sin(a)})
    for side, (upper, lower) in (('n', near), ('f', far)):
        rig += [
            {'name': f'thigh_{side}', 'parent': 'pelvis', 'x': HIP[0], 'y': HIP[1], 'rotation': upper, 'length': 19},
            {'name': f'shin_{side}', 'parent': f'thigh_{side}', 'x': 19, 'y': 0, 'rotation': lower, 'length': 19},
            {'name': f'foot_{side}', 'parent': f'shin_{side}', 'x': 19, 'y': 0, 'inheritRotation': False, 'length': 6},
        ]
    return rig


class Layer:
    """One source image. Paints in world coordinates, supersampled, saved at DENSITY."""

    def __init__(self, lo, hi, density=DENSITY):
        self.d = density
        self.lo = np.floor(np.array(lo, float))
        hi = np.ceil(np.array(hi, float))
        self.size = ((hi - self.lo)*self.d).astype(int)
        self.image = Image.new('RGBA', tuple(self.size*SS), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def p(self, point):
        return tuple(((np.array(point, float) - self.lo)*self.d*SS).tolist())

    def u(self, units):
        return max(1, int(round(units*self.d*SS)))

    def poly(self, points, fill, outline=INK, width=0.45):
        pts = [self.p(q) for q in points]
        self.draw.polygon(pts, fill=fill)
        if outline is not None and width:
            self.draw.line(pts + [pts[0]], fill=outline, width=self.u(width), joint='curve')

    def circle(self, centre, r, fill, outline=INK, width=0.45):
        x, y = self.p(centre)
        k = r*self.d*SS
        self.draw.ellipse([x-k, y-k, x+k, y+k], fill=fill, outline=outline if width else None, width=self.u(width) if width else 0)

    def line(self, points, fill, width):
        self.draw.line([self.p(q) for q in points], fill=fill, width=self.u(width), joint='curve')
        for q in (points[0], points[-1]):
            self.circle(q, width/2, fill, outline=None, width=0)

    def feather(self, base, tip, width, fill, outline=INK, line=0.3):
        base, tip = np.array(base, float), np.array(tip, float)
        d = tip - base
        n = np.array([-d[1], d[0]])/np.linalg.norm(d)
        pts = [base + d*t + n*width/2*math.sin(math.pi*t)**0.8 for t in np.linspace(0, 1, 18)]
        pts += [base + d*t - n*width/2*math.sin(math.pi*t)**0.8 for t in np.linspace(1, 0, 18)[1:-1]]
        self.poly(pts, fill, outline=outline, width=line)

    def scallop(self, centre, r, angle_deg, fill, width=0.22):
        x, y = self.p(centre)
        k = r*self.d*SS
        self.draw.arc([x-k, y-k, x+k, y+k], angle_deg + 20, angle_deg + 160, fill=fill, width=self.u(width))

    def save(self, name):
        image = self.image.resize(tuple(self.size), Image.LANCZOS)
        image.save(OUT / f'{name}.png', optimize=True)
        return {'image': f'{name}.png', 'origin': [0, 0], 'at': self.lo.tolist(), 'density': self.d}


def ellipse_points(centre, rx, ry, angle=0.0, n=72, start=0.0, end=2*math.pi):
    c, s = math.cos(angle), math.sin(angle)
    out = []
    for t in np.linspace(start, end, n):
        x, y = rx*math.cos(t), ry*math.sin(t)
        out.append((centre[0] + c*x - s*y, centre[1] + s*x + c*y))
    return out


def tapered(a, b, wa, wb):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a)/np.linalg.norm(b - a)
    n = np.array([-d[1], d[0]])
    return [a + n*wa/2, b + n*wb/2, b - n*wb/2, a - n*wa/2]



FPS, N = 60, 120                 # two seconds at 60 Hz; sample N equals sample 0 (periodic)
TREAD_E, TREAD_CAP, LIFT_SHARE, SINK = 1.8, 3.6, 0.5, 0.6


def ground_height(x, t):
    """Stone profile above the road surface at world x, time t (road scrolls one period per second)."""
    x = np.asarray(x, float)
    g = np.zeros_like(x)
    offset = V*(t % 1.0)
    for xc, w, h in STONES:
        for k in range(-3, 4):
            d = x - (xc + k*P - offset)
            g += h*np.clip(1 - (d/w)**2, 0, None)**0.6
    return g


def rigid_lift(cx, t):
    """How far a rigid wheel of radius TYRE_R centred over cx rides up when it rolls over the stones."""
    u = np.arange(-TYRE_R, TYRE_R + 1e-9, 0.2)
    return float(np.max(ground_height(cx + u, t) + np.sqrt(np.clip(TYRE_R**2 - u**2, 0, None))) - TYRE_R)


def periodic_response(signal, omega0, zeta):
    """Steady-state response of a spring-damper to a periodic signal, solved in the frequency domain."""
    w = 2*np.pi*np.fft.rfftfreq(len(signal), 1/FPS)
    h = omega0**2/(omega0**2 - w**2 + 2j*zeta*omega0*w)
    spectrum = np.fft.rfft(signal)
    return np.fft.irfft(spectrum*h, len(signal)), np.fft.irfft(spectrum*h*(-w**2), len(signal))


def ride():
    """Everything the bump interaction needs, as arrays of N+1 samples (last equals first)."""
    ts = np.arange(N)/FPS
    lift = np.array([[rigid_lift(-36, t), rigid_lift(36, t)] for t in ts])*LIFT_SHARE
    heave = lift.mean(1)
    pitch = -(lift[:, 1] - lift[:, 0])/72                       # nose up when the front wheel is higher
    dy = -heave + SINK
    tyre = {}
    for wheel, wx in (('r', -36.0), ('f', 36.0)):
        offsets = np.zeros((N, 8, 2))
        for k, t in enumerate(ts):
            c, s_ = math.cos(pitch[k]), math.sin(pitch[k])
            cx, cy = c*wx - s_*40, s_*wx + c*40 + dy[k]
            push = np.zeros(8)
            for j in range(8):
                a = math.radians(45*j)
                px, py = cx + RING_R*math.cos(a), cy + RING_R*math.sin(a)
                reach = py + TYRE_T*max(0.0, math.sin(a)) - (GROUND - float(ground_height(np.array([px]), t)[0]))
                push[j] = min(TREAD_CAP, TREAD_E*max(0.0, reach))
            depth = push.max()
            for j in range(8):
                a = math.radians(45*j)
                offsets[k, j, 0] = 0.45*depth*math.cos(a)                    # sides bulge outward
                offsets[k, j, 1] = -push[j] + 0.3*depth*max(0.0, -math.sin(a))   # contact pushes up, crown sinks
        tyre[wheel] = offsets
    body, accel = periodic_response(dy, 2*np.pi*4.5, 0.22)       # pelican springs on the bike
    lag = body - dy
    fish_hop = -accel/max(1e-9, np.abs(accel).max())             # impulse-driven jump of the fish
    lag_n = lag/max(1e-9, np.abs(lag).max())
    pebbles = {}
    for wheel, wx in (('r', -36.0), ('f', 36.0)):                # the biggest stone is crushed and kicks a pebble back
        start = np.zeros((N, 2))
        te = ((STONES[0][0] - wx)/V) % 1.0
        home_y = PEBBLE_HOME[wheel][1]
        y0, vx, vy, g = 55.5, -22.0, -34.0, 140.0
        for k, t in enumerate(ts):
            for event in (te - 1, te, te + 1):
                tau = t - event
                y = y0 + vy*tau + 0.5*g*tau**2
                if 0 <= tau and y <= home_y:
                    start[k] = (wx - 4 + vx*tau - PEBBLE_HOME[wheel][0], y - home_y)
        pebbles[wheel] = start
    wrap = lambda a: np.concatenate([a, a[:1]], axis=0)
    return dict(heave=wrap(heave), pitch=wrap(np.degrees(pitch)), dy=wrap(dy), body=wrap(body), lag=wrap(lag_n), fish_hop=wrap(fish_hop),
                tyre={w: wrap(a) for w, a in tyre.items()}, pebbles={w: wrap(a) for w, a in pebbles.items()})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rig_bones = bones()
    lookup = {b['name']: b for b in rig_bones}
    world = forward({'bones': rig_bones, '_bones': lookup})
    at = lambda bone, local=(0, 0): np.array(apply(world[bone], list(local)), float)
    parts = []

    def part(name, layer, influences, **extra):
        parts.append(dict(name=name, bones=influences, **layer.save(name), **extra))

    rigid = {'mesh': {'spacing': 24, 'alphaThreshold': 32, 'margin': 2}}

    # ---- backdrop: sky, clouds, hills, road, stones. Content is periodic so a short scroll loops.
    sky = Layer((-66, -46), (66, GROUND + 0.8), density=2)
    top, bottom = np.array([150, 200, 232]), np.array([252, 232, 206])
    rows = 36
    for k in range(rows):
        y0 = -46 + (GROUND + 0.8 + 46)*k/rows
        y1 = -46 + (GROUND + 0.8 + 46)*(k + 1)/rows + 0.2
        c = tuple(int(v) for v in top + (bottom - top)*(k/(rows - 1))**1.3) + (255,)
        sky.poly([(-67, y0), (67, y0), (67, y1), (-67, y1)], c, outline=None)
    part('sky', sky, ['root'], mesh={'mode': 'quad'})

    PC = 96.0                     # cloud period: scrolls one period in 2 s (reset on loop)
    clouds = Layer((-66, -42), (66 + PC, -6), density=3)
    for xc, yc, s_ in ((-40, -28, 1.0), (14, -36, 0.8), (50, -24, 1.2)):
        for k in range(-1, 3):
            base = np.array([xc + k*PC, yc])
            for dx, dy, r in ((0, 0, 5.5), (5.5, 1.6, 4.4), (-5.5, 1.8, 4.0), (10.5, 3.2, 3.2), (-10, 3.4, 3.0)):
                clouds.circle(base + np.array([dx, dy])*s_, r*s_, (255, 255, 255, 235), outline=None, width=0)
            clouds.poly([base + np.array(q)*s_ for q in ([-12, 4.6], [13, 4.6], [13, 6.4], [-12, 6.4])], (255, 255, 255, 235), outline=None)
    part('clouds', clouds, ['clouds'], mesh={'mode': 'quad'})

    PH = 92.0                     # hill period
    hills = Layer((-66, 18), (66 + PH, GROUND + 0.8), density=3)
    def ridge(x, phase, base, amp):
        w = 2*math.pi/PH
        return base - amp*(0.55*math.sin(w*x + phase) + 0.3*math.sin(2*w*x + phase*1.7 + 1) + 0.15*math.sin(3*w*x + phase*0.6 + 2))
    xs = np.linspace(-66, 66 + PH, 220)
    for phase, base, amp, colour in ((0.0, 44, 17, (138, 176, 170, 255)), (2.2, 50, 12, (104, 152, 140, 255))):
        hills.poly([(x, ridge(x, phase, base, amp)) for x in xs] + [(66 + PH, GROUND + 1), (-66, GROUND + 1)], colour, outline=None)
    part('hills', hills, ['hills'], mesh={'mode': 'quad'})

    for wheel in ('r', 'f'):      # pebbles hide behind the road and are kicked out when a stone is crushed
        home = np.array(PEBBLE_HOME[wheel], float)
        pebble = Layer(home - 3, home + 3)
        pebble.poly([home + np.array(q) for q in ([-1.6, 0.4], [-0.9, -1.1], [0.8, -1.3], [1.7, -0.2], [1.1, 1.1], [-0.7, 1.3])], (156, 150, 156, 255), width=0.35)
        pebble.line([home + [-0.7, -0.5], home + [0.4, -0.7]], (206, 202, 206, 255), 0.3)
        part(f'pebble_{wheel}', pebble, [f'pebble_{wheel}'], mesh={'spacing': 12, 'alphaThreshold': 32, 'margin': 2})

    road = Layer((-66, GROUND), (66 + P, GROUND + 10.5), density=6)
    road.poly([(-67, GROUND), (67 + P, GROUND), (67 + P, GROUND + 11), (-67, GROUND + 11)], (96, 98, 112, 255), outline=None)
    road.poly([(-67, GROUND), (67 + P, GROUND), (67 + P, GROUND + 0.9), (-67, GROUND + 0.9)], (136, 138, 152, 255), outline=None)
    road.poly([(-67, GROUND + 8.6), (67 + P, GROUND + 8.6), (67 + P, GROUND + 11), (-67, GROUND + 11)], (74, 76, 90, 255), outline=None)
    for k in range(-1, 3):
        for n in range(8):   # lane dashes: eight per revolution so every dash lines up after one second
            x0 = k*P + n*P/8
            road.poly([(x0, GROUND + 4.6), (x0 + P/8*0.55, GROUND + 4.6), (x0 + P/8*0.55, GROUND + 5.5), (x0, GROUND + 5.5)], (238, 226, 160, 255), outline=None)
    rng = np.random.default_rng(7)
    for _ in range(46):          # gravel speckles, repeated every period
        x, y, r = rng.uniform(0, P), rng.uniform(GROUND + 1.3, GROUND + 8.2), rng.uniform(0.18, 0.4)
        shade = int(rng.integers(70, 150))
        for k in range(-1, 3):
            road.circle((x + k*P, y), r, (shade, shade, shade + 8, 255), outline=None, width=0)
    road.line([(-67, GROUND), (67 + P, GROUND)], INK, 0.45)
    part('road', road, ['road'], mesh={'mode': 'quad'})

    stones = Layer((-66, GROUND - 6), (66 + P, GROUND + 1), density=6)
    for xc, w, h in STONES:
        for k in range(-1, 3):
            d = np.linspace(-w, w, 40)
            crown = [(xc + k*P + t, GROUND + 0.3 - h*max(0.0, 1 - (t/w)**2)**0.6) for t in d]
            stones.poly(crown + [(xc + k*P + w, GROUND + 0.3), (xc + k*P - w, GROUND + 0.3)], (158, 152, 158, 255), width=0.45)
            lit = [(xc + k*P + t*0.8 - w*0.1, GROUND + 0.3 - h*0.92*max(0.0, 1 - (t/w)**2)**0.6) for t in np.linspace(-w*0.7, w*0.3, 14)]
            stones.line(lit, (206, 200, 206, 255), 0.35)
            stones.line([(xc + k*P + w*0.2, GROUND - h*0.35), (xc + k*P + w*0.45, GROUND - h*0.1)], (110, 104, 112, 255), 0.22)
    part('stones', stones, ['road'], mesh={'mode': 'quad'})

    shadow = Layer((-58, GROUND - 3), (58, GROUND + 5))
    shadow.poly(ellipse_points((0, GROUND + 0.6), 52, 2.2), (30, 28, 40, 80), outline=None)
    part('shadow', shadow, ['root'], **rigid)

    # ---- wheels: spoked rim spins rigidly; the tyre is a soft ring skinned to eight non-rotating bones
    for wheel in ('r', 'f'):
        c = at(f'wheel_{wheel}')
        rim = Layer(c - RIM_R - 1.2, c + RIM_R + 1.2)
        rim.circle(c, RIM_R + 0.4, (0, 0, 0, 0), outline=STEEL, width=1.1)
        rim.circle(c, RIM_R - 0.9, (0, 0, 0, 0), outline=STEEL_DARK, width=0.25)
        for k in range(16):
            a = math.pi*k/8
            offset = 1.2*np.array([math.cos(a + math.pi/2), math.sin(a + math.pi/2)])*(1 if k % 2 else -1)
            rim.line([c + offset, c + (RIM_R - 0.9)*np.array([math.cos(a), math.sin(a)])], STEEL_DARK, 0.22)
        rim.circle(c, 2.2, STEEL, width=0.35)
        rim.circle(c, 0.9, STEEL_DARK, width=0)
        rim.circle(c + [RIM_R - 2.4, 0], 0.55, (240, 120, 70, 255), width=0.2)         # reflector: shows the spin
        rim.line([c + [0, -(RIM_R - 0.6)], c + [0, -(RIM_R + 1.0)]], STEEL, 0.5)      # valve
        part(f'wheel_{wheel}', rim, [f'wheel_{wheel}'], **rigid)

        t = at(f'tyre_{wheel}')
        tyre = Layer(t - TYRE_R - 1.2, t + TYRE_R + 1.2)
        tyre.circle(t, TYRE_R, TYRE, width=0.45)
        tyre.circle(t, RIM_R, (0, 0, 0, 0), outline=INK, width=0.35)
        for a0, a1 in ((200, 262), (284, 304)):   # sidewall highlight
            x, y = tyre.p(t)
            k = RING_R*tyre.d*SS
            tyre.draw.arc([x - k, y - k, x + k, y + k], a0, a1, fill=(104, 100, 116, 255), width=tyre.u(0.7))
        part(f'tyre_{wheel}', tyre, [f'tyre_{wheel}_{j}' for j in range(8)],
             mesh={'spacing': 8, 'alphaThreshold': 32, 'margin': 3},
             weights={'handleRadius': 3.8, 'coreInset': 0.0, 'maxInfluences': 3, 'pruneBelow': 0.01})

    # legs: feathered thigh -> straight scaly shin ending in a round ankle knob (weighted mesh),
    # and a separate rigid webbed foot hinged under that knob (no mesh bend at the ankle)
    for side, skin, shade in (('f', LEG_FAR, LEG_FAR_SHADE), ('n', LEG, LEG_SHADE)):
        hip, knee, ankle = at(f'thigh_{side}'), at(f'shin_{side}'), at(f'foot_{side}')
        feather = FEATHER_SHADE if side == 'f' else FEATHER

        foot = Layer(ankle - 4, ankle + 9)
        web = [at(f'foot_{side}', q) for q in ([-1.0, -1.3], [5.8, -0.4], [7.6, 1.3], [5.2, 1.0], [4.4, 2.0], [2.6, 1.4], [-1.0, 1.3])]
        foot.poly(web, skin)
        for q in ([6.2, -0.2], [4.6, 1.7]):
            foot.line([at(f'foot_{side}', [0.6, 0]), at(f'foot_{side}', q)], shade, 0.22)
        foot.circle(at(f'foot_{side}', [7.5, 1.0]), 0.35, INK, width=0)
        part(f'foot_{side}', foot, [f'foot_{side}'], **rigid)

        pts = np.array([hip, knee, ankle])
        layer = Layer(pts.min(0) - 6, pts.max(0) + 6)
        d = (ankle - knee)/np.linalg.norm(ankle - knee)
        n = np.array([-d[1], d[0]])
        layer.poly(tapered(knee, ankle, 3.0, 2.4), skin)
        for k in range(1, 7):  # scutes along the shin
            q = knee + (ankle - knee)*k/7.5
            layer.line([q - n*1.1, q + n*1.1], shade, 0.22)
        layer.circle(ankle, 1.7, skin)  # ankle knob covers the foot hinge
        layer.circle(ankle, 0.6, shade, outline=None, width=0)
        layer.circle(knee, 2.5, feather)  # feathered "trouser" hides the knee cap
        layer.poly(tapered(hip, knee, 6.4, 5.0), feather)
        layer.circle(hip, 3.2, feather, outline=None, width=0)
        t = (knee - hip)/np.linalg.norm(knee - hip)
        m = np.array([-t[1], t[0]])
        deep = FEATHER_DEEP if side == 'f' else FEATHER_SHADE
        layer.poly([hip - m*2.9, knee - m*2.2, knee - m*1.2, hip - m*1.6], deep, outline=None)  # shaded back of the thigh
        for f in (0.35, 0.6, 0.85):  # feather tips overlapping toward the knee
            layer.scallop(hip + (knee - hip)*f + m*0.6, 1.6, math.degrees(math.atan2(t[1], t[0])) - 90, FEATHER_DEEP)
        layer.circle(knee + (ankle - knee)*0.06, 2.0, feather, outline=None, width=0)
        part(f'leg_{side}', layer, [f'thigh_{side}', f'shin_{side}'],
             mesh={'spacing': 10, 'alphaThreshold': 32, 'margin': 3},
             # The bend lives in the soft feathered thigh end; the thin shin stays straight.
             weights={'handleRadius': {f'thigh_{side}': 4.0, f'shin_{side}': 2.2},
                      'coreInset': {f'thigh_{side}': [0.1, 0.3], f'shin_{side}': [0.06, 0.0]},
                      'maxInfluences': 2, 'pruneBelow': 0.01},
             lint={'maxReach': 14.0})

    # pedals
    for side in ('f', 'n'):
        c = at(f'pedal_{side}')
        pedal = Layer(c - 4, c + 4)
        pedal.poly([c + [-3.0, -0.8], c + [3.0, -0.8], c + [3.0, 0.8], c + [-3.0, 0.8]], STEEL_DARK, width=0.3)
        pedal.line([c + [-2.4, 0], c + [2.4, 0]], STEEL, 0.4)
        part(f'pedal_{side}', pedal, [f'pedal_{side}'], **rigid)

    # frame: tubes, fork, saddle, handlebar, chain
    bb, rear, front = at('crank'), at('wheel_r'), at('wheel_f')
    seat_top, head_top, head_low = np.array([-10.5, 10.0]), np.array([24.0, 2.0]), np.array([26.5, 9.5])
    frame = Layer((-56, -6), (56, 58))
    chain_top = [bb + [0, -4.6], rear + [0, -2.2]]
    chain_low = [bb + [0, 4.6], rear + [0, 2.2]]
    for a, b in (chain_top, chain_low):
        frame.line([a, b], (92, 92, 104, 255), 0.5)
    frame.circle(rear, 2.5, STEEL_DARK, width=0.3)
    for a, b, w in ((rear, bb, 1.5), (rear, seat_top + [0.5, 2.5], 1.3), (bb, seat_top, 1.9), (seat_top + [0.8, 2.6], head_top + [0.2, 1.2], 1.9),
                    (bb, head_low, 2.2), (head_top, head_low, 2.3), (head_low, front, 1.6)):
        frame.line([a, b], INK, w + 0.8)
        frame.line([a, b], FRAME, w)
    frame.line([bb + [1, -3], head_low + [-1, -1]], FRAME_LIGHT, 0.4)
    frame.line([seat_top + [1, 1.6], head_top + [-0.6, 0.6]], FRAME_LIGHT, 0.4)
    frame.line([seat_top, seat_top + [-0.6, -3.2]], STEEL, 0.9)
    frame.poly([seat_top + [-7, -3.4], seat_top + [3.2, -4.2], seat_top + [4.4, -2.6], seat_top + [-6, -1.6]], SADDLE, width=0.4)
    stem = head_top + [0.5, -3.5]
    frame.line([head_top, stem], STEEL_DARK, 1.0)
    frame.line([stem, stem + [3.5, -0.4], stem + [5.5, 1.6]], STEEL, 0.9)
    frame.line([stem + [5.3, 1.4], stem + [5.9, 3.2]], GRIP, 1.3)
    frame.circle(front, 1.6, STEEL_DARK, width=0.3)
    part('frame', frame, ['bike'], **rigid)

    # crank: toothed chainring + arms (rotates)
    crank = Layer(bb - 9, bb + 9)
    teeth = []
    for k in range(64):
        r = 5.4 if k % 2 else 4.8
        a = 2*math.pi*k/64
        teeth.append(bb + r*np.array([math.cos(a), math.sin(a)]))
    crank.poly(teeth, STEEL_DARK, width=0.25)
    crank.circle(bb, 4.0, STEEL, width=0.25)
    for k in range(5):
        a = 2*math.pi*k/5
        crank.circle(bb + 2.4*np.array([math.cos(a), math.sin(a)]), 0.8, (0, 0, 0, 0), outline=STEEL_DARK, width=0.3)
    crank.line([bb - [CRANK, 0], bb + [CRANK, 0]], INK, 1.9)
    crank.line([bb - [CRANK, 0], bb + [CRANK, 0]], STEEL_DARK, 1.2)
    crank.circle(bb, 1.1, INK, width=0)
    part('crank', crank, ['crank'], **rigid)

    # neck: two weighted bones; base hides under the body, tip under the head
    n0, n1, n2 = at('neck1', (-2.5, 0)), at('neck2'), at('head')
    pts = np.array([n0, n1, n2])
    neck = Layer(pts.min(0) - 6, pts.max(0) + 6)
    neck.poly(tapered(n0, n1, 7.6, 6.2), NECK)
    neck.circle(n1, 3.1, NECK)
    neck.poly(tapered(n1, n2, 6.2, 5.2), NECK)
    neck.circle(n2, 2.6, NECK)
    neck.circle(n1, 3.1, NECK, outline=None, width=0)
    for t in np.linspace(0.15, 0.9, 6):  # throat feathering crosses the neck joint
        for bone, length in (('neck1', 12), ('neck2', 11)):
            neck.line([at(bone, (length*t, 1.2)), at(bone, (length*t + 1.0, 2.3))], FEATHER_SHADE, 0.3)
    part('neck', neck, ['neck1', 'neck2'], mesh={'spacing': 10, 'alphaThreshold': 32, 'margin': 3},
         weights={'handleRadius': {'neck1': 4.0, 'neck2': 3.4}, 'coreInset': {'neck1': 0.2, 'neck2': 0.25},
                  'maxInfluences': 2, 'pruneBelow': 0.01},
         lint={'maxReach': 14.0})

    # body: teardrop with tail fan and soft belly shading
    centre = at('body', (8, 0))
    angle = math.radians(-14)
    body_pts = ellipse_points(centre, 18, 11.5, angle)
    lo, hi = np.min(body_pts, 0) - 12, np.max(body_pts, 0) + 4
    body = Layer(lo, hi)
    for k, (dx, dy) in enumerate(((-19, -4.5), (-20.5, -1.0), (-19.5, 2.6), (-17, 5.4))):
        body.feather(at('body', (-6, 1.0 + 0.4*k)), at('body', (dx, dy)), 3.4, FEATHER_SHADE if k % 2 else FEATHER_DEEP, line=0.35)
    body.poly(body_pts, FEATHER, width=0.5)
    body.poly(ellipse_points(at('body', (9, 4)), 14, 5.5, angle, start=0.15, end=math.pi - 0.15), FEATHER_SHADE, outline=None)
    for row, y in enumerate((3.5, 6.5)):  # breast feathering
        for x in np.arange(4 + 1.5*row, 22 - 2*row, 2.8):
            body.scallop(at('body', (x, y)), 1.6, -14 + 90, FEATHER_DEEP, width=0.24)
    part('body', body, ['body'], mesh={'spacing': 16, 'alphaThreshold': 32, 'margin': 2})

    # wing: folded along the body, layered coverts and dark primaries
    wing = Layer(np.minimum(at('wing'), at('wing', (26, 0))) - 9, np.maximum(at('wing'), at('wing', (26, 0))) + 9)
    for k, (tip, w) in enumerate((((28.5, 0.6), 3.0), ((27.0, 2.4), 3.0), ((25.0, 3.8), 2.8))):  # dark primaries fan out at the tip
        wing.feather(at('wing', (12, 0.4 + 0.8*k)), at('wing', tip), w, PRIMARY, line=0.3)
    shape = [at('wing', (x, y)) for x, y in zip(np.linspace(-2.5, 22, 20), [0]*20)]
    upper = [at('wing', (x, -4.6*math.sin(math.pi*min(1, (x + 3)/26))**0.7)) for x in np.linspace(-3, 22, 22)]
    lower = [at('wing', (x, 4.2*math.sin(math.pi*min(1, (x + 3)/26))**0.9)) for x in np.linspace(22, -3, 22)]
    wing.poly(upper + lower, FEATHER, width=0.45)
    for row, (y, r) in enumerate(((-2.2, 1.5), (0.2, 1.6), (2.4, 1.7))):  # covert rows as overlapping scallops
        for x in np.arange(1.5 + row, 19 - row, 2.6):
            wing.scallop(at('wing', (x, y)), r, math.degrees(math.atan2(world['wing'][2], world['wing'][0])) + 90, FEATHER_DEEP if row == 2 else FEATHER_SHADE, width=0.26)
    part('wing', wing, ['wing'], mesh={'spacing': 16, 'alphaThreshold': 32, 'margin': 2})

    # head: rigid skull, crest, eye, long beak with pouch
    hp = [at('head', q) for q in ([-7, -7], [30, -7], [30, 8], [-7, 8])]
    head = Layer(np.min(hp, 0), np.max(hp, 0))
    lower = [at('head', (x, 1.2 + 5.6*math.sin(math.pi*(x - 2)/22.5)**0.8)) for x in np.linspace(2, 24.5, 28)]
    upper = [at('head', (x, 0.9 + 0.08*x)) for x in np.linspace(24.5, 2, 12)]

    # pouch interior sits behind the fish; only its front rim is drawn over the fish (on the head layer)
    pouch_back = Layer(np.min(hp, 0), np.max(hp, 0))
    pouch_back.poly(lower + upper, POUCH, width=0.4)
    pouch_back.poly([at('head', q) for q in ([2.6, 1.0], [24, 1.7], [22, 2.9], [14, 3.4], [6, 2.9])], (222, 150, 92, 255), outline=None)
    part('pouch', pouch_back, ['head'], mesh={'spacing': 16, 'alphaThreshold': 32, 'margin': 2})

    # fish: four-bone weighted spine inside the pouch; tail pokes out under the beak
    def fx(x, y):
        return at('fish_root', (x, y))
    FISH, FISH_DARK, BELLY, FIN = (118, 168, 204, 255), (64, 104, 148, 255), (226, 238, 244, 255), (242, 150, 72, 255)
    hw = lambda x: 0.55 + 1.3*math.sin(math.pi*min(1.0, max(0.0, (x + 0.8)/14.0)))**0.8
    xs_body = np.linspace(-0.8, 13.4, 36)
    outline_top = [fx(x, -hw(x)*0.92) for x in xs_body]
    outline_bottom = [fx(x, hw(x)*1.1) for x in xs_body[::-1]]
    fish_pts = np.array(outline_top + outline_bottom + [fx(18.8, -2.7), fx(18.8, 2.7), fx(6.5, -3.6), fx(8, 3.6)])
    fish = Layer(fish_pts.min(0) - 2, fish_pts.max(0) + 2)
    fish.poly([fx(13.0, -0.55), fx(18.8, -2.7), fx(17.3, 0), fx(18.8, 2.7), fx(13.0, 0.6)], FIN, width=0.35)     # tail fin
    for a, b in ((fx(13.4, -0.4), fx(18.2, -1.7)), (fx(13.4, 0), fx(17.0, 0)), (fx(13.4, 0.4), fx(18.2, 1.7))):
        fish.line([a, b], (200, 100, 50, 255), 0.18)
    fish.poly([fx(4.4, -1.5), fx(5.8, -3.5), fx(9.6, -1.4)], FIN, width=0.35)                                      # dorsal fin
    fish.poly([fx(6.0, 1.7), fx(7.4, 3.6), fx(9.4, 1.8)], FIN, width=0.35)                                         # pelvic fin
    fish.poly(outline_top + outline_bottom, FISH, width=0.45)                                                      # body
    belly = [fx(x, hw(x)*0.1) for x in xs_body] + [fx(x, hw(x)*1.02) for x in xs_body[::-1]]
    fish.poly(belly, BELLY, outline=None)
    fish.line([fx(x, -hw(x)*0.12) for x in np.linspace(1.2, 13, 24)], FISH_DARK, 0.28)                              # lateral line
    for row, y in enumerate((-0.6, 0.55)):                                                                         # scales cross every joint
        for x in np.arange(3.6 + 0.7*row, 12.8, 1.5):
            fish.scallop(fx(x, y*hw(x)), 0.75, 90 + 6, FISH_DARK, width=0.16)
    fish.line([fx(2.7, -1.3), fx(3.3, 0), fx(2.7, 1.5)], FISH_DARK, 0.25)                                          # gill
    fish.circle(fx(1.0, -0.35), 0.5, (255, 255, 255, 255), width=0.18)
    fish.circle(fx(1.1, -0.35), 0.28, INK, width=0)
    part('fish', fish, ['fish_root', 'fish_b1', 'fish_b2', 'fish_b3'],
         mesh={'spacing': 6, 'alphaThreshold': 32, 'margin': 3},
         # a fish is soft all the way along: wide transitions, bend shared between neighbours
         weights={'handleRadius': 2.6, 'coreInset': {'fish_root': [0.05, 0.3], 'fish_b1': [0.3, 0.3], 'fish_b2': [0.3, 0.3], 'fish_b3': [0.3, 0.02]},
                  'maxInfluences': 2, 'pruneBelow': 0.01})

    # beak rim over the fish
    rim = [at('head', (x, 1.2 + 5.6*math.sin(math.pi*(x - 2)/22.5)**0.8)) for x in np.linspace(2.6, 24.0, 30)]
    head.line(rim, INK, 1.5)
    head.line(rim, POUCH, 0.7)
    head.poly([at('head', q) for q in ([1.5, -1.9], [27, -0.3], [28.2, 0.9], [26.6, 1.2], [1.5, 1.1])], BEAK, width=0.4)
    head.poly([at('head', q) for q in ([26.2, -0.4], [28.2, 0.9], [26.6, 1.3], [25.6, 0.4])], BEAK_TIP, width=0.3)
    head.line([at('head', (3, -0.6)), at('head', (25.5, 0.2))], (204, 120, 60, 255), 0.22)
    head.poly([at('head', q) for q in ([-3.4, -3.6], [-6.2, -5.6], [-2.2, -4.4], [-4.4, -6.4], [-0.6, -4.2])], CREST, width=0.3)
    head.poly(ellipse_points(at('head', (-0.2, -0.8)), 5.4, 4.6), NECK, width=0.45)
    head.circle(at('head', (1.6, -1.8)), 1.25, (238, 196, 186, 255), width=0.2)
    head.circle(at('head', (1.75, -1.8)), 0.75, INK, width=0)
    head.circle(at('head', (2.0, -2.15)), 0.26, (255, 255, 255, 255), outline=None, width=0)
    part('head', head, ['head'], mesh={'spacing': 16, 'alphaThreshold': 32, 'margin': 2})

    rig = {'schema': 'ogs.skin-rig/1', 'units': f'world units, y down; {DENSITY} source px per unit', 'bones': rig_bones,
           'parts': parts,
           'drawOrder': ['sky', 'clouds', 'hills', 'pebble_r', 'pebble_f', 'road', 'stones', 'shadow', 'wheel_r', 'tyre_r', 'wheel_f', 'tyre_f',
                         'pedal_f', 'foot_f', 'leg_f', 'frame', 'crank', 'neck', 'body', 'wing', 'pouch', 'fish', 'head', 'pedal_n', 'foot_n', 'leg_n'],
           'provenance': 'Procedurally drawn by examples/pelican-bicycle/make_art.py; repository MIT licence.'}
    (OUT / 'rig.json').write_text(json.dumps(rig, indent=1) + '\n')

    period = 2.0
    wave = lambda values: [{'t': period*k/(len(values)-1), 'v': v, 'curve': 'smooth'} for k, v in enumerate(values)]
    dense = lambda arr: [{'t': k/FPS, 'v': float(v)} for k, v in enumerate(arr)]
    grip = {'point': list(PEDAL_GRIP)}
    dyn = ride()
    t_all = np.arange(N + 1)/FPS
    w_fish = 2*math.pi*1.5                                        # three tail beats in two seconds
    tracks = [
        {'bone': 'crank', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 360}]},
        {'bone': 'wheel_r', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 720}]},
        {'bone': 'wheel_f', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 720}]},
        {'bone': 'pelvis', 'property': 'y', 'keys': wave([0, 0.7, 0, 0.7, 0])},
        {'bone': 'body', 'property': 'rotate', 'keys': wave([0, -1.5, 0, -1.5, 0])},
        {'bone': 'neck1', 'property': 'rotate', 'keys': wave([0, 6, 0, -4, 0])},
        {'bone': 'neck2', 'property': 'rotate', 'keys': wave([0, -11, 0, 9, 0])},
        {'bone': 'head', 'property': 'rotate', 'keys': wave([0, 6, 0, -5, 0])},
        {'bone': 'wing', 'property': 'rotate', 'keys': wave([0, -3, 0, -3, 0])},
        {'bone': 'foot_n', 'property': 'rotate', 'keys': wave([0, -14, 0, 10, 0])},
        {'bone': 'foot_f', 'property': 'rotate', 'keys': wave([0, 10, 0, -14, 0])},
        # bumps: the bike hops and pitches, the pelican springs on top of it
        {'bone': 'bike', 'property': 'y', 'keys': dense(dyn['dy'])},
        {'bone': 'bike', 'property': 'rotate', 'keys': dense(dyn['pitch'])},
        {'bone': 'pelvis', 'property': 'y', 'keys': dense(dyn['body'])},
        {'bone': 'neck1', 'property': 'rotate', 'keys': dense(-6*dyn['lag'])},
        {'bone': 'head', 'property': 'rotate', 'keys': dense(5*dyn['lag'])},
        # fish: travelling tail wave plus a flop and jump driven by the bumps
        {'bone': 'fish_root', 'property': 'rotate', 'keys': dense(4*np.sin(w_fish*t_all) + 6*dyn['lag'] - 3)},
        {'bone': 'fish_b1', 'property': 'rotate', 'keys': dense(8*np.sin(w_fish*t_all - 0.9) + 3*dyn['lag'])},
        {'bone': 'fish_b2', 'property': 'rotate', 'keys': dense(12*np.sin(w_fish*t_all - 1.8) + 3*dyn['lag'])},
        {'bone': 'fish_b3', 'property': 'rotate', 'keys': dense(17*np.sin(w_fish*t_all - 2.7) + 3*dyn['lag'])},
        {'bone': 'fish_root', 'property': 'y', 'keys': dense(-0.6*(1 - np.cos(w_fish*t_all))/2 + 1.5*dyn['fish_hop'])},
        # scrolling world: road and stones reset every second (one tyre revolution), clouds and hills drift slowly
        {'bone': 'road', 'property': 'x', 'keys': dense([-V*((k/FPS) % 1.0) for k in range(N + 1)])},
        {'bone': 'hills', 'property': 'x', 'keys': dense([-92.0*(k/FPS)/period if k < N else 0.0 for k in range(N + 1)])},
        {'bone': 'clouds', 'property': 'x', 'keys': dense([-96.0*(k/FPS)/period if k < N else 0.0 for k in range(N + 1)])},
    ]
    for wheel in ('r', 'f'):
        for j in range(8):
            tracks.append({'bone': f'tyre_{wheel}_{j}', 'property': 'x', 'keys': dense(dyn['tyre'][wheel][:, j, 0])})
            tracks.append({'bone': f'tyre_{wheel}_{j}', 'property': 'y', 'keys': dense(dyn['tyre'][wheel][:, j, 1])})
        tracks.append({'bone': f'pebble_{wheel}', 'property': 'x', 'keys': dense(dyn['pebbles'][wheel][:, 0])})
        tracks.append({'bone': f'pebble_{wheel}', 'property': 'y', 'keys': dense(dyn['pebbles'][wheel][:, 1])})
        tracks.append({'bone': f'pebble_{wheel}', 'property': 'rotate', 'keys': dense(720*t_all*(np.abs(dyn['pebbles'][wheel][:, 1]) > 0))})
    motion = {
        'schema': 'ogs.skin-motion/1', 'sampleRate': FPS, 'duration': period, 'loop': True,
        'scope': 'technical pedalling cycle over stones; not gameplay timing',
        'tracks': tracks,
        'ik': [
            {'name': 'leg_n', 'bones': ['thigh_n', 'shin_n'], 'target': {'bone': 'pedal_n', **grip}, 'bend': 1},
            {'name': 'leg_f', 'bones': ['thigh_f', 'shin_f'], 'target': {'bone': 'pedal_f', **grip}, 'bend': 1},
        ],
        'contacts': [
            {'name': 'near ankle on pedal', 'effector': {'bone': 'shin_n'}, 'target': {'bone': 'pedal_n', **grip}, 'first': 0, 'last': 120, 'tolerance': 1e-4},
            {'name': 'far ankle on pedal', 'effector': {'bone': 'shin_f'}, 'target': {'bone': 'pedal_f', **grip}, 'first': 0, 'last': 120, 'tolerance': 1e-4},
        ],
    }
    (OUT / 'motion.json').write_text(json.dumps(motion, separators=(',', ':')) + '\n')
    print(f'wrote {len(parts)} layers to {OUT}')


if __name__ == '__main__':
    main()
