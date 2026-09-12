---
name: materials
description: Generic material contract — PBR vs stylized ramps, no lighting baked into albedo, packed ORM, runtime flash hook.
---

# Materials

Albedo holds color, not shadows. Roughness / metal / AO are separate or packed ORM.
Normal maps stay in one space. Do not stack two tangent spaces.
Stylized ramps are legal; they must share the same flash/hit color the juice hook uses.
Web prefers KTX2 / Basis. Do not ship 4k maps on a 2m prop.
Hit flash is a runtime multiply, not a second material swap if you can avoid the draw-call break.
