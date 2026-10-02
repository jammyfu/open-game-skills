---
name: avatar-create
description: Use when a character creator needs stable part, slider/morph or hotspot identities, save/load compatibility, rig/socket constraints, cosmetic ownership and explicit separation from gameplay-affecting body rules.
---

# Avatar create

## Compatible modes

`part-kit` | `slider-morph` | `hotspot-sculpt`

The project may combine modes when ownership and serialization are explicit.

## Creator schema

Persist **stable** IDs/values rather than visible labels or array indices:

```text
creator schema/version
base/body preset ID when applicable
part/cosmetic IDs + slots
slider/morph semantic IDs + values
material/colour IDs or normalized values
rig/body compatibility tags
random seed when randomisation must reproduce
```

`save-systems` owns migration/atomic persistence. `character-rig` owns skeleton/sockets; `face-morph` owns facial channel schema; `game-monetization`/entitlements own paid/unlocked access.

## Rules

1. Creator state must **save** and reload/migrate by stable identity across reordered catalogs where supported.
2. Parts/sliders respect declared **rig**, socket, clipping, LOD and animation compatibility. Invalid combinations are rejected, constrained or supplied a documented fallback.
3. Cosmetic presentation does not silently change hitboxes, cancel windows, movement or other **gameplay**. If body morphology is gameplay-affecting, a separate explicit gameplay/body/collision contract owns it.
4. Availability/unlock policy is project/economy data; do not assume body identity is always free/up-front or wardrobe always unlocks later.
5. Randomisation and presets use stable IDs/seed when reproducibility matters and do not produce unsupported combinations.
6. Proportion sliders (height, head-to-body ratio, limb length) declare which regions stay rigid (head, face texture, sockets) and how the rest maps. Lengthening without matching width/thickness rules gives implausible bodies. Validate each slider at both ends of its range across LOD tiers for rig/socket fit, clipping and triangle/memory budget. Adapt resolution or LOD where the budget would otherwise be exceeded.
7. Preset values derived from other parameters, such as proportion from height, come from a documented, versioned function of stable inputs. Saves store either the resolved values or the inputs plus the derivation version.

## Accept

Save/load several materially different creators, reorder a test catalog/schema migration, exercise incompatible part/rig cases, and build every proportion slider at its range ends on each LOD tier. Stable identities reconstruct the intended avatar or a documented fallback, while cosmetic-only changes leave gameplay contracts unchanged.
