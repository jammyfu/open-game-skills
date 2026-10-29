"""Shared geometry for the skin-weights skill (numpy + Pillow only).

Conventions: world space is y-down (image-like). A bone matrix is [a,b,c,d,x,y]
mapping a local point (u,v) to (a*u+b*v+x, c*u+d*v+y), the same layout the
spine-skeletal trace audit reads. Rotation is degrees, positive turns +x toward +y.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

RIG_SCHEMA = 'ogs.skin-rig/1'
MESH_SCHEMA = 'ogs.skin-mesh/1'
WEIGHTS_SCHEMA = 'ogs.skin-weights/1'
MOTION_SCHEMA = 'ogs.skin-motion/1'


class SkinError(ValueError):
    """Invalid or insufficient evidence; callers map this to exit code 2."""


def require(condition, message):
    if not condition:
        raise SkinError(message)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def vec(value, size, name):
    require(isinstance(value, list) and len(value) == size and all(finite(v) for v in value), f'{name}: expected {size} finite numbers')
    return [float(v) for v in value]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise SkinError(f'{path}: {error}') from error


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1, allow_nan=False) + '\n', encoding='utf-8')


# ---------------------------------------------------------------- rig + FK

def load_rig(path):
    path = Path(path).resolve()
    rig = read_json(path)
    require(isinstance(rig, dict) and rig.get('schema') == RIG_SCHEMA, f'{path}: expected schema {RIG_SCHEMA}')
    bones = rig.get('bones')
    require(isinstance(bones, list) and bones, 'rig.bones must be a nonempty list')
    seen = {}
    for bone in bones:
        require(isinstance(bone, dict) and isinstance(bone.get('name'), str) and bone['name'], 'every bone needs a name')
        require(bone['name'] not in seen, f'duplicate bone {bone["name"]}')
        parent = bone.get('parent')
        require(parent is None or parent in seen, f'bone {bone["name"]}: parent must be declared earlier')
        for key in ('x', 'y', 'rotation', 'length'):
            require(finite(bone.get(key, 0)), f'bone {bone["name"]}: invalid {key}')
        require(bone.get('length', 0) >= 0, f'bone {bone["name"]}: negative length')
        require(isinstance(bone.get('inheritRotation', True), bool), f'bone {bone["name"]}: inheritRotation must be boolean')
        seen[bone['name']] = bone
    parts = rig.get('parts')
    require(isinstance(parts, list) and parts, 'rig.parts must be a nonempty list')
    names = set()
    for part in parts:
        name = part.get('name')
        require(isinstance(name, str) and name and name not in names, 'parts need unique names')
        names.add(name)
        influences = part.get('bones')
        require(isinstance(influences, list) and influences and len(set(influences)) == len(influences), f'part {name}: bones must be a nonempty unique list')
        require(all(b in seen for b in influences), f'part {name}: unknown influence bone')
        require(isinstance(part.get('image'), str), f'part {name}: missing image')
        vec(part.get('origin'), 2, f'part {name} origin')
        vec(part.get('at'), 2, f'part {name} at')
        require(finite(part.get('density')) and part['density'] > 0, f'part {name}: density must be positive pixels per world unit')
        require((path.parent / part['image']).is_file(), f'part {name}: image not found {part["image"]}')
    order = rig.get('drawOrder', [p['name'] for p in parts])
    require(sorted(order) == sorted(names), 'drawOrder must list every part exactly once')
    rig['drawOrder'] = order
    rig['_path'] = path
    rig['_bones'] = seen
    return rig


def local_matrix(x, y, degrees):
    r = math.radians(degrees)
    c, s = math.cos(r), math.sin(r)
    return np.array([c, -s, s, c, x, y], dtype=float)


def compose(parent, child):
    a, b, c, d, x, y = parent
    ca, cb, cc, cd, cx, cy = child
    return np.array([a*ca + b*cc, a*cb + b*cd, c*ca + d*cc, c*cb + d*cd, a*cx + b*cy + x, c*cx + d*cy + y])


def rotation_of(matrix):
    return math.degrees(math.atan2(matrix[2], matrix[0]))


def forward(rig, offsets=None):
    """World matrices for every bone. offsets: {bone: {'rotate','x','y'}} additive to setup."""
    offsets = offsets or {}
    world = {}
    for bone in rig['bones']:
        extra = offsets.get(bone['name'], {})
        local = local_matrix(bone.get('x', 0) + extra.get('x', 0), bone.get('y', 0) + extra.get('y', 0),
                             bone.get('rotation', 0) + extra.get('rotate', 0))
        parent = bone.get('parent')
        if parent is None:
            world[bone['name']] = local
            continue
        matrix = compose(world[parent], local)
        if not bone.get('inheritRotation', True):
            matrix[:4] = local_matrix(0, 0, bone.get('rotation', 0) + extra.get('rotate', 0))[:4]
        world[bone['name']] = matrix
    return world


def apply(matrix, points):
    a, b, c, d, x, y = matrix
    points = np.asarray(points, dtype=float)
    return np.stack([a*points[..., 0] + b*points[..., 1] + x, c*points[..., 0] + d*points[..., 1] + y], axis=-1)


def invert(matrix):
    a, b, c, d, x, y = matrix
    det = a*d - b*c
    require(abs(det) > 1e-12, 'singular bone matrix')
    ia, ib, ic, id_ = d/det, -b/det, -c/det, a/det
    return np.array([ia, ib, ic, id_, -(ia*x + ib*y), -(ic*x + id_*y)])


def segment(rig, world, name):
    start = world[name][4:6].copy()
    length = rig['_bones'][name].get('length', 0)
    end = apply(world[name], [length, 0.0]) if length else start.copy()
    return start, np.asarray(end, dtype=float)


def point_segment_distance(points, start, end):
    points = np.asarray(points, dtype=float)
    direction = end - start
    span = float(direction @ direction)
    if span == 0:
        return np.linalg.norm(points - start, axis=1)
    t = np.clip(((points - start) @ direction) / span, 0, 1)
    return np.linalg.norm(points - (start + t[:, None]*direction), axis=1)


# ---------------------------------------------------------------- meshes

def part_alpha(rig, part):
    with Image.open(rig['_path'].parent / part['image']) as image:
        return np.array(image.convert('RGBA').getchannel('A'))


def pixel_to_world(part, pixels):
    origin = np.array(part['origin'], dtype=float)
    at = np.array(part['at'], dtype=float)
    return at + (np.asarray(pixels, dtype=float) - origin) / part['density']


def build_grid_mesh(alpha, spacing, threshold=32, margin=2):
    """Grid mesh covering every visible pixel (dilated by margin) of one layer.

    Cells are kept when any dilated visible pixel lies inside them, so the mesh
    hull always contains the visible ink. Diagonals alternate to avoid a global
    shear bias. Returns (pixel vertices, triangles, cells kept)."""
    require(spacing >= 2, 'mesh spacing must be at least 2 pixels')
    require(0 <= threshold < 255 and margin >= 0, 'invalid alpha threshold/margin')
    height, width = alpha.shape
    mask = alpha > threshold
    require(mask.any(), 'layer has no visible pixels above the alpha threshold')
    if margin:
        size = 2*int(margin) + 1
        mask = np.array(Image.fromarray(mask.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(size))) > 0
    nx, ny = math.ceil(width / spacing), math.ceil(height / spacing)
    xs = np.linspace(0, width, nx + 1)
    ys = np.linspace(0, height, ny + 1)
    integral = np.zeros((height + 1, width + 1), dtype=np.int64)
    integral[1:, 1:] = mask.cumsum(0).cumsum(1)
    xi = np.round(xs).astype(int)
    yi = np.round(ys).astype(int)
    active = np.zeros((ny, nx), dtype=bool)
    for j in range(ny):
        for i in range(nx):
            y0, y1, x0, x1 = yi[j], yi[j + 1], xi[i], xi[i + 1]
            active[j, i] = integral[y1, x1] - integral[y0, x1] - integral[y1, x0] + integral[y0, x0] > 0
    active = manifold_cells(active)
    index = -np.ones((ny + 1, nx + 1), dtype=int)
    vertices, triangles = [], []

    def vid(j, i):
        if index[j, i] < 0:
            index[j, i] = len(vertices)
            vertices.append((xs[i], ys[j]))
        return int(index[j, i])

    for j in range(ny):
        for i in range(nx):
            if not active[j, i]:
                continue
            a, b, c, d = vid(j, i), vid(j, i + 1), vid(j + 1, i + 1), vid(j + 1, i)
            if (i + j) % 2:
                triangles += [[a, b, c], [a, c, d]]
            else:
                triangles += [[a, b, d], [b, c, d]]
    return np.array(vertices, dtype=float), np.array(triangles, dtype=int), int(active.sum())


def manifold_cells(active):
    """Fill enclosed holes and bridge diagonal-only contacts so each island has one outline."""
    active = active.copy()
    while True:
        padded = np.pad(active, 1)
        outside = np.zeros_like(padded)
        stack = [(0, 0)]
        outside[0, 0] = True
        while stack:
            j, i = stack.pop()
            for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                y, x = j + dj, i + di
                if 0 <= y < padded.shape[0] and 0 <= x < padded.shape[1] and not padded[y, x] and not outside[y, x]:
                    outside[y, x] = True
                    stack.append((y, x))
        active |= ~outside[1:-1, 1:-1]
        a, b, c, d = active[:-1, :-1], active[:-1, 1:], active[1:, :-1], active[1:, 1:]
        cross = (a & d & ~b & ~c) | (b & c & ~a & ~d)
        if not cross.any():
            return active
        j, i = np.argwhere(cross)[0]
        if active[j, i]:
            active[j, i + 1] = True
        else:
            active[j, i] = True


def boundary_loops(triangles):
    """Ordered boundary loops from edges used by exactly one triangle (manifold mesh)."""
    count = {}
    for tri in triangles:
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            key = (min(a, b), max(a, b))
            count[key] = count.get(key, 0) + 1
    directed = {}
    for tri in triangles:
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            if count[(min(a, b), max(a, b))] == 1:
                require(int(a) not in directed, 'non-manifold boundary vertex')
                directed[int(a)] = int(b)
    loops, seen = [], set()
    for start in sorted(directed):
        if start in seen:
            continue
        loop, v = [], start
        while v not in seen:
            seen.add(v)
            loop.append(v)
            v = directed[v]
        require(v == start, 'open boundary chain')
        loops.append(loop)
    return loops


def hull_first(vertices, triangles):
    """Reorder so the single outline comes first in outline order (Spine/rig-c mesh rule)."""
    loops = boundary_loops(triangles)
    if len(loops) != 1:
        return vertices, triangles, None, len(loops)
    hull = loops[0]
    rest = [i for i in range(len(vertices)) if i not in set(hull)]
    order = np.array(hull + rest)
    remap = np.empty(len(vertices), dtype=int)
    remap[order] = np.arange(len(vertices))
    return vertices[order], remap[triangles], len(hull), 1


def components(count, triangles):
    parent = list(range(count))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b, c in triangles:
        for u, v in ((a, b), (b, c)):
            ru, rv = find(int(u)), find(int(v))
            if ru != rv:
                parent[ru] = rv
    labels = np.array([find(i) for i in range(count)])
    _, labels = np.unique(labels, return_inverse=True)
    return labels


def edges_of(triangles):
    pairs = np.concatenate([triangles[:, [0, 1]], triangles[:, [1, 2]], triangles[:, [2, 0]]])
    pairs.sort(axis=1)
    return np.unique(pairs, axis=0)


def signed_areas(vertices, triangles):
    a, b, c = (vertices[triangles[:, i]] for i in range(3))
    return (b[:, 0]-a[:, 0])*(c[:, 1]-a[:, 1]) - (b[:, 1]-a[:, 1])*(c[:, 0]-a[:, 0])


def load_mesh(path):
    mesh = read_json(path)
    require(isinstance(mesh, dict) and mesh.get('schema') == MESH_SCHEMA, f'{path}: expected schema {MESH_SCHEMA}')
    parts = {}
    for name, item in mesh['parts'].items():
        vertices = np.array(item['vertices'], dtype=float).reshape(-1, 2)
        triangles = np.array(item['triangles'], dtype=int).reshape(-1, 3)
        uvs = np.array(item['uvs'], dtype=float).reshape(-1, 2)
        require(len(vertices) == len(uvs) and len(vertices) >= 3, f'mesh {name}: vertex/uv mismatch')
        require(triangles.size and triangles.min() >= 0 and triangles.max() < len(vertices), f'mesh {name}: bad triangle index')
        parts[name] = dict(item, vertices=vertices, triangles=triangles, uvs=uvs)
    mesh['parts'] = parts
    return mesh


# ---------------------------------------------------------------- harmonic weights

def cotangent_edge_weights(vertices, triangles, floor_ratio=1e-3):
    """Cotangent Laplacian edge weights, clamped to a small positive floor.

    Clamping negative cotangent weights keeps the system an M-matrix, so the
    discrete maximum principle holds: every harmonic weight stays in [0,1] and
    the per-bone solutions sum to one before pruning."""
    weights = {}
    for tri in triangles:
        p = vertices[tri]
        for k in range(3):
            i, j, o = tri[(k+1) % 3], tri[(k+2) % 3], tri[k]
            u, v = vertices[i] - vertices[o], vertices[j] - vertices[o]
            cross = abs(u[0]*v[1] - u[1]*v[0])
            cot = float(u @ v) / cross if cross > 1e-15 else 0.0
            key = (min(i, j), max(i, j))
            weights[key] = weights.get(key, 0.0) + 0.5*cot
    edges = np.array(list(weights), dtype=int)
    values = np.array(list(weights.values()), dtype=float)
    positive = values[values > 0]
    floor = floor_ratio * (np.median(positive) if positive.size else 1.0)
    return edges, np.maximum(values, floor), int((values < floor).sum())


def harmonic_solve(count, edges, edge_weights, fixed, fixed_values, tolerance=1e-11, iterations=20000):
    """Solve L x = 0 on free vertices with Dirichlet values (Jacobi-preconditioned CG)."""
    free = np.ones(count, dtype=bool)
    free[fixed] = False
    x = np.zeros((count, fixed_values.shape[1]))
    x[fixed] = fixed_values
    i, j = edges[:, 0], edges[:, 1]
    diagonal = np.zeros(count)
    np.add.at(diagonal, i, edge_weights)
    np.add.at(diagonal, j, edge_weights)

    def laplacian(v):
        out = diagonal[:, None]*v
        np.add.at(out, i, -edge_weights[:, None]*v[j])
        np.add.at(out, j, -edge_weights[:, None]*v[i])
        return out

    rhs = -laplacian(np.where(free[:, None], 0.0, x))
    rhs[~free] = 0
    solution = np.zeros_like(x)
    residual = rhs.copy()
    inverse = np.where(free, 1.0/np.maximum(diagonal, 1e-300), 0.0)[:, None]
    z = inverse*residual
    direction = z.copy()
    rz = (residual*z).sum(0)
    norm = np.sqrt((rhs**2).sum(0)) + 1e-300
    steps = 0
    for steps in range(1, iterations + 1):
        q = laplacian(direction)
        q[~free] = 0
        alpha = rz / np.maximum((direction*q).sum(0), 1e-300)
        solution += alpha*direction
        residual -= alpha*q
        if np.all(np.sqrt((residual**2).sum(0)) <= tolerance*norm):
            break
        z = inverse*residual
        new = (residual*z).sum(0)
        direction = z + (new/np.maximum(rz, 1e-300))*direction
        rz = new
    else:
        raise SkinError('harmonic solve did not converge')
    x[free] = solution[free]
    return x, steps
