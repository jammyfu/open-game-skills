---
name: genre-route
description: Use when a request names a broad game genre or hybrid genre and needs a small starting set of disciplines before canonical dispatcher routing resolves the actual project modes.
---

# Genre route

This is a heuristic hint layer, not a second dispatcher and not a genre rulebook.

## Contract

Publish:
- the user's genre phrase(s)
- optional `genre_profile_id` / revision when the project maintains one
- candidate discipline hints with a short reason
- project facts that override the generic hint
- unresolved choices that must return to `dispatcher`

## Suggested starting hints

Examples are defaults, not requirements:

| Genre phrase | Candidate disciplines |
|---|---|
| 2D platform | `platform-jump`, `jump-leniency`, `level-teach` |
| fighter | `fighting-design`, `action-feel`, `input-design` |
| character action | `action-feel`, `lock-on-target`, `combo-design` |
| open world | `world-map`, `world-streaming`, `ability-gate` |
| FPS / shooter | `projectile-hitscan`, `aim-assist`, `fps-feel` |
| stealth | `enemy-perception`, `stealth-info`, optionally `tactics-stealth` |
| deck / card | `deck-build`, `rng-seed`, `ui-hud-focus` |
| 2D skeletal | `spine-skeletal` plus the chosen engine adapter |

Hybrid genres may combine or replace these hints. Existing project architecture, mechanics and explicit user choices outrank the table.

## Ownership

`genre-route` only proposes candidate disciplines. `dispatcher` owns the final bounded USE / ENGINE / ASK / DEFER decision and its active-skill budget. Studio-style presets remain with `studio-columns` / compatibility aliases.

## Acceptance

The same explicit project facts produce the same final dispatcher decision whether the user supplied a genre label or directly named the mechanics. Genre hints never overwrite an existing engine, mode or implemented system merely to match a stereotyped genre recipe.
