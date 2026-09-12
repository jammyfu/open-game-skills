---
name: settings-persist
description: Generic settings save. Rebind, volume, language, look-sens. Survives a session drop.
---

# Settings persist

Ask: local-only | cloud-copy | none.
Binds (`input-design`, `kb-mouse-map`), locale (`game-localization`), and a11y flags write on confirm, not on crash.
A browser session drop must reload the last confirmed binds (`browser-input`). It must not reset difficulty or unlock flags (`debug-slate`, `save-checkpoint`).

Accept: kill the tab, come back, look-sens and language are still the player's.
