---
name: aim-assist
description: Stick or mouse help onto a target. Ask off vs friction vs rotation vs magnet. Publish the help. Magnet that finishes a combo belongs only to lock-on-brawler.
---

# Aim assist

Ask the column:

| Column | What it does |
|---|---|
| off | raw look |
| friction | slow the stick on target |
| rotation | steer toward target while firing |
| magnet | snap inside a small cone |

## Rules

1. Assist is a look modifier. It does not grow hitboxes.
2. Mouse and stick may use different columns. Matchmaking should not hide that. See matchmaking.
3. ADS look is slower than hip look. That split is data, not a secret.
4. Occluded or dead targets drop assist the same frame lock-on would drop.
5. a11y aim-help is the same table with a published larger cone. It still cannot change damage.

## Accept

Player can name whether the stick is raw. A bullet that hits only because the box grew is a hitbox bug, not assist.
