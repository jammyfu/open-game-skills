"""Solve bounded harmonic skin weights per part, then prune. Writes ogs.skin-weights/1.

Handles: vertices within `handleRadius` of each influence bone's *core* (the bone
segment shortened by `coreInset` of its length at both ends) are pinned rigid to
that bone. Everything between handles is the harmonic interpolation over the
mesh's own connectivity, so weights never jump across transparent gaps and the
transition width equals the joint gap you declared. `--method nearest` writes the
naive rigid nearest-bone binding; it exists only as a negative control.
Exit 0 solved, 2 invalid/unsolvable input. Never edits the rig or art.
"""
import argparse
import json
import sys

import numpy as np

from skinlib import (WEIGHTS_SCHEMA, SkinError, components, cotangent_edge_weights, forward, harmonic_solve, invert,
                     apply, load_mesh, load_rig, point_segment_distance, require, segment, sha256, write_json)

DEFAULTS = {'handleRadius': None, 'coreInset': 0.2, 'maxInfluences': 4, 'pruneBelow': 0.01}


def handle_distance(points, start, end, inset, radius=None):
    """Distance to a bone *slab*: the core [inset, 1-inset] of the segment, no end caps.

    Without end caps a joint keeps a free gap of 2*inset*length along the chain,
    which is where the harmonic transition happens. Zero-length bones use a disc."""
    direction = end - start
    span = float(direction @ direction)
    if span == 0:
        return np.linalg.norm(points - start, axis=1)
    t = ((points - start) @ direction) / span
    perpendicular = np.abs((points - start) @ np.array([-direction[1], direction[0]])) / np.sqrt(span)
    return np.where((t >= inset) & (t <= 1 - inset), perpendicular, np.inf)


def handles_for(rig, world, part, vertices, options):
    radius = options['handleRadius']
    radii = radius if isinstance(radius, dict) else {name: radius for name in part['bones']}
    require(set(radii) == set(part['bones']) and all(isinstance(r, (int, float)) and r > 0 for r in radii.values()),
            f'part {part["name"]}: weights.handleRadius must be a positive number or {{bone: radius}} for every influence bone')
    inset = options['coreInset']
    insets = inset if isinstance(inset, dict) else {name: inset for name in part['bones']}
    insets = {name: insets.get(name, DEFAULTS['coreInset']) for name in part['bones']}
    require(all(isinstance(v, (int, float)) and 0 <= v < 0.5 for v in insets.values()),
            f'part {part["name"]}: coreInset must be in [0,0.5) (number or {{bone: value}})')
    slabs, distances = [], []
    for name in part['bones']:
        start, end = segment(rig, world, name)
        slabs.append(handle_distance(vertices, start, end, insets[name], radii[name]) / radii[name])
        distances.append(point_segment_distance(vertices, start, end))
    slabs, distances = np.array(slabs), np.array(distances)  # bones x vertices
    within = slabs <= 1.0
    contested = within.sum(0) > 1
    owner = np.where(within.any(0) & ~contested, within.argmax(0), -1)
    missing = [name for k, name in enumerate(part['bones']) if not np.any(owner == k)]
    require(not missing, f'part {part["name"]}: no handle vertices for {missing}; the bone core lies outside the art or handleRadius is too small')
    gaps = {}
    for a in range(len(part['bones'])):
        for b in range(a + 1, len(part['bones'])):
            pa, pb = vertices[owner == a], vertices[owner == b]
            gap = float(np.sqrt(((pa[:, None, :] - pb[None, :, :])**2).sum(-1)).min())
            gaps[f'{part["bones"][a]}|{part["bones"][b]}'] = round(gap, 6)
    return owner, distances, int(contested.sum()), gaps


def prune(weights, max_influences, below):
    pruned_mass = np.zeros(len(weights))
    out = weights.copy()
    out[out < below] = 0
    if out.shape[1] > max_influences:
        order = np.argsort(-out, axis=1)
        drop = order[:, max_influences:]
        np.put_along_axis(out, drop, 0, axis=1)
    pruned_mass = weights.sum(1) - out.sum(1)
    total = out.sum(1, keepdims=True)
    require(np.all(total > 0), 'pruning removed every influence of a vertex')
    return out / total, float(pruned_mass.max())


