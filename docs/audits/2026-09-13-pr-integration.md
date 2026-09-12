# PR integration checkpoint

This extends the [recovery record](2026-09-13-recovery.md); its earlier 144/154 counts describe historical checkpoints, not this merged snapshot.

The push check for `ccf91cc6347fc8b99b0ffdbbd88f379418127070` passed, but PR run `34716475585` failed `test_committed_catalog_covers_actual_skills`. The PR base had advanced to `f4d01bbf37e1ae4ffab1859c36aef94cf9bae9b5`, adding sprite-skin, art-bible, audio-buses and fps-feel after the previous synchronization.

This commit preserves those four upstream files byte-for-byte and regenerates the catalog. No freshness assertion was removed or weakened. The resulting local snapshot has **158 SKILL.md files**; **35 tests pass**, static checks report zero errors, and `git diff --check` passes. Remote push and PR-merge conclusions are reported separately in PR #1 after the checks execute.

The original per-skill semantic audit, agent behavior tests and engine/gameplay integration are still incomplete. The previously blocked Phaser enumeration edits in the two Chinese README files remain unchanged and recorded in the recovery report. Main was not directly edited by this recovery; this commit incorporates its named snapshot as a merge parent.

## Cocos integration boundary

The next PR run `34716634903` used synthetic merge `75e86c54aca833fb16f4973b4d1f42d03997b5f1`, whose actual base was `52a2e7db4b393f2f5677b9c9260e37cfe972e6a1`. Its failures were catalog freshness and the missing Cocos engine option. The branch push run `34716633058` succeeded independently.

This checkpoint imports the ten new upstream files without changing their bytes, regenerates the catalog to **168 skills**, and includes Cocos in the dispatcher's engine enumeration. Both integration failures were reproduced locally before repair. After repair, **35 tests pass** and the explicit static/catalog check reports zero errors. No test was skipped or weakened. This is a snapshot integration result, not a promise that a moving main branch cannot add further work. README engine lists remain illustrative and not exhaustive; the dispatcher and catalog are the authoritative current inventory. The blocked Chinese README writes were not retried.
