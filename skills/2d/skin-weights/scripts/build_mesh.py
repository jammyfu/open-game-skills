"""Build a grid mesh per rig part from the part's own alpha. Writes ogs.skin-mesh/1.

The mesh is a covering, not an outline tracer: every visible pixel (dilated by
`margin`) lies inside it, so UV triangles never cut ink off. Exit 0 ok, 2 invalid.
"""
import argparse
import json
import sys

import numpy as np

from skinlib import MESH_SCHEMA, SkinError, components, hull_first, load_rig, part_alpha, pixel_to_world, sha256, signed_areas, write_json


def build(rig):
    parts, notes = {}, []
    for part in rig['parts']:
        options = part.get('mesh', {})
        spacing = options.get('spacing', 8)
        threshold = options.get('alphaThreshold', 32)
        margin = options.get('margin', 2)
        alpha = part_alpha(rig, part)
        pixels, triangles, cells = build_grid_mesh_checked(alpha, spacing, threshold, margin, part['name'])
        height, width = alpha.shape
        pixels, triangles, hull, loops = hull_first(pixels, triangles)
        if hull is None:
            notes.append(f'{part["name"]}: {loops} outlines (islands); Spine/rig-c export needs one outline per attachment, split the part')
        world = pixel_to_world(part, pixels)
        labels = components(len(pixels), triangles)
        islands = int(labels.max()) + 1
        if islands > 1:
            notes.append(f'{part["name"]}: {islands} disconnected mesh islands; each needs its own handle bone')
        parts[part['name']] = {
            'image': part['image'],
            'sha256': sha256(rig['_path'].parent / part['image']),
            'imageSize': [width, height],
            'vertices': world.round(6).ravel().tolist(),
            'uvs': (pixels / [width, height]).round(8).ravel().tolist(),
            'triangles': triangles.ravel().tolist(),
            'islands': islands,
            'hull': hull,
            'stats': {'vertices': len(pixels), 'triangles': len(triangles), 'cells': cells,
                      'spacingPx': spacing, 'alphaThreshold': threshold, 'marginPx': margin},
        }
    return {'schema': MESH_SCHEMA, 'rigSHA256': sha256(rig['_path']), 'parts': parts, 'notes': notes}


def build_grid_mesh_checked(alpha, spacing, threshold, margin, name):
    from skinlib import build_grid_mesh
    try:
        pixels, triangles, cells = build_grid_mesh(alpha, spacing, threshold, margin)
    except SkinError as error:
        raise SkinError(f'part {name}: {error}') from error
    areas = signed_areas(pixels, triangles)
    if not (np.all(areas > 0) or np.all(areas < 0)):
        raise SkinError(f'part {name}: inconsistent triangle winding')
    return pixels, triangles, cells


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rig')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        mesh = build(load_rig(args.rig))
    except SkinError as error:
        print(json.dumps({'status': 'BLOCKED', 'errors': [str(error)]}, indent=1))
        sys.exit(2)
    write_json(args.out, mesh)
    summary = {name: p['stats'] for name, p in mesh['parts'].items()}
    print(json.dumps({'status': 'BUILT', 'parts': summary, 'notes': mesh['notes']}, indent=1))


if __name__ == '__main__':
    main()
