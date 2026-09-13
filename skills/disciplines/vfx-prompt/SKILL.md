---
name: vfx-prompt
description: Use when an existing integration requests vfx-prompt for a game effect sheet or generation brief.
---

# VFX prompt compatibility entry

Delegate generation and acceptance to [vfx-generate](../../assets/vfx-generate/SKILL.md). It is the sole owner of the effect modes and provider capability checks. Use its [bundled prompts](../../references/vfx-image-prompts.md) as examples, not executable API parameters.

Legacy mode aliases: guard-break → shield-break; dash-trail → trail-streak; jump-puff → foot-puff; cast-circle → summon-circle. Preserve direction, timing intent and style while translating. teleport-in and teleport-out remain distinct modes; do not collapse assembly and dissolution. All other supported modes retain their names.

Do not maintain a second effect table or invent a model identifier. This compatibility entry replaces, rather than adds to, the active generator skill slot.

## Accept

A legacy prompt request resolves to `vfx-generate` with the translated mode, actual provider/output constraints and the same measured acceptance checks. This alias adds no second generator ruleset.
