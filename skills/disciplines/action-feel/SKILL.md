---
name: action-feel
description: Use when attacks feel floaty, cancels fire illegally, hitstop freezes unrelated actors, or combat outcomes change with render rate or same-tick processing order.
---

# Action feel

Choose the project column before tuning numbers. Studio labels are examples, not rules.

| Column | Buffer | Cancel | Hitstop | Turn |
|---|---|---|---|---|
| short-special | short attack buffer | on-hit into named specials | authored per contact | snap on startup if published |
| long-cancel | longer command buffer | named on-hit/jump/ranged edges | authored rhythm/weight | optional inertia carry |
| commit-whitelist | anti-misinput buffer | named follow-ups only | authored weight | limited during commitment |
| coyote-platformer | jump buffer + coyote | only published attack/jump edges | tiny or none | published air control |

Do not combine columns implicitly. Persist the selected values in project data.

## Logical clock and phase order

Publish the logical tick rate; render FPS is never the combat clock. Engine adapters provide input, pose, contact-query and presentation hooks, but gameplay owns ordering.

A deterministic default phase is:

1. sample input into the input ring;
2. update clocks that are not frozen and resolve legal state/cancel transitions;
3. snapshot active hit/grab volumes and collect contact candidates;
4. resolve same-tick contacts using the published trade/priority rule and stable IDs;
5. apply damage, reaction, hitstop and queued launch state;
6. emit presentation events after logical results are known.

A project may choose another order, but it must publish it and regression-test same-tick cases.

Every contact carries a stable attack/hit instance identity. A target is hit at most once by one hit instance unless the move explicitly schedules separate multi-hit indices. Container iteration order must not decide who wins a trade.

Hitstop freezes only the actor clocks named by the resolved event. Input sampling, unrelated actors and the world keep running unless a different pause system explicitly owns them. Projectiles or hazards without an actor clock are not accidentally frozen because two actors touched.

## Charge and cancel ownership

Publish charge start → full → hold-cost → release → cancel. Interruption, weapon swap and focus loss must restore a legal state.

Cancels are directed edges plus windows and conditions. Motion commands are stepwise sequences with explicit timing windows, not an unordered bag of recent inputs.

## Accept

Replay the same input/contact trace at different render rates and with reversed entity iteration order. Move starts, legal cancels, contact IDs, trades, hitstop ownership and resulting states must match. Freeze A/B and verify unrelated C still advances. Record which scenarios actually ran; a timing table alone is not runtime evidence.
