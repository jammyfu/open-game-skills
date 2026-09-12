---
name: move-tell
description: Startup must be readable. Ask pose-audio vs color-flash vs both vs none. Flash-only fails if a11y flash-off is on. Tells live on the move, not in juice.
---

# Move tell

Ask the column:

| Column | How the player reads startup |
|---|---|
| pose-audio | body + sfx |
| color-flash | extra color / line |
| both | pose plus a published mark |
| none | only for player pokes under 8f |

## Rules

1. Enemy heavies and grabs need a tell longer than a human tap. See enemy-kit-balance.
2. Color-flash is juice. Pose-audio must still work with juice off.
3. A tell that covers the whole screen is a HUD fail.
4. Fake tells that never attack teach the player to ignore tells.
5. Same logic frame as the startup frame. Late VFX is not a tell.

## Accept

A new player can say "that one is the slam" after two rooms. Flash-off still leaves the slam readable.
