# Fighter presentation lessons (cases, not rules)

This document records one project: a Three.js 2.5D voxel fighter with a deterministic fixed-tick simulation. The voxel characters come from a separate character studio. The numbers below are measurements from that project, not tuning seeds. The portable rules live in `audio-feel`, `juice-vfx`, `projectile-hitscan`, `animation-blend`, `avatar-create` and the `threejs` adapter.

## "The hits feel weak"

What was wrong with the first version:
- every hit used the same few oscillator layers, so repeated hits sounded identical;
- punch, kick, throw and projectile hits were not distinguished;
- there were no voices;
- sparks were radially random rather than directional.

What helped:

| Change | Why it mattered |
|---|---|
| Role-layered impacts: contact transient, pitch-dropping saturated body, band-limited slap, low "whump", sparse crunch clicks, sub boom and short room tail on heavy hits | The transient gives the snap. The saturated body survives laptop speakers. |
| Source class from a presentation table keyed by move ID (punch / kick / slam / energy) | Kicks sound heavier than punches without the simulation knowing about audio |
| Four pre-rendered variants per cue, random choice and about ±4% rate jitter, slight pitch rise with combo index | Repeated jabs stop sounding like a machine gun |
| Effort, pain and defeat voices with one voice slot per fighter | A new grunt interrupts the old one instead of stacking |
| Pan from event x relative to the camera, and a bus low-pass "ringing ears" during the KO slow-motion | Space and moment without touching gameplay timing |

Cue synthesis was rendered offline sample by sample and cached. Warm-up ran in 8 ms idle slices after the audio unlock gesture. The longest single cue (crowd) took about 45 ms, so it was rendered at a lower sample rate and scheduled during menus. After warm-up there were 136 cached buffers, and a cached playback request cost about 0.3 ms.

No one could listen during development, so the evidence was objective:
- finite output and no clipping;
- the onset reaches near-peak within 2 ms;
- heavier hits are longer and have more low-band energy;
- kicks have more low-band energy than punches;
- vocal pitch measured by autocorrelation.

The first voice synthesis failed the pitch check: periodicity was about 0.3 because breath noise swamped the harmonics. Normalising the harmonics fixed it (periodicity above 0.8). Perceived quality stayed **not-run**.

Visual changes:
- spiky impact stars with a white core;
- cone sparks along the attacker-to-defender direction;
- two rings;
- limb trails sampled from hand/foot bones after the pose update;
- squash on the defender;
- a spring kick on the camera;
- floor cracks on throws and hard landings;
- focus lines on counter-hit launchers;
- a KO frame.

Two composition bugs were only visible in frozen captures:
- The first heavy-hit star was about 1.5 m across and hid the defender's head. It was halved.
- The full-screen white flash fired in the same beat as the negative KO frame and washed it out. The fix was to sequence them: negative frame, then high-contrast frame, then flash.
- The focus-line overlay also first rendered above the HP bars.

## Projectiles stuck after a clash

Two fireballs collided and were removed from the simulation. The simulation emitted `clash` but not `projectile-end`, so the presentation kept both glowing meshes frozen at the impact point.

Fix:
- emit a terminal event per projectile with reason `clash`;
- make the VFX layer retire any effect whose projectile ID is no longer live.

The regression test drives both players' quarter-circle inputs. It asserts:
- two spawns;
- one clash;
- two terminal events;
- zero live projectiles and no actor hit;
- both players can fire again.

## Arm jitter while walking

Metric: elbow and wrist world positions sampled at 60 fps. A frame counts as shaking when consecutive accelerations both exceed 25 m/s² and point in opposite directions.

Baseline: 717 shaking frames across 6 bodies and 11 gaits. With the arm avoidance layer switched off it dropped to about 54. That attribution came before any tuning.

Causes, in the order they were found:
1. A hard threshold in a style layer moved the hanging hand 3–4 cm outward once the hand dropped below a height. The swinging hand crossed it back and forth.
2. Swing amplitude switched between forward and back values at zero phase, and elbow bend used a hard `max`. Both produce velocity kinks.
3. The torso push field snapped to 1 cm bins. It cut off at bone z-range edges, and a thigh-root exclusion was a hard cutoff. The direction came from the single deepest sample.
4. Upper-arm penetration was handled by translating the hand target. For wide armor or coats this barely moved the upper arm, and sometimes pushed it deeper. The four rounds then gave very different totals on neighbouring frames, swinging from several centimetres to zero.

A first attempt "exempted" the upper-arm overlap already present in the hanging pose. It reduced jitter but raised clipping on a coat from about 911 to 2891 vertices, and was reverted.

What worked:
- smooth steps in the style layer;
- bin interpolation that keeps the full last row;
- bone blending in bind coordinates, not averaging per-bone pushes, which halved them;
- |d|⁴-weighted directions;
- rotation about the shoulder for upper-arm contacts;
- soft onset d²/(d+w);
- 0.9 gain per round;
- per-clip correction tables, filled on demand at about 1 ms per cell and blurred over time with σ ≈ 27 ms.

Results:
- walk/run: 717 → 5 shaking frames;
- all 52 motions: 639, against 601 with avoidance off (the rest is authored keyframe motion);
- standard-tier clipping audit: 1081 → 881 vertices;
- the old code fails the new regression test with 508 frames.

## Head-to-body ratio

The voxel style capped the ratio at 5, so a 226 cm character and a 175 cm one looked alike.

The range was widened to 2–8.5. Lengthening alone made an 8-head body's shoulders about 17% of height, against about 23% for real adults. So the high end also gets:
- legs that stretch more than the torso;
- a mild chest-band stretch;
- widening below the neck, blending back to 1 at the chin, with the head and face texture unchanged.

Body grid resolution follows the final scale, so the reference outfit stays at ≤ 29.4k triangles (budget 30k) across the range.

Library ratios became `style × height / reference height`. Head size barely changes with height, so this gives 226 cm → 6.33 and 147 cm → 3.44.

## Evidence notes

- An in-app browser pane that was hidden reported a 6000 ms worst frame. `document.visibilityState` was `hidden`, so the evidence was discarded rather than blamed on the change.
- A long background test run launched in the live worktree was later edited underneath. Results from such runs are only trusted when they show no new failures. Clean comparisons used a detached snapshot worktree.
