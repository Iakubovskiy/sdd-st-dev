---
name: task-review
model: inherit
effort: medium
agents: [reviewer]
description: >
  Use to review the code written for a task — runs automatically at the end of every story slice,
  small-task and fix, and on demand for any uncommitted diff or branch. A clean-context reviewer hunts
  runtime hazards from a per-stack checklist (memory leaks, recursion and event / rebuild loops, race
  conditions, N+1, deadlocks, main-thread work …). Problems in the current changes are fixed right
  away without asking; problems outside them are only listed. Triggers on "/st-plug:task-review",
  "review my changes", "review the diff", "check the code for leaks / N+1", "переглянь зміни",
  "зроби рев'ю", "рев'ю задачі", "перевір код".
---

# Skill: task-review

One review, two ways in: **called by `story` (after each slice), `small-task` and `fix`** right after
their gate, or **run by the dev** on whatever is uncommitted (or the branch). It looks for the problems
tests and static analysis rarely catch — leaks, loops, races, N+1, deadlocks — not for style.

House rules → [`../_shared/house-rules.md`](../_shared/house-rules.md). Checklist →
[`../_shared/review-checklist.md`](../_shared/review-checklist.md).

## Inputs

- **The change.** Called from a flow: the diff of this session's work. Run by the dev: the
  uncommitted working tree (`git diff` + untracked); clean tree → current branch vs its base.
  Nothing to review → say so and stop.
- **What was agreed** — from the calling flow (behaviours / the fix); run by the dev: the task / bug
  text if they paste it, otherwise skip that pass.
- The surface ([`../_shared/surfaces.md`](../_shared/surfaces.md)).

## Protocol

1. **Skip if mechanical.** Only DTOs, config, wiring, generated migrations, renames → one line
   «task-review: mechanical only, skipped» and stop. (Saves a whole agent call.)
2. **Dispatch** [`reviewer`](../../agents/reviewer.md) (sonnet, clean context) with: the exact git
   command for the diff, the surface, what was agreed (verbatim). It reads the diff and at most one
   hop around it, against the checklist.
3. **IN DIFF findings → fix now, no question.** Each fix goes through
   [`../_shared/tdd-loop.md`](../_shared/tdd-loop.md) (a test first when it's behaviour — e.g. a
   query-count test for N+1, a dispose test for a leak; otherwise straight to the change) and the gate
   re-runs once at the end. Exception — the fix would change an agreed behaviour or a contract →
   house rule «ask now».
4. **OUTSIDE DIFF findings → list only**, never touch: `file:line — problem`. The dev decides; if they
   say "fix it", that's a new `small-task` / `fix`.
5. **Report** (part of the calling flow's handoff, or the dev's answer): one line «task-review: fixed
   N in this diff — <short list>», then the outside list (or «nothing outside»). Never `git add` /
   `git commit`.

## Definition of Done

- Mechanical-only diffs were skipped; otherwise the reviewer ran on the diff with the surface's checklist.
- Every in-diff finding is fixed and the gate is green again; outside findings are listed, untouched.
- The re-run gate + the reviewer pass are this skill's **structural self-check**
  ([`../_shared/house-rules.md`](../_shared/house-rules.md)).

## Anti-patterns

- **Asking before fixing in-diff problems** — they are this session's own code; fix them.
- **Fixing outside the diff** — out of scope; list it.
- **Sweeping the repo** — the diff plus one hop, nothing more.
- **Re-checking what the gate / config enforces** (style, static analysis, timeouts, access rules).
