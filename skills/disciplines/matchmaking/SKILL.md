---
name: matchmaking
description: Use when players or parties need to enter a local/online/private/ranked pool with explicit ticket identity, compatibility constraints and deterministic match assignment separate from netcode and gameplay balance.
---

# Matchmaking

Ask the queue model: casual, ranked, private, local-only, custom, or existing.

## Contract

Publish:
- stable `match_ticket_id` and request revision
- stable `match_ruleset_id` and revision
- party/member IDs if grouped
- explicit `compatibility predicate` (build/protocol/region/input/policy as applicable)
- ranking/search expansion policy where used
- cancellation/timeout/retry semantics
- assigned match/session identity

## Ownership

This skill owns queue/ticket lifecycle and compatible assignment. `netcode-feel` owns transport/prediction, balance systems own gameplay tuning, and party/local-coop systems own member identity before ticket creation.

## Rules

1. Enqueue, cancel and assignment callbacks are idempotent by ticket/request identity.
2. Ranking, skill estimates, input segmentation, region widening and queue-time tradeoffs are project policies; none are universally required or forbidden.
3. The same compatibility revision cannot silently pair clients that fail its published predicate.
4. Queue delays and assignment failures are setup/service evidence, not permission to mutate gameplay rules.
5. Private/direct matching uses stable room/session identity and explicit access policy rather than display names.

## Acceptance

A reviewer can trace one `match_ticket_id` from enqueue through cancel/timeout/assignment, identify the `match_ruleset_id` and compatibility predicate, and show that duplicate callbacks do not create multiple matches or silently change gameplay policy.
