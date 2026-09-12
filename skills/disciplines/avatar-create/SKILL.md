---
name: avatar-create
description: Character maker columns. Part-kit, sliders, or hotspots. Cosmetics do not change hurtboxes.
---

# Avatar create

Ask: part-kit | slider-morph | hotspot-sculpt.

| Column | How the face changes |
|---|---|
| part-kit | swap eyes / hair / mouth from a authored set (Mii-like) |
| slider-morph | blendshape or bone pose weights |
| hotspot-sculpt | drag on the mesh; maps to morphs under the hood |

Parts are paint (`sprite-skin`, `art-bible`). The logic body and sockets stay `character-rig` / `hitbox-hurtbox`. A paid hat is cosmetic (`game-monetization`).
Identity (skin, body) is available up front. Wardrobe can unlock later. Do not ship a slider that breaks the rig toe or weapon socket.
Public refs to study, not to copy assets: Mii part lists, Sims hotspot talk, Ready Player Me / VRM / ARKit morph names, MakeHuman/MPFB, TalkingHead visemes.

Accept: three saved faces load on the same rig. Hitboxes and cancel windows do not change.
