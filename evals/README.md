# Evals

On-demand harness (not CI — it calls `claude` and costs tokens): `./evals/run.sh [scenario…]`.
Each scenario is `evals/scenarios/<name>/` with `prompt.txt`, `rubric.md` and an optional `fixture/`
repo; a judge model scores the transcript against the rubric (`judge-prompt.md`).

Scenarios for `story` / `small-task` / `fix` are to be added from real tasks — the point is to compare
the plugin against plain auto mode on the same input (tokens, iterations, result quality).
