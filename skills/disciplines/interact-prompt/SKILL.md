---
name: interact-prompt
description: The world says which verb is legal. Ask context-one vs listed-verbs vs no-prompt. Context never fires an attack. Localization owns the words.
---

# Interact prompt

Ask the column:

| Column | What the HUD shows |
|---|---|
| context-one | one line for the looked-at object |
| listed-verbs | a short list |
| no-prompt | diegetic only |

## Rules

1. Priority list lives in input-design (interact > grab > talk > mount > none).
2. Prompt shows the role, then the current bind.
3. Occluded or dead targets drop the prompt. Do not steal a lock-on pip.
4. A prompt that covers a boss tell is a HUD fail.
5. Language swap uses the same glossary. See game-localization.

## Accept

A new player can name what the context key will do before they press it.
