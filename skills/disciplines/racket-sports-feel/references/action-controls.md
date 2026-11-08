# Action controls (button-charge mode)

This is the second pass of the same table-tennis build. Pointer-swing input was replaced by the control grammar of tennis action games: run into position, press a shot button before the ball arrives, hold it to charge, and let the swing fire on its own. The opponent is an animated PunchBox character. The player's own side shows only the racket. Physics, solvers and rules are unchanged from the [table-tennis kit](table-tennis-kit.md). Every number below is a tuning seed from that build.

## 1. Input grammar

| Input | Meaning |
|---|---|
| Left mouse / J | topspin family |
| Right mouse / K | backspin family |
| Both within 90 ms / L | flat (smash) |
| Right, then left within 350 ms | lob |
| Left, then right within 350 ms | drop / short push |
| Hold any shot button | charge: 0→1 over 0.65 / 0.8 / 0.9 s (easy / normal / hard); movement speed ×0.45 while held |
| WASD, Shift, 1/2/3 | move, dash (4.3 vs 3.0 m/s, accel 24, decel 30), snap to the near / mid / far depth (1.68 / 2.3 / 3.0 m from the net) |
| Mouse over the opponent half | landing reticle (clamped to ±0.68 m, 0.22–1.27 m past the net) |
| Space | serve; the buttons held 0.1 s before serve contact choose top / back / no-spin, Q / E add side, and hold time is charge |

The shot is queued at press time and consumed at commit. The press timestamp is real time (`performance.now`), because simulation time freezes during hitstop.

## 2. Button × position → technique

| Button | Over the table | Near (< 1.98 m) | Mid | Far (≥ 2.62 m) |
|---|---|---|---|---|
| top | flick | drive (loop if charge ≥ 0.45) | loop | loop |
| back | push | push | long push (chop motion, smaller) | chop |
| flat | smash (weaker on a low ball) | smash | smash | smash |
| lob | flick | lob | lob | lob |
| drop | short push | short push | short push | short push |

Charge `c` raises the synthetic swing speed. For example, loop `s = 5.2 + 5c` gives about 15 → 51 rev/s of topspin against a 35 rev/s drive. A flat shot with ball height > 0.38 m is a chance shot: push ×(1.15 + 0.2c), plus a slow-motion beat.

## 3. Contact selection and commit

- **Selecting the contact.** Predict the incoming ball once (dt 1/600). Re-predict at the receiver's own bounce, which removes the drift between the solver step and the game step. Score every sample between the own-side bounce and the next bounce or floor:

  `overflow·10 + |h − hIdeal|·1.6 + |Δdepth|·0.25`

  Here `overflow = max(0, distance to the required root − (magnet + speed·(t − react − 0.05)))`. The ideal height is 0.18 m for the player, 0.20 for an attacker and 0.05 for a chopper.
- **Required root.** `contact − clip blade offset` (in the xz plane), with the offset rotated by the athlete's **base** yaw.
- **Commit.** Swing when the best contact is within `SWING_LEAD` = 0.3 s and the distance is within the magnet: 0.9 / 0.62 / 0.42 m for the player, `0.35 + 0.3·level` for the opponent. If no button was pressed, easy and normal auto-block and hard does not swing.
- **During the swing.** Pull the logical position toward the root at `max(3.2, distance / time left)` m/s, so the athlete always arrives by contact.
- **At contact.** Resolve the hit at the scheduled time and only if the real ball is within 0.3 m of the predicted point and has bounced exactly once on that side. Otherwise it is a whiff.

## 4. Hit quality

- Timing: `tq = clamp((pressLead − 0.08) / 0.22)`.
- Position: `pq = 1 − 0.6·clamp((magnetDist − 0.12) / (magnet − 0.12))`.
- Quality: `q = (0.35 + 0.65·tq)·pq`. A block is capped at 0.7.

Effects of quality:
- **Grade:** above 0.86 is 完美 (perfect), above 0.62 is 好 (good), a low `tq` is 仓促 (rushed), and anything else is 勉强 (scraped).
- **Strength:** power ×(0.8 + 0.2q).
- **Accuracy:** target spread `(1 − q)·0.25 m·noise`, and face noise `(0.25 + 2.2(1 − q))°·noise`.

The face is still solved with the partial spin read: 1 / 0.95 / 0.85. So a wrong spin family loses points through the real physics, not through a scripted rule.

## 5. Feel layer

| Element | Seed |
|---|---|
| Hitstop (simulation and animation frozen, render keeps going) | `0.03 + 0.08·power`, ×1.2 on perfect; power = speed/22 + 0.35·charge (+0.3 on a chance shot) |
| Chance smash | slow motion ×0.35 for 0.35 s |
| Camera | shake `0.2 + 0.9·power²` decaying at 2.5/s; FOV kick `2.5°·power²` decaying at 18°/s |
| Particles | one pooled Points set of 48 sparks; `8 + 22·power` per hit, colored by shot family |
| Ball | glow sprite scaled by speed; a camera-facing ribbon trail that widens with speed (red = top, blue = back, gold = flat) |
| Floor markers | stand ring at the required root (blue = reachable, orange = too far), a gold star when a chance shot is available, a reticle colored by the queued shot, a charge ring at the feet |
| Audio (synthesised) | brush noise layer ∝ friction; smash = noise + 120 Hz thump + square crack; perfect = two sines (1760 / 2637 Hz); charge = one persistent saw voice whose pitch and filter rise with charge; cheer = band-passed noise swell |

