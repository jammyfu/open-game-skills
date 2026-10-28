"""Generate the layered pelican-on-a-bicycle test character (repository-authored, MIT).

Writes source/rig.json, source/motion.json and one RGBA PNG per layer. The setup
pose is solved first (legs reach the pedals at crank angle 0); every layer is then
painted along its actual setup bones, with hidden overlap at the knee, ankle and
neck joints, so the drawing and the skeleton agree by construction.
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

DENSITY = 4          # source pixels per world unit
OUT = HERE / 'source'
INK = (38, 34, 44, 255)
CRANK = 8.0
HIP = (2.0, 4.0)     # near hip, local to pelvis


def two_bone(start, target, l1, l2, bend=1):
    dx, dy = target[0]-start[0], target[1]-start[1]
    d = math.hypot(dx, dy)
    inner = math.acos((l1*l1 + d*d - l2*l2)/(2*l1*d))
    knee = math.acos((l1*l1 + l2*l2 - d*d)/(2*l1*l2))
    return math.degrees(math.atan2(dy, dx) - bend*inner), math.degrees(bend*(math.pi - knee))


def bones():
    pelvis = (-8.0, 4.0)
    hip_world = (pelvis[0]+HIP[0], pelvis[1]+HIP[1])
    near_upper, near_lower = two_bone(hip_world, (CRANK, 38.0), 20, 20)
    far_upper, far_lower = two_bone(hip_world, (-CRANK, 38.0), 20, 20)
    return [
        {'name': 'root'},
        {'name': 'bike', 'parent': 'root'},
        {'name': 'wheel_r', 'parent': 'bike', 'x': -36, 'y': 40, 'length': 0},
        {'name': 'wheel_f', 'parent': 'bike', 'x': 38, 'y': 40, 'length': 0},
        {'name': 'crank', 'parent': 'bike', 'x': 0, 'y': 38, 'length': CRANK},
        {'name': 'pedal_n', 'parent': 'crank', 'x': CRANK, 'y': 0, 'inheritRotation': False},
        {'name': 'pedal_f', 'parent': 'crank', 'x': -CRANK, 'y': 0, 'inheritRotation': False},
        {'name': 'pelvis', 'parent': 'root', 'x': pelvis[0], 'y': pelvis[1], 'length': 0},
        {'name': 'body', 'parent': 'pelvis', 'x': 0, 'y': -2, 'rotation': -20, 'length': 18},
        {'name': 'neck1', 'parent': 'body', 'x': 18, 'y': -3, 'rotation': -62, 'length': 12},
        {'name': 'neck2', 'parent': 'neck1', 'x': 12, 'y': 0, 'rotation': 38, 'length': 11},
        {'name': 'head', 'parent': 'neck2', 'x': 11, 'y': 0, 'rotation': 52, 'length': 7},
        {'name': 'wing', 'parent': 'body', 'x': 4, 'y': -2, 'rotation': 35, 'length': 20},
        {'name': 'thigh_n', 'parent': 'pelvis', 'x': HIP[0], 'y': HIP[1], 'rotation': near_upper, 'length': 20},
        {'name': 'shin_n', 'parent': 'thigh_n', 'x': 20, 'y': 0, 'rotation': near_lower, 'length': 20},
        {'name': 'foot_n', 'parent': 'shin_n', 'x': 20, 'y': 0, 'inheritRotation': False, 'length': 6},
        {'name': 'thigh_f', 'parent': 'pelvis', 'x': HIP[0], 'y': HIP[1], 'rotation': far_upper, 'length': 20},
        {'name': 'shin_f', 'parent': 'thigh_f', 'x': 20, 'y': 0, 'rotation': far_lower, 'length': 20},
        {'name': 'foot_f', 'parent': 'shin_f', 'x': 20, 'y': 0, 'inheritRotation': False, 'length': 6},
    ]


class Layer:
    def __init__(self, lo, hi):
        self.lo = np.array(lo, float)
        size = np.ceil((np.array(hi, float) - self.lo)*DENSITY).astype(int)
        self.image = Image.new('RGBA', tuple(size), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def p(self, point):
        return tuple(((np.array(point, float) - self.lo)*DENSITY).tolist())

    def capsule(self, a, b, width, fill, outline=INK, line=1.2):
        for colour, w in ((outline, width + 2*line), (fill, width)):
            self.draw.line([self.p(a), self.p(b)], fill=colour, width=int(w*DENSITY))
            for c in (a, b):
                x, y = self.p(c)
                r = w*DENSITY/2
                self.draw.ellipse([x-r, y-r, x+r, y+r], fill=colour)

    def poly(self, points, fill, outline=INK, width=1.0):
        self.draw.polygon([self.p(q) for q in points], fill=fill, outline=outline, width=int(width*DENSITY))

    def ellipse(self, centre, rx, ry, fill, outline=INK, width=1.0):
        x, y = self.p(centre)
        self.draw.ellipse([x-rx*DENSITY, y-ry*DENSITY, x+rx*DENSITY, y+ry*DENSITY], fill=fill, outline=outline, width=int(width*DENSITY))

    def save(self, name):
        path = OUT / f'{name}.png'
        self.image.save(path)
        return {'image': path.name, 'origin': [0, 0], 'at': self.lo.round(6).tolist(), 'density': DENSITY}


def tip(world, rig_bones, name, along=None):
    length = rig_bones[name].get('length', 0) if along is None else along
    return apply(world[name], [length, 0])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rig_bones = bones()
    lookup = {b['name']: b for b in rig_bones}
    world = forward({'bones': rig_bones, '_bones': lookup})
    origin = {n: world[n][4:6] for n in lookup}
    parts = []

    def part(name, layer, influences, **extra):
        parts.append(dict(name=name, bones=influences, **layer.save(name), **extra))

    # legs: one continuous painted limb per side (thigh, shin, foot share a mesh)
    for side, fill, shade in (('f', (226, 140, 60, 255), (190, 110, 45, 255)), ('n', (247, 166, 74, 255), (214, 130, 52, 255))):
        hip, knee, ankle = origin[f'thigh_{side}'], origin[f'shin_{side}'], origin[f'foot_{side}']
        toe = tip(world, lookup, f'foot_{side}')
        pts = np.array([hip, knee, ankle, toe])
        layer = Layer(pts.min(0) - 6, pts.max(0) + 6)
        layer.capsule(hip, knee, 5.2, fill)
        layer.capsule(knee, ankle, 3.4, fill)
        layer.capsule(knee, ankle, 1.2, shade, outline=shade, line=0)  # shin stripe: visible ink across the knee
        for k in range(1, 6):
            q = np.array(hip) + (np.array(knee)-np.array(hip))*k/6
            layer.ellipse(q, 1.0, 1.0, shade, outline=shade)
        layer.poly([ankle + np.array([-1.5, -1.2]), toe + np.array([1, -1.5]), toe + np.array([1.5, 1.6]), ankle + np.array([-1.5, 1.6])], fill)
        part(f'leg_{side}', layer, [f'thigh_{side}', f'shin_{side}', f'foot_{side}'],
             mesh={'spacing': 6, 'alphaThreshold': 32, 'margin': 2},
             weights={'handleRadius': {f'thigh_{side}': 4.2, f'shin_{side}': 2.4, f'foot_{side}': 1.6},
                      'coreInset': {f'thigh_{side}': 0.3, f'shin_{side}': 0.3, f'foot_{side}': 0.35}, 'maxInfluences': 3, 'pruneBelow': 0.01},
             lint={'maxReach': 14.0})

    for wheel in ('wheel_r', 'wheel_f'):
        c = origin[wheel]
        layer = Layer(c - 19, c + 19)
        layer.ellipse(c, 18, 18, (0, 0, 0, 0), width=2.2)
        layer.ellipse(c, 15.4, 15.4, (0, 0, 0, 0), outline=(120, 120, 130, 255), width=0.6)
        for k in range(12):
            a = math.pi*k/6
            layer.draw.line([layer.p(c), layer.p(c + 15.5*np.array([math.cos(a), math.sin(a)]))], fill=(110, 110, 120, 255), width=2)
        layer.ellipse(c, 2, 2, (180, 180, 190, 255))
        part(wheel, layer, [wheel], mesh={'spacing': 12, 'alphaThreshold': 32, 'margin': 2})

    frame = Layer((-40, -2), (44, 44))
    rear, front, bb = origin['wheel_r'], origin['wheel_f'], origin['crank']
    seat, bar = np.array([-10.0, 9.0]), np.array([30.0, 4.0])
    red = (208, 54, 64, 255)
    for a, b in ((rear, bb), (bb, seat), (seat, rear), (seat, bar + [-4, 8]), (bb, bar + [-4, 8]), (bar + [-4, 8], front)):
        frame.capsule(a, b, 2.2, red, line=0.6)
    frame.poly([seat + [-7, -2], seat + [5, -2.5], seat + [4, 0.8], seat + [-6, 0.8]], (40, 40, 48, 255))
    frame.capsule(bar + [-4, 8], bar, 1.6, (90, 90, 100, 255), line=0.4)
    frame.capsule(bar, bar + [6, -1], 1.6, (40, 40, 48, 255), line=0.4)
    part('frame', frame, ['bike'], mesh={'spacing': 12, 'alphaThreshold': 32, 'margin': 2})

    crank = Layer(bb - 10, bb + 10)
    crank.ellipse(bb, 4, 4, (170, 170, 180, 255))
    crank.capsule(bb - [CRANK, 0], bb + [CRANK, 0], 1.6, (130, 130, 140, 255), line=0.4)
    part('crank', crank, ['crank'], mesh={'spacing': 8, 'alphaThreshold': 32, 'margin': 2})
    for side in ('n', 'f'):
        c = origin[f'pedal_{side}']
        pedal = Layer(c - 4, c + 4)
        pedal.poly([c + [-3.2, -0.9], c + [3.2, -0.9], c + [3.2, 0.9], c + [-3.2, 0.9]], (60, 60, 66, 255), width=0.4)
        part(f'pedal_{side}', pedal, [f'pedal_{side}'], mesh={'spacing': 8, 'alphaThreshold': 32, 'margin': 2})

    body_o, body_t = origin['body'], tip(world, lookup, 'body')
    body = Layer(np.minimum(body_o, body_t) - 14, np.maximum(body_o, body_t) + 14)
    centre = (np.array(body_o) + np.array(body_t))/2
    angle = math.radians(-20)
    pts = [centre + np.array([math.cos(t)*16*math.cos(angle) - math.sin(t)*10*math.sin(angle),
                              math.cos(t)*16*math.sin(angle) + math.sin(t)*10*math.cos(angle)]) for t in np.linspace(0, 2*math.pi, 64)]
    body.poly(pts, (246, 246, 240, 255), width=1.2)
    body.poly([centre + [-15, 3], centre + [-24, 9], centre + [-13, 8]], (230, 230, 222, 255), width=0.8)  # tail
    part('body', body, ['body'], mesh={'spacing': 10, 'alphaThreshold': 32, 'margin': 2})

    n0, n1, n2, n3 = origin['neck1'], origin['neck2'], origin['head'], tip(world, lookup, 'head')
    beak_tip = apply(world['head'], [24, 0])
    pouch = apply(world['head'], [16, 4.8])
    pts = np.array([n0, n1, n2, n3, beak_tip, pouch])
    neck = Layer(pts.min(0) - 8, pts.max(0) + 8)
    white = (248, 248, 242, 255)
    neck.capsule(n0, n1, 5.0, white)
    neck.capsule(n1, n2, 4.2, white)
    upper_beak = [apply(world['head'], q) for q in ([2, -2.2], [24, -0.6], [24, 0.6], [2, 0.8])]
    lower_pouch = [apply(world['head'], q) for q in ([2, 0.6], [22, 0.9], [14, 5.2], [5, 4.0])]
    neck.poly(lower_pouch, (244, 196, 92, 255), width=0.7)
    neck.poly(upper_beak, (240, 170, 60, 255), width=0.7)
    neck.ellipse(n2, 4.6, 4.2, white, width=1.0)
    eye = apply(world['head'], [1.2, -1.6])
    neck.ellipse(eye, 0.9, 0.9, (20, 20, 24, 255), outline=(20, 20, 24, 255))
    for k in range(1, 4):  # neck feather marks: visible ink across both neck joints
        neck.ellipse(np.array(n0) + (np.array(n1)-np.array(n0))*k/4, 0.8, 0.8, (200, 200, 196, 255), outline=(200, 200, 196, 255))
        neck.ellipse(np.array(n1) + (np.array(n2)-np.array(n1))*k/4, 0.7, 0.7, (200, 200, 196, 255), outline=(200, 200, 196, 255))
    part('neck', neck, ['neck1', 'neck2', 'head'], mesh={'spacing': 6, 'alphaThreshold': 32, 'margin': 2},
         weights={'handleRadius': {'neck1': 4.5, 'neck2': 3.0, 'head': 4.5}, 'coreInset': {'neck1': 0.2, 'neck2': 0.2, 'head': 0.3}, 'maxInfluences': 3, 'pruneBelow': 0.01},
         lint={'maxReach': 22.0})

    w0, w1 = origin['wing'], tip(world, lookup, 'wing')
    wing = Layer(np.minimum(w0, w1) - 8, np.maximum(w0, w1) + 8)
    side = apply(world['wing'], [0, 1])
    normal = np.array(side) - np.array(w0)
    wing.poly([w0 - normal*5, w0 + (np.array(w1)-w0)*0.6 - normal*4, w1, w0 + normal*4], (226, 226, 218, 255), width=1.0)
    for k in range(3):
        a = w0 + (np.array(w1)-w0)*(0.45 + 0.17*k)
        wing.draw.line([wing.p(a - normal*3), wing.p(a + normal*2)], fill=(150, 150, 150, 255), width=3)
    part('wing', wing, ['wing'], mesh={'spacing': 8, 'alphaThreshold': 32, 'margin': 2})

    rig = {'schema': 'ogs.skin-rig/1', 'units': 'world units, y down; 4 source px per unit', 'bones': rig_bones,
           'parts': parts,
           'drawOrder': ['leg_f', 'pedal_f', 'wheel_r', 'wheel_f', 'frame', 'crank', 'body', 'neck', 'wing', 'leg_n', 'pedal_n'],
           'provenance': 'Procedurally drawn by examples/pelican-bicycle/make_art.py; repository MIT licence.'}
    (OUT / 'rig.json').write_text(json.dumps(rig, indent=1) + '\n')

    period = 2.0
    keys = lambda values: [{'t': period*k/(len(values)-1), 'v': v, 'curve': 'smooth'} for k, v in enumerate(values)]
    motion = {
        'schema': 'ogs.skin-motion/1', 'sampleRate': 60, 'duration': period, 'loop': True,
        'scope': 'technical pedalling cycle; not gameplay timing',
        'tracks': [
            {'bone': 'crank', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 360}]},
            {'bone': 'wheel_r', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 720}]},
            {'bone': 'wheel_f', 'property': 'rotate', 'keys': [{'t': 0, 'v': 0}, {'t': period, 'v': 720}]},
            {'bone': 'pelvis', 'property': 'y', 'keys': keys([0, 0.6, 0, 0.6, 0])},
            {'bone': 'neck1', 'property': 'rotate', 'keys': keys([0, 7, 0, -5, 0])},
            {'bone': 'neck2', 'property': 'rotate', 'keys': keys([0, -12, 0, 10, 0])},
            {'bone': 'head', 'property': 'rotate', 'keys': keys([0, 8, 0, -6, 0])},
            {'bone': 'wing', 'property': 'rotate', 'keys': keys([0, -4, 0, -4, 0])},
            {'bone': 'foot_n', 'property': 'rotate', 'keys': keys([0, -12, 0, 10, 0])},
            {'bone': 'foot_f', 'property': 'rotate', 'keys': keys([0, 10, 0, -12, 0])},
        ],
        'ik': [
            {'name': 'leg_n', 'bones': ['thigh_n', 'shin_n'], 'target': {'bone': 'pedal_n'}, 'bend': 1},
            {'name': 'leg_f', 'bones': ['thigh_f', 'shin_f'], 'target': {'bone': 'pedal_f'}, 'bend': 1},
        ],
        'contacts': [
            {'name': 'near ankle on pedal', 'effector': {'bone': 'shin_n'}, 'target': {'bone': 'pedal_n'}, 'first': 0, 'last': 120, 'tolerance': 1e-4},
            {'name': 'far ankle on pedal', 'effector': {'bone': 'shin_f'}, 'target': {'bone': 'pedal_f'}, 'first': 0, 'last': 120, 'tolerance': 1e-4},
        ],
    }
    (OUT / 'motion.json').write_text(json.dumps(motion, indent=1) + '\n')
    print(f'wrote {len(parts)} layers to {OUT}')


if __name__ == '__main__':
    main()
