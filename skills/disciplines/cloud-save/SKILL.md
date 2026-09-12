---
name: cloud-save
description: Cross-device progress. Slots follow save-integrity. Use for 云存档, 换机.
---

# Cloud save

Ask first: single slot, conflict prompt, or last-write?

Columns: one-slot | prompt-conflict | last-write-wins.

Rules: story slot and lab slot stay separate (`save-integrity`). Settings travel with `settings-persist`, not mixed into the story blob. A failed sync is a setup failure, not a wipe. Debug unlocks do not upload as natural clears.

Accept: two devices can explain which slot won. A conflict never silently deletes the longer playtime.
