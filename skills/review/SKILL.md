---
name: review
model: inherit
effort: high
agents: [reviewer]
description: >
  Use for an optional, independent second look at a change before the dev commits or opens a PR —
  a clean-context reviewer checks the diff against what was asked (the story / bug / task text and
  the behaviours agreed in this session), the repo's conventions (CLAUDE.md) and the touched
  contexts' invariants, then each finding is resolved with the dev on the spot. Triggers on
  "/sdd:review", "review my changes", "review the diff", "is this ready for PR", "переглянь зміни",
  "зроби рев'ю", "рев'ю диффу".
---

# Skill: review

Optional — never a gate. The dev runs it when a second pair of eyes is worth one agent call: a wide
change, an unfamiliar module, money or state logic. The reviewer did **not** write the code and sees
none of the conversation that did — that independence is the point.

House rules (one screen per stop, nothing committed, nothing left open) →
[`../_shared/house-rules.md`](../_shared/house-rules.md).

## Inputs

- **The change.** Default: the uncommitted working tree (`git diff` + untracked files). If the tree
  is clean: the current branch vs its base (`git diff <base>...HEAD`). Nothing to review → say so and stop.
- **What was asked.** In priority order: the behaviours / fix agreed earlier in this session (the
  step-5 answers of `story`, step-3 of `small-task`, step-4 of `fix`); else the story / bug / task text
  the dev pastes. Neither → ask the dev for one line on what the change is meant to do.
- `CLAUDE.md`; `docs/contexts/<Context>/language.md` + `model.md` for the touched contexts
  → [`../_shared/contexts.md`](../_shared/contexts.md).

## Protocol

1. **Scope.** Resolve the diff; list touched contexts (modules). One line to the dev: «Reviewing N
   files in <contexts> against <what was asked>.»
2. **Dispatch** [`reviewer`](../../agents/reviewer.md) (clean context). The prompt carries: how to get
   the diff (the exact git command), what was asked (verbatim), the paths to `CLAUDE.md` and the
   context docs. It reads everything itself.
3. **Resolve every finding with the dev** — one `AskUserQuestion` per finding (batch ≤ 4), the finding
   as `file:line` + problem + suggested fix:
   - «Fix it» **(Recommended for asked-vs-built and correctness findings)** — Claude fixes it through
     [`../_shared/tdd-loop.md`](../_shared/tdd-loop.md) (a test first when it's behaviour), no commit;
   - «Leave it» **(Recommended for style-only findings the gate doesn't enforce)**;
   - Other.
4. **Hand over** per the house rules: the gate result after any fixes, then «Review the diff and
   commit it yourself». No review-record file.

## Definition of Done

- The reviewer ran in a clean context over the whole change.
- Every finding was fixed or consciously left by the dev; nothing open.
- After fixes, the gate is green — the gate + the reviewer pass are this skill's **structural
  self-check** ([`../_shared/house-rules.md`](../_shared/house-rules.md)).

## Anti-patterns

- **Reviewing in the context that wrote the code** — dispatch the agent; don't self-review.
- **Uncited findings** — no `file:line`, no finding.
- **A report file** — findings are resolved on the spot, not filed.
- **Re-litigating what `CLAUDE.md` already settled**, or style the gate already enforces.
