---
name: hitbox-hurtbox
description: >
  Engine-neutral strike and receive volumes. Use when hits miss the eye,
  when the mesh is the collider, or when a cinematic frame has a secret
  box. Stacks on action-feel. Ask the column first.
---

# Hitbox / hurtbox

Ask the column.

| Column | Strike volume | Receive volume |
|---|---|---|
| sprite-box | 2D boxes on frames | 2D boxes on frames |
| capsule-3d | capsules / spheres per limb | body capsule + head |
| melee-arc | swept volume this frame | same receive |
| projectile-orb | small sphere + lifetime | same receive |
| grab-range | throw box, not strike | throw-hurt distinct |

Render mesh is never the combat collider.

## Clock

Boxes exist on the **logic tick**. A strike box is on for N frames published in the move row.
Hitstop freezes both actors' boxes; it does not spawn a new box on a render frame.
Clash / trade: if two strike boxes overlap and both hurtboxes are valid, both hit, unless the column is single-winner (first tick wins).

## Readability

- Active frames that kill must be visible as motion, not only as a box in debug.
- Debug draw is a develop toggle. Players see silhouette and juice, not the box.
- Whiff: strike on, hurtbox of target not overlapped. Cancel rules live in combo-design.
- Grab box is a different color in debug and a different job in kb-mouse-map. It does not hit-confirm into a punch.

## Iron rules

- No unseen box on a cinematic freeze unless boss-design published the freeze.
- Hurtbox may shrink on dodge / block. It may not vanish for 20 frames without a pose.
- Projectiles inherit the same clock. They do not hit on interpolation frames only.
- Throw invuln and strike invuln are separate flags.

## Accept

A poke that looks short is short. A spectator can tell a whiff from a hit without the debug overlay. A grab does not connect from a punch box.
