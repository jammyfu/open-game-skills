# Table-tennis kit

Distilled from building a Three.js + React table-tennis game whose ball physics is shared with a spin-teaching demo. Every number here is a **tuning seed** measured in that build, not a universal constant. Re-measure after you change the integrator, coefficients or input mapping.

## 1. Physical seeds (SI units)

| Quantity | Seed | Note |
|---|---|---|
| Ball radius / mass | 0.02 m / 0.0027 kg | 40 mm ball |
| Moment of inertia | (2/3)·M·R² | thin shell: `M·R²/I = 1.5` |
| Drag | `F = −½ ρ C_d A ‖v‖ v`, ρ 1.2, C_d 0.5 | |
| Magnus | `F = 5e-6 · (ω × v)` | positive coefficient; topspin dips |
| Spin decay | `ω *= 1 − 0.05·dt` | |
| Table contact | e 0.89, μ 0.22 | topspin skids long, backspin checks short |
| Inverted rubber | e 0.80, μ 0.90 | pimples e 0.86 μ 0.32; long pimples e 0.70 μ 0.04 |
| Table | 2.74 × 1.525 m, top at 0.76 m, net 0.1525 m | net width 1.83 m |
| Physics substep | 1/1200 s (game), 1/800 s (solver) | solver margins cover the difference |

Contact is one impulse model for every surface. `n` points from the surface to the ball's centre, and `surfV` is the surface's velocity at the contact:

```js
function contact(s, n, surfV, { e, mu }) {
  const vrel = sub(s.v, surfV);
  const vn = dot(vrel, n);
  if (vn >= 0) return null;                       // separating
  const r = scale(n, -R);                         // centre → contact point
  const u = add(vrel, cross(s.w, r));             // slip velocity of the contact point
  const ut = sub(u, scale(n, dot(u, n)));
  const Jn = -(1 + e) * M * vn;
  const Jroll = (M * len(ut)) / (1 + (M * R * R) / I); // impulse that stops slip (rolling)
  const Jt = scale(norm(ut), -Math.min(mu * Jn, Jroll));
  s.v = add(s.v, scale(add(scale(n, Jn), Jt), 1 / M));
  s.w = add(s.w, scale(cross(r, Jt), 1 / I));
}
```

The opponent uses the same code in a mirrored frame: `mirror(a) = [−a.x, a.y, −a.z]`, applied to position, velocity and angular velocity. That is a proper rotation, so cross products stay valid.

## 2. Strokes: gesture → racket motion

The input is the pointer's velocity over the last 70 ms, measured on a vertical plane in front of the player so that it reads directly in m/s. `push` is the racket's speed along the face normal. `brushUp` and `brushSide` are its speeds along the face. The face angle is **not** in this table: it is solved per shot.

| Gesture at contact | Stroke | push (m/s) | brushUp (m/s) | brushSide | Target depth past net |
|---|---|---|---|---|---|
| almost still (< 0.8 m/s) | block | 1.1 | 0.3·vy | 0 | 0.75 |
| up, slow | drive | 1.9 + 0.35s | 0.9·vy, 1..5 | 0.2·vx | 0.82 |
| up, fast (> 4.5) | loop | 2.2 + 0.3s | 1.15·vy, 5..15 | 0.2·vx | 0.88 |
| up, fast, ball > 0.40 m above table | smash | 4.4 + 0.45s, 5..9 | 0.25·vy, 0..3 | 0 | 0.92 |
| up, contact over the table | flick | 1.7 + 0.25s | 0.8·vy, 2..7 | 0.3·vx | 0.85 |
| down, slow | push (搓) | 1.45 + 0.12s | 0.8·vy, −4..−1 | 0.2·vx | 0.60 |
| down, fast | chop (削) | 1.5 + 0.12s | 1.2·vy, −14..−5 | 0.15·vx | 0.95 |
| sideways dominant | side (侧拧) | 1.7 + 0.3s | 0.4·vy | 0.85·vx, ±9 | 0.80 |

Here `s` is swing speed, and the classification uses `|vy| ≥ 0.7·|vx|` for up/down. The opponent picks the same keys and drives them with a level-scaled "standard swing" (`k = 0.55 + 0.6·level`).

Serve: the spin comes from the same contact model (a falling ball, the face tilted back 8°, brush taken from the swing), clamped to 65 rev/s. Placement is solved separately (§4).

## 3. Assists per difficulty (seed)

