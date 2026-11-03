# Drift-kart feel kit

Load this only when `racing-feel` resolves to `drift-kart` (or a hybrid that names drift/boost pieces) and the request is about speed sense, drift depth or boost layering. Everything below is a **genre mechanic or tuning seed**, not a rule of any named game. Borrow mechanics; never copy a franchise's track, item, character, symbol, sound or proprietary term (HUD labels included).

## 1. Audit before tuning

Record, from the running project, before changing anything:

| Probe | What to look for |
|---|---|
| Drift state | Is drift only "hold = less grip, release = boost ∝ charge"? Is direction locked? Does steering inside a drift change the arc? |
| Boost sources | Which events grant boost (drift, pads, start, draft, trick)? One shared boost state or several? Does a refresh extend or restart? |
| Boost ceiling | Is the overshoot a fixed m/s or a fraction of the class top speed? Fixed m/s vanishes at high speed classes. |
| Camera | Is FOV mapped from absolute speed or from the class/handling top speed? Does boost snap FOV on/off or ease in/out? |
| Audio | Is there a continuous engine voice whose pitch follows speed? Is a speed-class pitch field defined but unread? |
| Presentation truth | Do sparks/HUD/audio read the same tier number that the handling step uses, or guess from thresholds? |
| Cancels | Does a stun/hit/spin that ends a drift still pay out its boost? |

Unread config fields, presentation-only guesses and payouts on cancel are the common defects.

## 2. Drift contract (handling owner)

1. **Entry gate**: drift input + minimum forward speed + steer beyond a threshold. Entry locks a direction (±1).
2. **Locked arc**: while drifting, stick input modulates the arc instead of choosing a side: outer → wide, neutral → base, inner → tight. Neutral keeps turning toward the locked side.
3. **Charge by line**: charge rate scales with how far the stick points into the drift, so the tight line is rewarded.
4. **Tiers**: authored ascending `{charge, boostSeconds}` entries. The handling step owns the tier number; presentation (spark color, HUD bar, tier-up chime) reads that number.
5. **Payout** only on voluntary release above tier 1. Speed loss below the gate or a stun/hit cancels without payout.
6. Keep a legacy path when older handling data omits the new fields, so existing replays and tests do not silently change.

## 3. Boost layering

| Source | Trigger (seed) | Notes |
|---|---|---|
| Drift tier | release at tier 1/2/3 | longer, not stronger, per tier is the simplest readable ladder |
| Launch timing | throttle held from a window before GO | too early = short stall; mid-countdown release resets |
| Slipstream | stay inside a wake cone behind a same-heading rival | same rule for every racer; rank-dependent strength belongs to `racing-design` |
| Ramp trick | press jump in a short window after a lip launch | pays on landing; jumping on the ramp face counts |
| Pads | surface zone | already a surface modifier; just share the boost presentation |

Rules: one boost state, refreshes take the maximum remaining time, and the overshoot ceiling is a fraction of the current class top speed. Presentation treats "remaining time increased" as a boost event, so refreshes also get the cue.

## 4. Speed readability stack (presentation only)

None of these may write logical velocity.

- **FOV** maps from `speed / class top speed`, plus an eased boost kick (fast attack, slow release) and a short punch for large gains (perfect start, top tier).
- **Camera rig** pulls back with speed and boost (in vehicle-length units), and blends its yaw part-way toward the travel direction so a drift visibly slides sideways.
- **Micro-shake** at near-top speed, accumulated per step like surface rumble, normalized by viewport height, and zero under reduced motion.
- **Wind/speed lines** thicken with speed, boost and slipstream wake. Label boost pulses by source.
- **Engine voice**: within each gear, pitch climbs from slightly below the previous gear's peak to this gear's peak, so the overall envelope rises with speed and drops a little at each shift. Boost lifts the pitch, the class adds a pitch offset, and the voice has one owner, one instance and a release on mute or dispose.
- **Drift entry hop**: a presentation-only bounce derived from the first slice of charge, which keeps it stateless and replay-identical.

## 5. Tuning seeds (one shipped kart project; re-measure yours)

| Value | Seed |
|---|---|
| Tiers (charge / boost s) | 0.30/0.50, 0.65/0.95, 1.00/1.50 with charge rate ≈0.72/s |
| Arc factors outer / neutral / inner | 0.40 / 0.75 / 1.30 × steering rate |
| Boost overshoot | +22–25% of class top speed |
| Launch windows | perfect 0.95–0.30 s before GO → 1.2 s, later → 0.6 s, earlier than 1.5 s → 0.8 s stall |
| Slipstream | 1.8–13 m ahead, ±1.5 m, ≥55% top speed, 1.4 s to fill → 0.9 s |
| Trick | 0.45 s window → 0.7 s |
| Camera | FOV 46→62 + 7 boost + 5 punch; kick attack 10/s, release 2.2/s; pull-back 0.35 m speed + 0.5 m boost; travel-yaw blend 0.35 |

## 6. Accept

- Replay the same input → identical drift direction, tier, boost time and position.
- Tier boost durations strictly increase. Release below tier 1, a cancel or a speed-drop exit pays nothing.
- Boost FOV/kick: attack faster than release. Reduced motion → base FOV and no shake.
- Slipstream: a follower charges, the leader does not; beside, opposite-heading, too-far and too-slow cases do not charge.
- Launch: windows map to perfect/good/none/stall; AI outcome is a stable function of racer id.
- Term audit: HUD/audio/item labels use the project's own vocabulary.
- Report what was verified at runtime (browser lap, screenshots) separately from unit tests. Feel itself still needs a human playtest; label it not-run until one happens.
