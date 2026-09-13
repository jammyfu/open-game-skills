---
name: ik-foot-locking
description: Use when rendered feet need contact locking or terrain adaptation after locomotion/animation, including varied skeleton joints, slopes, stairs and moving surfaces without making IK the gameplay movement owner.
---

# IK foot locking

IK is a **presentation pose correction** after the authoritative root/body movement and source animation pose.

## Contact schema

Select an available contact marker: toe when present/useful, otherwise a **foot/ankle** marker or project-defined sole/contact point. Do not require a toe joint on every rig.

Contact detection may combine relative velocity, height/distance, animation phase and ground probe with authored hysteresis/debounce. Thresholds and durations are project/scale data.

For a **moving** or rotating support, store the lock anchor in support-local or otherwise stable reference space and evaluate actor/contact motion **relative** to that surface so the foot follows it without world-space skating.

## Rules

1. `locomotion`/physics owns root movement; IK edits leg/foot pose and never fabricates grounding/gameplay collision.
2. Lock point/joint is chosen from the rig/contact schema, not universally toe-vs-heel.
3. Leg extension is clamped to an anatomical/rig range. Optional **pelvis** compensation may be used when authored, bounded and presentation-only; it is not universally forbidden or required.
4. Contact enter/exit hysteresis prevents noisy pops, but no universal 3–5 frame vote is imposed.
5. Ground/support data comes from explicit probes/contacts, never an assumed world Y=0.
6. Blend/inertialisation keeps lock transitions continuous and avoids averaging unrelated world-space targets.

## Accept

Test stationary and moving/rotating supports, slopes/stairs, missing-toe rigs, reach limits and unlock transitions. Record contact marker, support ID/reference, lock error and pelvis adjustment where used; acceptance tolerance is authored for rig scale rather than a universal 1 cm.