| Knob | Easy | Normal | Hard | Meaning |
|---|---|---|---|---|
| spinRead | 1.0 | 0.9 | 0.7 | fraction of incoming spin the face solve knows; own brush is always known |
| faceGain | 4° | 8° | 12° | face change per reach of racket offset (below = open, above = close, side = yaw) |
| reach | 0.30 m | 0.22 m | 0.17 m | swept-path hit radius |
| autoHeight | 1.0 | 0.35 | 0 | racket height pulled toward the predicted contact height |
| opponent level | 0.3 | 0.6 | 0.88 | speed 2.2 + 4.5a m/s, reaction 0.22 − 0.14a s |

Depth footwork is always automatic: the racket plane eases toward the predicted contact depth at about 4 m/s. Without that, the game becomes a 3D aiming test.

**The face lever and its hint.** The lever reads the hand's *intended* racket position: the pointer after the height assist, before the visual racket's smoothing. Read it at the exact contact substep, interpolated between the last two frames. The hint ring must not be an angle formula. Run the game's own shot (same stroke from a typical swing, same target, same partial read), scan the racket offset across the reach, and draw the ring at the centre of the longest window that really lands. On normal that window was about 6 cm wide against 46–55 rev/s topspin; on hard it was 1–3 cm.

## 4. Solvers

**Face solve** (`solveShot`). Inputs: the contact state, push/brush, and a target `[x, z]`.

1. Scan pitch from −40° to 70° in 5° steps with yaw 0. Keep pitches whose flight clears the net by more than half the margin and lands within the flight cap (1.0 s). Seed Newton from the two whose landings are closest to the target, plus the previous shot's face.
2. Run a 2D Newton on pitch/yaw against the landing point, with a finite-difference Jacobian (h = 0.25°), the step capped at 8°, and pitch clamped to −45..72°.
3. Accept a solution when the landing error is under 8 cm, the clearance is at least 3.5 cm and the flight is at most 1.0 s.
4. Otherwise, move the target 12 cm deeper (up to 8 cm from the end line) and solve again.
5. If that still fails, retry with push ×0.75 and then ×0.55. Brush is unchanged, so the stroke keeps its spin character.
6. Return the least-bad solution only as a last resort. Its failure is then real and visible in play.

**Serve solve.** Use a 3D Newton on the launch velocity. The residual is `[net clearance − C, second-bounce z − Z2, second-bounce x − X2]`, seeded by a coarse grid over vz/vy. Solve in the server-at-−z frame and mirror the result for the player's serve. It takes about 8 ms in Node.

**Contact planning.** Predict to the second bounce, skip the server's own first bounce, and score the samples between the bounces:

`score = −|h − hPref|·(h > hPref ? 2.4 : 2) − 0.22·|z − zPref| − (rising ? 0.03 : 0)`

| Style | zPref | hPref | Idle z | Stroke preference |
|---|---|---|---|---|
| attack | 1.6 m | 0.35 m | −1.78 | smash high balls, loop low ones, push/flick short backspin |
| chop | 2.45 m | 0.12 m | −2.5 | chop everything long, push short backspin, occasionally loop or smash |

Hit by **time** (`clock ≥ planT0 + plan.t`, within reach), not by crossing a z plane: nearly vertical balls never cross it.

## 5. Calibration: what the physics should reproduce

Matrix: 8 strokes × 5 incoming balls × spin read 1 or 0.

| Incoming | spinRead = 1 | spinRead = 0 (face for a no-spin ball) |
|---|---|---|
| topspin drive, 35 rev/s, 7 m/s | every stroke lands | every stroke goes long: "topspin flies out" |
| backspin push, 35 rev/s | block fails, smash nets; push, chop, loop and drive land | flat strokes drop into the net or own side; push and chop still land |
| heavy chop, 55 rev/s | loop returns at 68 rev/s topspin | loop still lands; everything else drops |
| side 30 + top 10 | lands | block, loop and smash are pulled out; drive and push survive |

The tolerance when spin is unread is small. A face correction rescues the shot only inside a window of about **2–4°** for fast strokes (wider for block and push). This is why spin-read is the main difficulty knob, and why the face lever needs a hint.

## 6. Pitfalls found while building it

