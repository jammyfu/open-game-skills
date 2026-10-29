# Pelican on a bicycle: skin weights, IK and bumps

<p align="center">
  <img src="docs/preview.gif" alt="A layered pelican with a fish in its beak pedals along a road; the tyres squash over stones" width="620"/>
</p>

<p align="center">
  <a href="README.zh.md">简体中文</a> ·
  <a href="../../skills/2d/skin-weights/SKILL.md">skin-weights Skill</a> ·
  <a href="../../skills/2d/spine-skeletal/SKILL.md">spine-skeletal audit</a>
</p>

A layered pelican pedals a bicycle down a road with a fish in its beak. The fish is skinned to a four-bone spine and keeps flopping. The tyres are soft rings that flatten where they touch the road and the stones. Each leg is one painted mesh driven by two-bone IK to a pedal on a rotating crank, and the wing is one mesh on two bones whose tip holds the handlebar through IK. All 26 layers come from a deterministic generator in this folder, so the case needs no downloads, no paid editor and no game assets.

It runs the whole [skin-weights](../../skills/2d/skin-weights/SKILL.md) pipeline and shows the ways weights go wrong: folding, rubber-bending and seams.

## Run it

```sh
python -m pip install -r requirements-dev.txt
python examples/pelican-bicycle/run.py --out /tmp/pelican-review
python examples/pelican-bicycle/make_figures.py --run /tmp/pelican-review   # optional: rebuild docs/
```

`run.py` exits 0 only when both expected outcomes are reproduced. The full run renders GIFs and takes a few minutes; pass `--no-render` for the reports alone.

| Step | Script | Output |
|---|---|---|
| Paint layers, rig, ride dynamics and motion | `make_art.py` | `source/` (26 PNG layers, `rig.json`, `motion.json`) |
| Alpha-covering, outline-first meshes | `build_mesh.py` | `mesh.json` |
| Harmonic weights and a rigid control | `solve_weights.py` | `harmonic.weights.json`, `nearest.weights.json` |
| Static lint | `lint_weights.py` | `*.lint.json` |
| IK pedalling trace, 121 samples at 60 Hz | `pose_trace.py` | `*.trace.json`, `*.pose.json` |
| Fold audit and surface strain | spine-skeletal `audit_skin.py`, `measure_surface.py` | `*.audit.json`, `*.surface.json` |
| Fixed-camera review | `render_skin.py` | `*.gif`, `*.sheet.png` |

## The fish

<p align="center">
  <img src="docs/fish.gif" alt="A fish skinned to a four-bone spine flops inside the pelican's pouch" width="560"/>
</p>

The fish lives between two rigid layers. The pouch interior is behind it and the beak with the pouch rim is in front, so it reads as being held. Its four bones form a travelling tail wave (three beats in two seconds). Bumps from the road add a flop and a hop. Weights are wide, because a fish should be soft all the way along. Each joint has a transition about 3 units wide, and no triangle folds.

## The wing on the handlebar

The wing is drawn as an arm: an upper wing with covert rows and a hand of dark primaries that curl round the grip. Both are one mesh skinned to two bones, `wing` and `wing_hand`, with the bend at the wrist. A two-bone IK chain keeps the tip on the grip while the pelican bobs on its spring and the bike pitches over stones, so the elbow angle moves between 34° and 39° and the tip stays on the bar within 2e-14 world units.

## The tyres and the road

<p align="center">
  <img src="docs/wheel.gif" alt="The rear tyre squashes over two stones" width="480"/>
</p>

- **Soft tyre.** The tyre is a ring mesh. Its inner edge is pinned to the non-rotating tyre centre bone, so it never cuts into the rim. Its tread follows 24 zero-length bones just inside the outer edge. The spoked rim is a separate rigid layer drawn behind the tyre and spins through the tyre's hole.
- **Contact.** For every frame, the tread is clipped to the actual surface: along each tread bone's ray, the part of the tyre that would sit below the road or a stone is pushed back onto it, at most 2.4 units (half the tyre wall). The press is smoothed once around the ring, so a stone leaves a rounded dent instead of a step. The bottom therefore flattens into a contact patch and takes the stone's shape, while the rest of the tyre stays round. Next to the patch the sidewall bulges by 0.25 of the press. A small resting sag of 0.45 units gives a loaded tyre on flat road.
- **Ride.** The bike lifts by 75% of what a rigid wheel would climb and pitches to follow, and the pelican rides on a spring (4.5 Hz, damping 0.22) so it overshoots. The fish hop is driven by that acceleration.
- **Kick.** Each wheel crushes the biggest stone and kicks a pebble back. Pebbles hide behind the road until then.
- **A seamless loop.** The road is exactly one tyre revolution long, so scrolling by one period per second matches the wheel's rotation. The spring is solved in the frequency domain, so the last sample equals the first exactly.

## Results

| Weights | Lint | Fold audit | Visible fold pixels |
|---|---|---|---|
| Harmonic, declared cores | PASS | PASS | 0 |
| Rigid nearest-bone control | FAIL | FAIL | rear tyre 323, front tyre 329, near leg 198, far leg 164, fish 6 |

- Both ankles stay on their pedals and the wing tip stays on the grip within 2e-14 world units, even while the bike hops and pitches (up to 2.1 units and ±2.5°). IK never leaves reach.
- The tread presses in by at most 1.5 units with no fold, and the rim edge never moves. The smallest tyre triangle keeps 26% of its setup area, inside the contact patch.
- The near knee swings 44° to 114°, its smallest triangle keeps 39%, and the shin stays straight (soft length 0.05). The fish is soft by design (0.15 to 0.58).

![Harmonic weights against a rigid nearest-bone binding at the worst frame of each part](docs/compare.png)

## What each figure shows

**Layers.** Every element is its own image, listed back to front. Weighted meshes list their bone count; rigid layers follow one bone. Backdrops use one quad each, so they export with a single outline.

![All 26 layers](docs/layers.png)

**Weights view.** One colour per bone, as in Spine's weights view. The blend band is the harmonic transition between rigid cores.

![Weights on the leg, neck, fish and tyre](docs/weights.png)

## Lessons this case encodes

- **A pass can still look wrong.** An earlier draft kept the foot inside the leg mesh with symmetric 30% insets. It passed the fold audit, but the thin shin curved like rubber into the ankle. The foot became a rigid layer under a painted ankle knob, and the knee transition moved into the thigh with asymmetric insets. `pose_trace.py` reports `softLengthFraction` per bone so this is measured.
- **Seams are caught before motion.** With one handle radius for every leg bone, the shin and foot rigid zones touched and the audit found a fold at that ankle. The seam lint now rejects that configuration without running any motion.
- **Fixed windows for scrolling worlds.** A scrolling backdrop is wider than the screen, so a camera fitted to every vertex zooms out. `render_skin.py --view x0,y0,x1,y1` fixes the world window.
- **The control proves the check.** The same meshes with rigid nearest-bone weights fold, and lint and audit reject them.
- **Export is verified, not assumed.** `export_rigc.py --verify-rigc` compiled this rig with rig-c 2.79.0 and posed it with rig-c's own core. All 26 layers match this evaluator within 2e-5 world units for the character and 7e-4 for the 200-unit-wide backdrops (float32). IK is baked into keys. The road and cloud tracks reset to zero at the loop point, so an engine that interpolates between the last two keys shows a one-frame jump. The official Spine editor/parser round trip was not run.

## Scope

This is a technical deformation case. It does not approve character design, anatomy, gameplay timing or a target runtime. The reference evaluator is not the shipping runtime; a game still exports its own trace for final evidence. All art is generated by repository code under the repository MIT licence.
