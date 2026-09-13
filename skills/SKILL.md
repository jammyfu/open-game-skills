---
name: open-game-skills
description: Use when a game task should be routed through this pack's engine-neutral disciplines, shared execution contract and engine adapters without loading the whole catalog.
---

# open-game-skills

This is the pack entry point, not a second dispatcher.

## Flow

1. Read [the shared contract](CONTRACT.md) once for the current task/session.
2. Delegate routing to [dispatcher](dispatcher/SKILL.md). Preserve explicit project engine, modes and existing architectural choices unless the user asks to change them.
3. Load only the selected skill bodies for the current phase; keep deferred work named rather than silently expanding scope.
4. Execute the work, run the relevant deterministic/static checks, and distinguish real runtime/model/human evidence from checks that were not run.
5. Continue deferred phases only when they become active.

The [catalog](catalog.json) is discovery data. Do not dump it into every prompt or treat catalog order as priority. Keep the complete pack together when installed so bundled references remain resolvable.

## Ownership

- `open-game-skills` owns pack entry/discovery only.
- `dispatcher` owns routing policy.
- discipline skills own domain contracts.
- engine adapters own engine-specific mapping.
- `gameplay-validation` / `game-qa` own what runtime evidence may prove.

## Acceptance

A request entering through this file resolves through the same dispatcher decision as a direct dispatcher request, does not overwrite explicit project choices, loads only the bounded skill set needed for the active phase, and reports unrun behavior as unrun rather than inferring success from pack CI.
