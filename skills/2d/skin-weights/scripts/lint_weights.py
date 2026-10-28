"""Static lint for authored skin weights against the rig and mesh they claim.

Checks (FAIL): stale rig/mesh hashes, unknown/foreign bones, negative or
unnormalized weights, too many influences, bind coordinates that no longer
reproduce the setup vertex, handle vertices that are not rigid, and detached
influence islands (a bone's weight reappearing in a second region = leakage).
Optional per-part bounds under rig part `lint`: maxReach (world units from the
bone segment) and maxGradient (weight change per world unit along an edge).
Measured values are always reported. Exit 0 PASS, 1 FAIL, 2 BLOCKED.
"""
import argparse
import json
import sys

import numpy as np

from skinlib import (SkinError, apply, components, edges_of, forward, load_mesh, load_rig, point_segment_distance,
                     read_json, require, segment, sha256, write_json)


def influence_islands(mask, edges, labels):
    """Connected pieces of one bone's support, counted inside each mesh island."""
    keep = mask[edges[:, 0]] & mask[edges[:, 1]]
    sub = edges[keep]
    parent = np.arange(len(mask))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in sub:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    roots = {}
    for v in np.flatnonzero(mask):
        roots.setdefault(int(labels[v]), set()).add(find(v))
    return max((len(r) for r in roots.values()), default=0)


def lint(rig, mesh, weights, tolerance=1e-6, bind_tolerance=1e-4, support=1e-4):
    errors, measured = [], {}
    if mesh.get('rigSHA256') != sha256(rig['_path']):
        errors.append('mesh was built from a different rig file')
    if weights.get('rigSHA256') != sha256(rig['_path']):
        errors.append('weights were solved for a different rig file')
    world = forward(rig)
    for part in rig['parts']:
        name = part['name']
        require(name in mesh['parts'] and name in weights['parts'], f'part {name} missing from mesh or weights')
        m, w = mesh['parts'][name], weights['parts'][name]
        vertices, triangles = m['vertices'], m['triangles']
        rows = w['weights']
        require(len(rows) == len(vertices), f'part {name}: {len(rows)} weight rows for {len(vertices)} vertices')
        bones = part['bones']
        cap = part.get('weights', {}).get('maxInfluences', 4)
        dense = np.zeros((len(vertices), len(bones)))
        worst_bind = 0.0
        for index, row in enumerate(rows):
            if not row:
                errors.append(f'{name} v{index}: no influences')
                continue
            if len(row) > cap:
                errors.append(f'{name} v{index}: {len(row)} influences exceed maxInfluences {cap}')
            seen = set()
            for item in row:
                bone = item.get('bone')
                if bone not in bones or bone in seen:
                    errors.append(f'{name} v{index}: bone {bone} is unknown, duplicate or not an allowed influence of this part')
                    continue
                seen.add(bone)
                value = item.get('weight')
                if not isinstance(value, (int, float)) or not np.isfinite(value) or value < 0:
                    errors.append(f'{name} v{index}: invalid weight {value}')
                    continue
                dense[index, bones.index(bone)] = value
                rebuilt = apply(world[bone], [item.get('x', np.nan), item.get('y', np.nan)])
                worst_bind = max(worst_bind, float(np.linalg.norm(rebuilt - vertices[index])) if np.all(np.isfinite(rebuilt)) else np.inf)
            total = dense[index].sum()
            if abs(total - 1) > tolerance:
                errors.append(f'{name} v{index}: weights sum to {total:.9f}')
        if worst_bind > bind_tolerance:
            errors.append(f'{name}: bind coordinates drift {worst_bind:.3g} from setup vertices (stale bindings after a setup change?)')
        for index in w.get('handles', []):
            if dense[index].max() < 1 - tolerance:
                errors.append(f'{name} v{index}: handle vertex is not rigid ({dense[index].max():.6f})')
        edges = edges_of(triangles)
        median_edge = float(np.median(np.linalg.norm(vertices[edges[:, 0]] - vertices[edges[:, 1]], axis=1)))
        bounds = part.get('lint', {})
        min_gap = bounds.get('minTransition', 2*median_edge)
        handles = np.array(w.get('handles', []), dtype=int)
        gaps = {}
        if len(bones) > 1 and handles.size:
            owner = dense[handles].argmax(1)
            for a in range(len(bones)):
                for b in range(a + 1, len(bones)):
                    pa, pb = vertices[handles[owner == a]], vertices[handles[owner == b]]
                    if len(pa) and len(pb):
                        gap = float(np.sqrt(((pa[:, None] - pb[None]) ** 2).sum(-1)).min())
                        gaps[f'{bones[a]}|{bones[b]}'] = gap
                        if gap < min_gap - 1e-9:
                            errors.append(f'{name}: rigid zones of {bones[a]} and {bones[b]} are {gap:.3g} apart (< minTransition {min_gap:.3g}); '
                                          'the weight transition collapses to a seam. Reduce handleRadius or raise coreInset')
        labels = components(len(vertices), triangles)
        lengths = np.linalg.norm(vertices[edges[:, 0]] - vertices[edges[:, 1]], axis=1)
        gradient = np.abs(dense[edges[:, 0]] - dense[edges[:, 1]]).max(1) / np.maximum(lengths, 1e-12)
        islands, reach = {}, {}
        for k, bone in enumerate(bones):
            mask = dense[:, k] > support
            islands[bone] = influence_islands(mask, edges, labels)
            if islands[bone] > 1:
                errors.append(f'{name}: influence of {bone} forms {islands[bone]} detached islands (weight leakage)')
            start, end = segment(rig, world, bone)
            reach[bone] = float(point_segment_distance(vertices[mask], start, end).max()) if mask.any() else 0.0
        if 'maxReach' in bounds:
            for bone, value in reach.items():
                if value > bounds['maxReach']:
                    errors.append(f'{name}: {bone} influences a vertex {value:.3g} from its segment > maxReach {bounds["maxReach"]}')
        if 'maxGradient' in bounds and gradient.max() > bounds['maxGradient']:
            errors.append(f'{name}: weight gradient {gradient.max():.3g}/unit exceeds maxGradient {bounds["maxGradient"]}')
        measured[name] = {'vertices': len(vertices), 'maxInfluences': int((dense > 0).sum(1).max()),
                          'maxBindDrift': worst_bind, 'maxWeightGradientPerUnit': float(gradient.max()),
                          'influenceIslands': islands, 'maxReach': reach, 'handleGaps': gaps, 'minTransition': min_gap,
                          'boundsDeclared': sorted(bounds)}
    return errors, measured


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rig')
    parser.add_argument('mesh')
    parser.add_argument('weights')
    parser.add_argument('--out')
    args = parser.parse_args()
    code = 0
    try:
        rig, mesh, weights = load_rig(args.rig), load_mesh(args.mesh), read_json(args.weights)
        errors, measured = lint(rig, mesh, weights)
        if weights.get('meshSHA256') != sha256(args.mesh):
            errors.insert(0, 'weights were solved for a different mesh file')
        status = 'FAIL' if errors else 'PASS'
        code = 1 if errors else 0
        report = {'status': status, 'errors': errors[:200], 'errorCount': len(errors), 'measured': measured,
                  'scope': 'static weight structure only; deformation needs pose_trace + audit_skin'}
    except (SkinError, KeyError, TypeError) as error:
        report, code = {'status': 'BLOCKED', 'errors': [str(error)]}, 2
    if args.out:
        write_json(args.out, report)
    print(json.dumps(report, indent=1)[:4000])
    sys.exit(code)


if __name__ == '__main__':
    main()
