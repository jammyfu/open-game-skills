---
name: jump-leniency
description: Use when jumps feel unfair around ledge departure, early button presses, variable-height release, or small corner contacts and the project needs explicit forgiveness windows.
---

# Jump leniency

This skill **owns** jump forgiveness windows. `locomotion` supplies ground-transition events; `platform-jump` supplies the physical jump arc.

Choose:

| Column | Forgiveness |
|---|---|
| none | no coyote or pre-landing buffer |
| generous-platform | coyote + buffer + optional variable height/corner nudge |
| strict-arcade | authored short buffer and optional/zero coyote |

## Rules

1. Coyote and buffer are durations on the same logical clock as movement. Store durations in project data (ticks or seconds converted once to ticks). Example starting values may be tested, but there is no universal frame count or millisecond cap.
2. Coyote starts from the declared `left_ground` transition. Buffered jump records an input edge and expires deterministically; landing may consume it once according to the published phase order.
3. Variable jump height modifies upward motion through an authored cut/release rule. Holding jump does not create extra jumps unless another mechanic owns them.
4. Corner nudge/correction may resolve a small geometric near-miss but may not cross blockers, lethal boundaries or ability gates.
5. Hitstop/cancel windows are not extended by jump forgiveness. Automation may use separate allowances; do not inflate player windows to make a bot pass.

## Accept

Test immediately before/at/after coyote expiry and buffer expiry at at least two render rates. Verify one buffered press is consumed once, no stale press survives focus loss/reset, and corner correction never crosses a published blocker. Record the logical event/tick sequence rather than judging from animation alone.
