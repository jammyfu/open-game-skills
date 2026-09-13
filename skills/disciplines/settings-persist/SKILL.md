---
name: settings-persist
description: Use when confirmed control, audio, language, camera, graphics, or accessibility preferences must survive restart, crash, browser termination, migration, or optional cloud copy.
---

# Settings persist

Settings are versioned preferences, not story progress.

## Modes

| Mode | Storage |
|---|---|
| local-only | device/browser local persistence |
| cloud-copy | local committed settings plus account-scoped cloud copy |
| none | session-only; persistence intentionally disabled |

## Contract

Persist a small `settings_schema_version` plus only confirmed values. Editing UI may keep a draft, but the durable record changes at the published apply/confirm boundary. Unknown keys are handled by an explicit forward-compatibility policy; renamed/removed fields migrate without resetting unrelated preferences.

Use an atomic write/replace mechanism appropriate to the platform. If persistence fails, keep the previous confirmed record and report/retry; never replace it with a partial draft.

Bindings (`input-design`, `kb-mouse-map`), locale (`game-localization`) and accessibility settings keep their domain owners. This skill owns persistence and migration only. Story difficulty/unlocks do not live here unless they are explicitly preferences rather than progression.

## Acceptance

Confirm settings, kill the process/tab during the next write, restart, migrate an older schema, and simulate a malformed settings file. The last confirmed valid values survive or a documented default/recovery path is used. A cancelled draft never becomes durable state.
