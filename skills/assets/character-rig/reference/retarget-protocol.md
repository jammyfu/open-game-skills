# Reusable motion and retarget protocol

This extends the rig contract, not gameplay timing ownership. Cross-rig compatibility is a tested mapping, never a promise that every model accepts every clip.

## Mapping record

Record source/target asset and skeleton hashes, importer/version, unit conversion, rest-pose basis, semantic bone mapping, required chains, optional joints/fallback markers, translation-scaling policy, handedness/facing, sockets and skin/morph preservation. Bone names alone are insufficient: verify hierarchy and local bind/rest orientation. Resolve duplicate/ambiguous names explicitly. Non-humanoids need their own semantic profile; do not coerce a quadruped into a human map.

Map pelvis versus locomotion root separately. Preserve twist distribution and joint limits where supported; do not copy local rotations blindly between differing rest poses. Use neutral pose plus left/right single-limb motions to expose mirroring before testing a whole dance or attack.

## Root displacement policy

Every clip declares in-place, extracted root motion, or another explicitly owned policy. Publish source root path, axes used, world conversion, displacement application owner and loop-wrap/reset behavior. `animation-graph` composes root contributions; `locomotion`/`physics-interaction` apply the agreed displacement once. Never add both extracted root displacement and an independently integrated full locomotion displacement for the same action.

Separate **desired displacement** from collision-resolved displacement and rendered pose. A wall may prevent movement despite a clip continuing. Reconcile presentation through the project's supported controller/animation technique rather than teleporting collision to the animated foot. Changing clip speed or duration must not silently move hit/cancel windows; gameplay owners authorize any timing change.

## Contact and motion probes

Use a small reusable clip set: idle, forward walk, turn, stop, jump/land and one representative attack. Test available sockets and extreme poses, short/tall proportions, optional toes absent, loop wrap, interruption, pause and actor-local hitstop.

Record at the project's update boundary: root height/facing, desired and resolved displacement, left/right contact intervals, planted-foot drift relative to the moving support surface, penetration distance and required socket error. Publish per-project tolerances and units before scoring. Moving platforms require support-relative measurements; camera motion is not foot drift. No universal centimeter limit proves a convincing character.

Keep clip and skeleton hashes with results. A passing static map is not a passing deformation, root-motion or foot-contact test. Missing source rights, rest-pose data or required joint chains blocks that clip/rig pair; optional joints use a declared fallback. Preserve source assets and write retargeted variants separately.

## Primary references

[Godot retargeting](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html) and [AnimationTree root motion](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html) describe adapter-specific mechanisms. Verify the installed engine version; this protocol does not claim those APIs exist in every runtime.
