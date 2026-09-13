---
name: move-tell
description: Use when an existing integration requests the legacy move-tell entry or pose-audio, color-flash, both, or none modes and the request must map to the canonical attack warning contract.
---

# Move tell compatibility entry

This is a **compatibility entry**. [attack-tell](../attack-tell/SKILL.md) owns warning timing, channel availability, accessibility and activation-boundary evidence.

## Legacy mapping

| Legacy mode | Canonical handling |
|---|---|
| pose-audio | `attack-tell`: pose-audio |
| color-flash | `attack-tell`: color-flash as an authored additional/eligible channel |
| both | `attack-tell`: use the project's required multi-channel warning policy |
| none | no warning contract is requested for this move; invalid if another project rule requires one |

Do not keep a second frame threshold, “human reaction” constant, tell duration, screen-coverage rule or move-class policy here. Move balance stays with its design owner and logical activation stays with `action-feel`/the move state.

## Accept

The legacy mode resolves to `attack-tell` or an explicit no-warning project decision, with no duplicated timing/accessibility rules in this alias.
