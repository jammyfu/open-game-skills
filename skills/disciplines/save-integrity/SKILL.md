---
name: save-integrity
description: >
  Progress flags, debug unlocks, and capture sessions must not silently
  rewrite a player's story save. Use when a clip flipped difficulty or
  when a lab slot leaked into slot 0.
---

# Save integrity

## Trigger

Training, capture, or debug-slate can write flags that look like progress.

## Mode

| Column | What the file may hold |
|---|---|
| story-slot | natural unlocks only |
| lab-slot | dummy, flags, items; never the default slot |
| capture-slot | a snapshot labeled with cheats |
| settings-only | remap / language / volume — not progress |

settings-persist is settings-only. save-checkpoint picks *where* you respawn. This skill owns *which file is allowed to lie*.

## Procedure

1. Name the slot before any cheat.
2. Teleport, wipe, force phase, or flip an unlock writes capture-slot or lab-slot.
3. Exporting a clip copies the slot label into gameplay-capture's title card.
4. Copying lab → story is a published debug action with a confirm, not an autosave.

## Constraints

- A story-slot clear with lab flags is invalid evidence (gameplay-validation).
- Difficulty override lives beside the save, not inside the same silent bit as "door opened".
- Cloud sync must not merge lab flags into story without a prompt.

## Accept

After a debug session, slot 0 still has the last *natural* flags. A clip that used an override says so on disk.
