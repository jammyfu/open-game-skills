---
name: soak-stability
description: Leave the slice running. Ask short-hour vs overnight vs idle-resume. Look for leak, hitch growth, save rot — not for a new combo.
---

# Soak stability

Ask the column:

| Column | How long |
|---|---|
| short-hour | 1–2 hours of real verbs |
| overnight | 8+ hours, can idle |
| idle-resume | pause / tab-out / suspend then back |

## Rules

1. Fix a scene, resolution, and backend. Report memory and frame time at start, mid, end. See performance-optimization.
2. A growing heap or hitch after one hour is a soak fail even if fps started at 60.
3. Save and load every N minutes. Slot 0 must still read. See save-integrity.
4. Audio loops must not stack. See audio-feel.
5. A bot walk is soak, not a stranger-clear. Label the tape.

## Accept

Start and end memory are published. Resume after idle still accepts poll_input. No silent save wipe.
