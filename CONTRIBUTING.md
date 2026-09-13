# Contributing and recovery

Use Python 3.10+; CI verifies Python 3.12. This is a skill pack, not a game runtime.

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/skill_quality.py --check-catalog
```

After adding, removing or renaming a skill, regenerate the path catalog:

```sh
python tools/skill_quality.py --write-catalog --check-catalog
```

Do not rewrite a whole README from an older snapshot: preserve concurrent catalog edits. Fetch current branch and main first, work in a review branch, test each coherent change, commit and push without force. Record the remote SHA and CI conclusion after each batch. A created tree is not a published commit, and a created commit is not synchronized until its branch ref advances.

The checker validates frontmatter, names, common tables, inline Markdown file links inside the installable pack, and catalog drift. It does not validate every CommonMark construct, HTTP availability, API semantics, agent behavior or actual gameplay. Routing tests check explicit names/mode vocabulary, not LLM routing accuracy. Unrun engine, agent and human tests must be labeled not-run.

## Engineering contracts

The six engineering skills have a scoped registry, example contracts and three classes of evaluation cases. Run `python tools/engineering_quality.py` after changing their modes, dependencies or cases. CI validates the structure; the default report intentionally shows unexecuted cases as not-run. Actual model responses and judgments use the [evaluation record workflow](docs/EVALUATION.md). Keep private run outputs outside `skills/` and out of commits unless deliberately sanitized and approved.

A new skill needs an explicit owner, a bounded responsibility, meaningful output and observable failure/acceptance scenarios. Add routing seeds and update each README locale together; do not create another overlapping rule owner merely to grow the catalog.