def solve(rig, mesh, method='harmonic'):
    world = forward(rig)
    result, report = {}, {}
    for part in rig['parts']:
        name = part['name']
        require(name in mesh['parts'], f'mesh has no part {name}')
        m = mesh['parts'][name]
        options = dict(DEFAULTS, **part.get('weights', {}))
        vertices, triangles = m['vertices'], m['triangles']
        count, bones = len(vertices), part['bones']
        stats = {'method': method}
        if len(bones) == 1:
            weights = np.ones((count, 1))
            stats.update(rigid=True)
        else:
            owner, distances, contested, gaps = handles_for(rig, world, part, vertices, options)
            labels = components(count, triangles)
            for island in np.unique(labels):
                require(np.any(owner[labels == island] >= 0), f'part {name}: mesh island {int(island)} has no handle vertices; split the part or bind it explicitly')
            if method == 'nearest':
                weights = np.eye(len(bones))[distances.argmin(0)]
                stats.update(control='rigid nearest-bone binding, expected to fold at bends')
            else:
                require(method == 'harmonic', f'unknown method {method}')
                edges, edge_weights, clamped = cotangent_edge_weights(vertices, triangles)
                fixed = np.flatnonzero(owner >= 0)
                values = np.eye(len(bones))[owner[fixed]]
                raw, steps = harmonic_solve(count, edges, edge_weights, fixed, values)
                stats.update(cgIterations=steps, clampedCotangentEdges=clamped,
                             rawMin=float(raw.min()), rawMax=float(raw.max()),
                             partitionOfUnityError=float(np.abs(raw.sum(1) - 1).max()))
                weights = np.clip(raw, 0, 1)
            stats.update(handleVertices={b: int((owner == k).sum()) for k, b in enumerate(bones)}, contestedHandleVertices=contested, handleGaps=gaps)
        weights, pruned = prune(weights, options['maxInfluences'], options['pruneBelow'])
        stats.update(maxPrunedMass=pruned, maxInfluencesUsed=int((weights > 0).sum(1).max()), vertices=count)
        inverse = {b: invert(world[b]) for b in bones}
        bindings = []
        for index in range(count):
            row = []
            for k, bone in enumerate(bones):
                w = float(weights[index, k])
                if w > 0:
                    lx, ly = apply(inverse[bone], vertices[index])
                    row.append({'bone': bone, 'weight': round(w, 9), 'x': round(float(lx), 7), 'y': round(float(ly), 7)})
            total = sum(item['weight'] for item in row)
            for item in row:
                item['weight'] = item['weight'] / total
            bindings.append(row)
        result[name] = {'bones': bones, 'weights': bindings,
                        'handles': [int(v) for v in (np.flatnonzero(owner >= 0) if len(bones) > 1 else [])],
                        'options': options}
        report[name] = stats
    return {'schema': WEIGHTS_SCHEMA, 'method': method, 'rigSHA256': sha256(rig['_path']), 'parts': result,
            'status': 'authored-weights-not-accepted'}, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rig')
    parser.add_argument('mesh')
    parser.add_argument('--out', required=True)
    parser.add_argument('--method', default='harmonic', choices=['harmonic', 'nearest'])
    args = parser.parse_args()
    try:
        rig = load_rig(args.rig)
        mesh = load_mesh(args.mesh)
        require(mesh.get('rigSHA256') == sha256(rig['_path']), 'mesh was built from a different rig file; rebuild it')
        weights, report = solve(rig, mesh, args.method)
    except (SkinError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'BLOCKED', 'errors': [str(error)]}, indent=1))
        sys.exit(2)
    weights['meshSHA256'] = sha256(args.mesh)
    write_json(args.out, weights)
    print(json.dumps({'status': 'SOLVED', 'parts': report}, indent=1))


if __name__ == '__main__':
    main()