## 6. Animated players (PunchBox)

- **Export.** Run `tools/export-players.mjs` (in the game repository). It reads the PunchBox source only. It builds a preset with `tableTennisRecipe` (the standard table-tennis body, because the motions were fitted to it). It bakes `idle`, `run`, `victory`, 6 strokes and 7 serves at 60 fps (about 5–6 MB per player), and writes JSON with each clip's `contactTime`, the blade centre at contact in the character's root frame, the blade velocity, `tossTime` and the palm ball position.
- **Which presets.** Use original archetype presets only. Skip any set that imitates a specific commercial game's characters.
- **Footwork clip.** Build a shuffle by taking the leg tracks from `run` and every other track from `tt-ready`. Weight it by speed and lean the body into the direction of motion.
- **Stroke playback.** If there is less time left than the clip's contact time, speed the clip up (to ×1.6 at most) and start it mid-way. If there is more, slow it (to ×0.7 at least).
- **Arm IK.** Run CCD on lower arm, upper arm and chest with per-bone limits of 0.6 / 0.6 / 0.25 rad, weighted inside ±0.16 s of contact. Apply it after `mixer.update` every frame, so it never accumulates.
- **Ready pose.** The exported ready pose holds the racket at 0.68 m, below table height, so a far opponent's racket was hidden behind the table. Lift it with the same IK, at weight 0.7, toward a point in front of the body at 0.98 m.

## 7. Serve pipeline

1. Start the windup clip. The pendulum serves share one windup: back, float, side-under and side-top all toss at 0.567 s and contact at 1.1 s.
2. Keep the ball on the palm until `tossTime`. Then launch it ballistically with `v0 = (contact − palm + ½·g·T²) / T`, where the contact point is `root + blade offset (base yaw) + 3 cm`.
3. 0.1 s before contact, read the held buttons and Q / E and cross-fade to the matching variant clip at the same time offset.
4. At contact, set the ball **exactly** to the planned contact point. Then solve the serve toward the reticle, with spin `top = ±(34 or 48)·(0.45 + 0.55c)` and `side = 32·(0.45 + 0.55c)`.
5. Lock the server's yaw for the whole serve.

## 8. Pitfalls from this pass

- **Re-prediction dropped the bounce.** Re-predicting at the own-side bounce produces a trajectory with no own-side bounce in it, so contact selection returned nothing and the player never swung. If the rally already records the bounce, select from "now" until the next bounce or floor.
- **Gating on the bounce.** Gating the commit on "has already bounced" made short balls unplayable. Commit on the prediction, and check legality at contact.
- **Serve contact over the table and too low.** Serving from 1.72 m put the clip's contact (0.39 m forward) over the table, only 2–7 cm above it, so the serve solver failed every time. Contributing causes were the yaw following the ball, and a launch half a frame late that had already dropped the ball. Fix: stand at 2.0 m, lock yaw, and launch from the planned point.
- **Hiding the body node hid the racket.** In the exported GLB the bones sit under the body mesh node, so `visible = false` on that node hid the hand bone's racket too. Set `material.visible = false` (and turn off shadows) instead.
- **Bot artifacts.**
  - A bot that released all buttons every non-rally frame cancelled its own serve spin (every serve came out as no-spin).
  - Eight parallel headless Chromes stalled. Run them one or two at a time with timeouts.
  - Record harness stalls as `blocked`, not as game results.

## 9. Racket poses and clipping (third pass)

Requirement: every racket pose must look like a real receiving posture, the swing must match the stroke, and the racket must never pass through the table, the net or the floor.

- **The drawn racket is the computed racket.** Solve the face when the swing commits, using the predicted contact state, and use that same face (noise included) for the physical hit. At contact the drawn face normal equals the physics normal (measured error 0°). The blade centre sits at `ball − n·(R + half the blade thickness)` (measured error under 8 mm). The swing passes through that point along the physics racket velocity, `n·push + up·brushUp + right·brushSide`.
- **Racket-only side.** A procedural rig is easier to make correct than a hidden body's hand bone.
  - **Ready pose:** in front of the body, above the table; lower when far from the table. It flips between forehand (red face toward the net) and backhand (black face toward the net) by the side of the predicted contact.
  - **Swing:** a Hermite path ready → backswing → contact → follow-through → ready.
  - **Per stroke:** backswing and follow-through length, timing, an extra follow-through offset, a face roll during follow-through, and a tip-direction hint for forehand and backhand.
- **Animated opponent.**
  - Pick the clip by stroke and by forehand / backhand.
  - Clips whose contact face is black (backhand block, backhand flick) flip the target normal.
  - Near contact, rotate the hand toward the physics face (capped at 70°), then re-run the arm IK so the blade centre returns to the ball.
