---
name: character-rig
description: Use when character skeletons, rest poses, axes, sockets, or IK contact points must be standardized across assets or engine adapters.
---

# Character rig

Publish a canonical **asset-space** skeleton contract; engine adapters own any runtime conversion.

Minimum humanoid chain: pelvis, spine, neck/head, clavicle, upperArm, lowerArm, hand, thigh, shin, foot. Extra spine joints, twist bones and toe/ball joints are capabilities, not universal requirements. A foot-lock implementation may target a toe/ball joint when present, otherwise a published foot/ankle contact marker. Do not silently invent a missing joint in runtime code.

Bind in a documented rest pose with a documented forward/up convention. Keep left/right naming deterministic. Sockets such as `weapon_r`, `weapon_l`, `bow`, `camera_pivot` and `hit_flash` are optional published attachments; consumers must declare which are required.

The exported rig records scale/unit metadata and facing. Importers may convert once at the adapter boundary; do not hide repeated 90°/180° or scale corrections in gameplay code.

## Accept

Retarget a neutral locomotion clip and verify left/right limbs, root height and facing. Attach every required socket and confirm it survives export/import. Test a rig both with and without toe joints when foot locking is supported; missing optional joints must degrade through the declared fallback rather than disabling the whole character.
