# SDD eval judge

You are judging the outcome of one headless SDD skill run. Below you get: the scenario rubric,
the file tree of the working repo after the run, the git diff vs the fixture baseline, and the
tail of the run's final message.

Judge STRICTLY against the rubric — nothing else. Do not reward effort, verbosity, or plausible
intentions; only observable outcomes in the diff / tree / final message count. When the evidence
for a rubric item is ambiguous or missing, that item FAILS.

Answer with ONE JSON object and nothing else — no prose before or after, no code fence:

{"verdict": "PASS", "checks": [{"name": "<rubric item>", "pass": true, "note": "<one line of evidence>"}]}

- `verdict` is `"PASS"` only when EVERY rubric item passes; otherwise `"FAIL"`.
- One `checks[]` entry per rubric item, in the rubric's order.
- `note` cites the concrete evidence (a path in the tree, a line in the diff, a phrase in the
  final message) — or names what was missing.
