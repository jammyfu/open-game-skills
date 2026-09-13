---
name: cert-handoff
description: Use when platform or operating-system lifecycle events such as suspend/resume, input-device loss, storage failure, sign-in changes, overlays, or similar certification-relevant interruptions need explicit recovery contracts.
---

# Cert handoff

This skill owns lifecycle handoff behavior, not a copied vendor checklist. Current first-party/vendor requirements must come from the project's authorized, versioned sources.

## Event contract

For every applicable event publish:

```text
event id + source
precondition / active game state
state that must persist
input policy during interruption
resume/recovery state
failure/fallback path
evidence required by game-qa
```

Examples include suspend-resume, focus/overlay transitions, controller or primary input loss, storage/save failure and account/session changes.

## Rules

1. Resume clears or reconciles held/edge-triggered input according to `input-design` / engine lifecycle so stale input is not replayed accidentally.
2. Device loss follows a **project policy**: pause, prompt for reassignment, continue with another valid device, or another declared behavior. It is not universally “open a menu.”
3. Corrupt or unavailable saves follow `save-integrity` / `save-systems`; do not overwrite other valid slots while recovering.
4. Platform capability differences live in `platform-targets` and engine adapters.
5. Every handoff scenario is a named `game-qa` interrupt/combination case on the relevant target. Passing one target does not prove another.

## Accept

Each applicable interrupt has an observable legal recovery or fallback, no stale input fires on resume, persisted state follows its owner, and evidence names the exact build and platform target.
