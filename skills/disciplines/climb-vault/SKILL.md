---
name: climb-vault
description: Use when characters need ledge mantle, vault, or sustained climb states with explicit geometry probes, attach/detach transitions, stamina policy, and failure recovery.
---

# Climb and vault

Choose:

| Column | Capability |
|---|---|
| mantle | short ledge transition |
| full-climb | sustained surface traversal |
| vault | cross a low authored obstacle |
| no-climb | no climb transition |

## Rules

1. Detect candidates with declared geometry evidence: reach volume, surface normal/slope, ledge clearance and destination body clearance. A visual edge alone is not a valid mantle target.
2. Attach, traverse, crest and detach are logical movement states with explicit interrupt/failure paths. Do not teleport directly from ground to roof because an animation looks correct.
3. Optional stamina/resource drain is published through `stamina-clock` or another explicit owner; running out transitions to a legal detach/fall state.
4. Physical button mapping and whether jump/interact share a control are owned by `input-design`. This skill requests semantic actions such as `jump`, `interact`, `climb` and does not mandate a physical key layout.
5. `camera-anti-clip` still validates the final camera near walls; `fall-rules` owns consequences after a failed detach.

## Accept

Test reachable/unreachable ledges, too-steep surfaces, blocked destination volume, moving geometry if supported, resource exhaustion and interruption. The actor never snaps through a blocker or becomes stuck in an attached state. Debug output shows the candidate surface, destination clearance and state transition reason.
