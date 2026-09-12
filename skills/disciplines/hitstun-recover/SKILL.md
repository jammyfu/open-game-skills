---
name: hitstun-recover
description: Use when hitstun, blockstun, frame advantage, knockdown recovery or a suspected infinite combo needs an explicit timing contract.
---

# Hitstun and recover

Resolve the column from the project before tuning:

| Column | After the hit |
|---|---|
| none | flinch presentation, no action lock |
| light-stun | timed action lock, then legal actions |
| knockdown | downed state plus authored wakeup options |
| juggle | airborne state with explicit landing and escape rules |

Hitstop and hitstun are different. Under [action-feel](../action-feel/SKILL.md), each affected actor pauses its move clock during hitstop while simulation input sampling continues. Count that actor's remaining stun or recovery on its advancing ticks, not render frames. Publish exceptions for asymmetric hitstop or other clock policies.

## Timing contract

Record hitstop per participant, hitstun, blockstun, remaining active/recovery at impact, knockdown duration and wakeup invulnerability. Use half-open intervals `[start, end)` and a declared logical frequency. Do not assume wakeup invulnerability or blockstun shorter than hitstun for every design.

Frame advantage = victim first-action tick minus attacker first-action tick, measured on the same global simulation timeline. Positive means the attacker can act first. Only with equal freezes and matching interval conventions can this simplify to stun minus the attacker's remaining commitment at impact; total move recovery alone can miss remaining active frames.

Positive advantage is not proof of a true combo or an infinite. Also check follow-up startup, walk-in time, range, cancel conditions, target state and escape options. Resolve simultaneous contact/action boundaries with the project's explicit priority rule.

Example: an attacker is free at tick 108, the victim at 116, but the next attack first contacts at 120. The attacker has eight ticks of advantage and still leaves a four-tick gap:

```json
{
  "attacker_first_action_tick": 108,
  "victim_first_action_tick": 116,
  "followup_first_contact_tick": 120,
  "advantage_ticks": 8,
  "gap_ticks": 4
}
```

An infinite requires a repeatable route with no escape or terminating resource/state condition; one inequality or damage scaling alone does not establish that.

## Accept

Log both first-action ticks, follow-up contact and the defender's earliest legal reply. Test a true link, a gap, a whiff, asymmetric hitstop, knockdown and recovery after interruption. Turning visual effects off must not change the counts. Document which scenarios ran; arithmetic/documentation checks alone do not prove engine behavior.