- **Lift the whole swing.** Some exported clips carry the racket about 0.6 m high, below the 0.76 m table top. Once the athlete is pulled close to the table, the windup and follow-through pass through the table. Lift the entire swing by `ball height − clip blade height at contact`, ramped in over the windup, held through contact, faded out over 0.35 s. That keeps the swing's shape. An IK window of ±0.16 s fixes only the contact itself.
- **Clipping check.**
  - Sample 32 rim points (both rubber surfaces) plus 3 handle points in the racket's local frame.
  - The table counts as solid from 4 mm above its top to 8 cm below. The net plane counts out to 16 cm beyond the table sides.
  - **Racket-only side:** first slide the blade up within its own plane, by at most 6 cm, so the ball stays on the face. Only then lift straight up.
  - **Animated side:** pull the blade centre out with arm IK, up to 6 passes.
  - Measured residual after the fix: 0 for both sides across every stroke type. The fix moved the racket by at most about 1 cm in the contact frame (one smash).
- **Pitfalls.**
  - `q.slerpQuaternions(identity, q, k)` silently returns the identity, because it copies the first argument into `this` before reading the second. The arm IK did nothing for two passes until the alias was removed.
  - A tip hint nearly parallel to the face normal projects to noise, and the handle points the wrong way. Keep tip hints roughly in the face plane, for example "outward and up" for a flick whose face points forward.
  - From behind the player, an open-faced forehand push correctly shows the black (back) side. Check the face geometry before "fixing" a colour that looks wrong.

## 10. Gesture aim and read-by-button (fourth pass)

The same grammar now drives the rally and the serve: **buttons pick the spin family, hold time is power, the drag while holding is the line and the sidespin, and the direction keys pick the depth zone.**

- **Drag sampling.**
  - Record the pointer when the first shot button goes down. Use pointer capture so the drag survives leaving the canvas.
  - `D = pointer − press point`, normalised by canvas height.
  - Freeze `D` on release, and lock it when the swing commits.
- **Drag mapping.**
  - Dead zone `|D| < 0.03`.
  - Angle `θ = atan2(Dx, |Dy|)`, clamped to ±60°.
  - Line: 0 means a straight line from the contact x; ±1 means the far sideline (±0.66 m).
  - Sidespin factor `sign(Dx)·clamp((|Dx| − 0.04)/0.25)`, multiplied by a per-stroke cap on lateral racket brush. Loop is 7 m/s, about 24 rev/s.
  - The face solver still lands the ball on the dragged line, so the sidespin shows only as a curving path.
- **Power sets depth.** Each stroke has a range of target distance from the net, from power 0 to power 1. Push runs 0.30 → 0.95 m, loop 0.80 → 1.20 m.
- **Power window.** Count power and press timing only from the opponent's contact (or serve). Holding while your own shot is still in flight does not count. If a button is already held when the opponent hits, start charging from that instant instead of making the player re-press.
- **Serve.**
  - No separate serve key: pressing left or right starts the toss and picks top- or backspin (both together means no spin). Hold time is power and the drag is the line and sidespin, the same gesture as a rally shot.
  - Before the toss, the pointer ray hits a vertical plane 15 cm behind the end line. That point is the contact point, clamped to the legal box. Draw a marker that renders over the racket.
  - The toss is solved to reach that point.
  - Serve depth comes from the upward drag, not from power. Power is already the spin, and a short heavy-backspin serve must stay possible.
- **Read by button.** The pressed button is the player's judgement of the incoming spin. Solve the face with the spin the button implies, and hit with the true spin.
  - Left on backspin is correct only if power ≥ `clamp((−top − 15)/40)·0.8`. Otherwise the solver assumes no spin.
  - A low flat hit on backspin is wrong.
  - Right on topspin, near or mid, is wrong: the solver assumes −12 rev/s. In the far zone it is correct (a chop).
  - Sidespin is read only when the drag follows the incoming ball's on-screen curve direction. Otherwise only 30% of it is read.
  - Difficulty only moves a wrong read toward the truth by `wrongFix` (0.6 / 0.25 / 0). The penalty is real physics:
    - backspin 35 with left at 20% power goes into the net; the same press at 80% clears;
    - topspin 35 with right at the near table goes long;
    - sidespin 30 that is not dragged drifts 0.45 m.
  - After a lost point, show which judgement was wrong.
- **Spin colours belong to the core game, not to the hints.**
  - The main colour comes from top/back spin: orange-red, blue or white, more saturated as spin grows.
  - Sidespin is a helix ribbon around the trail, coloured by on-screen curve direction (green right, purple left). The helix turns at a rate proportional to the sidespin.
  - Give the shot buttons the same colours.
  - The predicted path line is the difficulty assist: full / up to the bounce / none.
- **Pitfalls.**
  - Power runs from the opponent's contact to the swing commit (0.3 s before your contact), so the reachable maximum depends on the ball's flight time. Tune `chargeTime` against real flight times (about 0.6–1.0 s), not against an idle hold.
  - A swing toward +x brushes the ball so that it curves toward −x. Name the sidespin by its curve, never by the swing, or the receiver's colour key contradicts what they see.
