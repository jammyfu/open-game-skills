---
name: input-combo-test
description: Buttons that work alone can fail together. Ask tap-only vs move-look vs menu-vs-play vs unplug-mid. Browser and pad both need combo rows.
---

# Input combo test

Ask the column:

| Column | Pair to prove |
|---|---|
| tap-only | each verb once |
| move-look | walk + look / aim at once |
| menu-vs-play | inventory / pause does not eat attack |
| unplug-mid | pad or pointer lock drops mid-move |

## Rules

1. Phone that can walk but cannot look is a fail. See browser-input.
2. Menu open must park gameplay reads. Closing must not dump a buffered attack. See cutscene-handoff.
3. Reload and interact are different keys. Empty mag must not fire interact.
4. Two players / two pads: each pad owns one actor. See local-coop.
5. a11y hold-to-toggle is a published column, still needs the same combo rows.

## Accept

A tape shows move+look, attack then menu, menu then attack, and an unplug that recovers. Single-button greens are not enough.
