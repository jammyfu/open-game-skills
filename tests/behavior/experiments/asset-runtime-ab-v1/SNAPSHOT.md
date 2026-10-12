# Historical Skill input

`plan.json` is unchanged. Its asset-runtime source pin is still
`5d6f28a1526cdfe0718c4fe26eae0a3403ee9e7e8cbf3426534bacc17b0c06fc`.
The production Skill evolved after this preregistration. The exact original
bytes, recovered from repository base `8051a36b44e38d641db2bd6fc15314468bc86234`,
are stored as `asset-runtime.skill-snapshot.txt` so v1 remains reproducible.

The runner prefers this archive for this one Skill input, checks the original
hash and records the actual `source_locations` in newly collected metadata.
A corrupt or symlinked archive is rejected, not bypassed with a live file.
Without the archive, only a live file matching the old pin is accepted.
All non-Skill input drift still blocks. The task, oracle, model, budget,
conditions, planned sample IDs, source hashes and historical results are not
changed. A v1 result concerns the frozen guidance, never the current Skill.
Testing the expanded Skill requires a new preregistration and new observations.

This archive is input data, not an additional installed Skill or a new LLM run.
