---
name: dodge-iframe
description: Use when a dodge, roll, step, dash, or similar defensive move needs explicit invulnerability timing and attack-class eligibility rules.
---

# Dodge iframe

Choose: `none` | `roll-iframe` | `step-iframe`.

Publish a half-open invulnerability interval on the logical dodge state, plus the attack classes it ignores (for example strike/projectile/throw). Invulnerability is an **eligibility rule** evaluated by hit resolution; do not require deleting hurtbox geometry, because hurtboxes may still be needed for debug, proximity, grabs or classes the dodge does not ignore.

Direction is sampled from the project's published input point (commonly dodge activation) and may be locked or steerable according to data. Camera/mouse look changes direction only when the selected control scheme says so. Resource cost belongs to `stamina-clock`.

Parry timing belongs to `parry-guard`, not this skill.

## Accept

Draw the dodge interval and eligibility mask on the logical clock. Test contact immediately before, at the start, at the end and immediately after the interval for every relevant attack class. A late dodge remains hittable; changing render FPS does not move the eligibility boundaries.