- **Moon-ball branch.** Newton started near pitch 40° converged on lobs that cleared the net by 3 m. Scan first, then cap flight time.
- **Low, fast, skidding topspin.** With nothing else in place, the solver could not clear the net (best clearance about 2 cm), so even a perfect-reading opponent erred about 50% of the time. Pace absorption plus a deeper target fixed this.
- **Contact picked too low.** Weighting depth more than height chose contacts 8–14 cm above the table. Weight height about 2× more.
- **The swing moves the racket.** A loop gesture moves the racket 20–30 cm, so testing an instantaneous point gives whiffs. Use a swept test over the last 70 ms of the hand's path.
- **Where the face lever reads from.** Three wrong versions, in the order they were tried:
  - The *rendered* racket position lags the pointer by about 30 ms (0.1–0.2 m during a swing).
  - The *path midpoint* always lies behind the swing direction, so every upswing opened the face.
  - The un-interpolated frame sample carries ±8 ms of timing noise, about ±6 cm at a loop's 7.5 m/s.
  
  What works is the intended position at the contact substep, interpolated within the frame. Swing timing then legitimately changes the face.
- **The hint drifted from the real shot.** A hint computed as `(full-read face − partial-read face) / gain` used a different stroke and target than the game's shot. The bot followed it to within 5 mm and still hit long. Scan the real landing window instead, and show no hint when the solve itself is unreliable.
- **Opponent noise.** With windows of 2–4°, a pitch noise σ of 3° made the easy opponent miss 40% of shots. Use `0.25 + 0.8·(1 − level)` degrees, and give weaker opponents slower swings (bigger windows).
- **Spin rendering.** True spin (30–60 rev/s) aliases at 60 fps. Display it at 1/10, and color the trail by spin type (red for top, blue for back).
- **Background pane.** A hidden browser tab pauses `requestAnimationFrame`, and the game sits at clock 0. Run bots in headless Chromium, and never take timing evidence from a hidden page.
- **First frame.** The first `requestAnimationFrame` timestamp can be earlier than `performance.now()` at construction. A negative dt multiplied by a zero-length move (`0 × −∞`) turned the idle opponent's position into NaN, and it vanished. Bot runs that began with the opponent serving overwrote the position and hid the bug. Clamp dt to 0 or more and guard zero distances. Check the idle state with no bot running.
- **Harness, not game.** With eight headless Chromes in parallel, some browser processes died and the driver waited forever. Run at most two at a time with a driver timeout, and record those runs as `blocked` (harness), not as game failures.

## 6b. Self-play reference (this build)

Headless self-play: an opponent at each level against a perfectly positioned player that reads all the spin and chooses strokes by the incoming ball. 80 points per cell.

| Opponent | vs attack: shots per point | vs chop: shots per point | Opponent error mix |
|---|---|---|---|
| easy (0.3) | 5.6 | 11.0 | mostly long |
| normal (0.6) | 9.1 | 7.0 | mostly long |
| hard (0.88) | 26.8 | 20.4 | long; some points timed out |

Long rallies against the chopper on easy are expected: chops are slow and floaty, so the windows are large. These figures say nothing about how hard a human finds each level.

## 7. Reproduction checklist

1. A `physics` module: the seeds above, `stepBall`, `collide` (net, table, floor events), `contact`, `predict`, `racketNormal`/`racketAxes`, `solveFace`/`solveShot`, `solveServe`, `mirror`.
2. A pure `rules` module: rally (serve own-side-first, return after exactly one bounce, net, own side, out, double bounce) and match (11 points, win by 2, serve swaps every 2 points and every point from 10–10). Unit-test it.
3. A `strokes` table shared by player and opponent (§2).
4. An `ai` module: levels, styles, a serve catalog (short backspin, side-backspin, reverse side-backspin, side-topspin, fast long, no-spin), contact planning, stroke choice, spin read and noise.
5. An `input` module: pointer → plane at the player's depth → target and 70 ms swing velocity. Lift the racket above the finger on touch. Space or tap tosses the serve.
6. A `game` loop: a fixed substep inside `requestAnimationFrame` with dt clamped to 1/20 s; swept hit test; face solve with partial spin read plus the racket-offset lever; hint ring at the corrected racket position; HUD at about 12 Hz; and failure tips built from the logged incoming spin and stroke.
7. Presentation: table, net and lines, a textured ball, blob shadow, spin-colored trail, landing rings, a pooled set of synthesized Web Audio voices (table "tick", racket "tock", brush noise layer, smash crack), an opponent jersey color per style, and a camera that follows the racket slightly.
8. Evidence: unit tests, the §5 matrix, headless self-play per level × style, and a `?bot` browser driver dispatching real pointer events (debug-assisted). Human feel stays `not-run` until someone plays.
