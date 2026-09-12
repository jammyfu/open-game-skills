---
name: visual-novel-ui
description: Portraits, backlog, auto-advance. Flags stay in dialogue-flags.
---

# Visual novel UI

Ask: page-click | auto-play | backlog.
`dialogue-flags` writes flags. This file owns portraits, nameplate, backlog, skip. Auto-play must be stoppable. Skip must not skip a choice (`ui-hud-focus`).

Accept: backlog replays text already seen. A choice cannot be skipped by auto.
