---
name: moving-platform
description: Use when riders must stay stable on moving geometry, preserve or discard platform-relative velocity on departure, or handle lifts and crush contacts deterministically.
---

# Moving platform

Choose the carry/transfer policy:

| Column | Grounded carry | Departure transfer |
|---|---|---|
| stick-carry | full platform pose delta | published world/relative velocity rule |
| loose-carry | partial authored carry | published transfer factor |
| one-shot-lift | constrained rider policy | authored exit rule |
| crush-safe | any carry policy | explicit stop/yield/damage response |

## Reference frames and order

1. Sample platform previous/current logical transforms and derive platform point velocity/delta for the rider contact point.
2. Grounded rider movement is solved in a declared platform-relative or world-space convention exactly once. Do not both carry by transform delta and add the same platform velocity again.
3. On jump/detach, convert the rider's relative motion to world motion using the published transfer policy. Whether platform velocity is inherited fully, partially or not at all is data, not a universal exception for one lift type.
4. `jump-leniency` owns coyote after support is lost. `platform-jump` owns jump arc. `locomotion` owns rider movement integration.
5. Moving collision geometry, navigation/leashes and `camera-anti-clip` must observe a compatible platform pose for the same logical frame.
6. Crush behavior is explicit: stop/yield, authored damage/kill with telegraph, or another declared response. Silent interpenetration is invalid.

## Accept

Stand, walk, jump and re-land on platforms moving horizontally, vertically and with the supported rotation policy. Reverse update iteration and vary render rate; grounded relative offset and departure velocity remain consistent. Test support loss near coyote boundaries and a closing/crush case without double-applying platform velocity.
