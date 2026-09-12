---
name: restore-purchase
description: Restore and re-grant on a new device. Use for 恢复购买, 换机到账.
---

# Restore purchase

Ask first: store-restore button, silent on login, or both?

Rules: restore writes the entitlement slot, not the story slot (`save-integrity`, `entitlement-grant`). Settings stay in `settings-persist`. A failed store session is setup, not a wipe. Do not consume a one-time pack twice.

Accept: after restore, the player can name what came back. A lab unlock does not ride along.
