---
name: materials
description: Use when game materials need a shared PBR or stylized contract, texture-channel policy, compression budget, or runtime hit-flash behavior.
---

# Materials

Albedo/base color holds authored color, not baked scene lighting. Roughness, metalness and AO remain separate logical channels even when packed for a target runtime. Normal maps use one declared tangent/object-space convention; do not combine incompatible spaces.

Stylized ramps are valid when the renderer supports them. Runtime hit flash is presentation owned by the juice hook and must not replace logical damage/hit state. Prefer a parameter/multiply or documented shader path over duplicating a material per hit when that avoids needless state changes.

Compression and container format are target capabilities, not universal rules. KTX2/Basis is a strong web option when the selected renderer/loader supports the chosen transcode path; other engines may use different native formats. Publish source resolution, shipped resolution, color space, alpha convention and channel packing.

## Accept

Inspect the same asset under neutral light and verify base color contains no baked directional shadow. Decode every packed channel and compare it with the source intent. Trigger hit flash repeatedly without changing gameplay state or leaking material instances. Load the shipped texture format in the actual target adapter; unsupported compression is blocked or falls back explicitly, never assumed.
