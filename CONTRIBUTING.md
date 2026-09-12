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
