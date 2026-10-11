# House rules — how every skill in this plugin talks to the dev

> **Reference-only.** Not a skill. `story`, `small-task`, `fix` and `review` all follow these
> rules (and `answer`, `task-review`); each SKILL.md links here instead of repeating them.

## Ownership

- **Claude never commits.** No `git add`, no `git commit`, no push. The dev reviews the diff and
  commits it — that is how ownership stays with the dev.
- **Conventions come from the repo**: `CLAUDE.md` first, then the code. When the repo already has
  a way of doing this kind of change, follow the closest existing example; a deviation is a decision
  to agree, not a default.

## Reading budget

- **The dev never gets a document to read.** No plans, task lists, tables or reports for approval.
- **Every stop is one screen**: what Claude decided (one line each) + an `AskUserQuestion` for what
  needs the dev. Diagrams go to files; chat shows only the *delta* vs today.

## Agreeing before code

The standard question, used for behaviours (`story`, `small-task`) and fixes (`fix`):

> **<Behaviour / bug>**
> I'm doing: <the change, in domain terms>.
> I'm testing it from: <level — scenario>; <level — scenario>.

Options — **never a "reject"** (it dead-ends the flow; the dev steers instead):
1. «Yes, do it» **(Recommended)**;
2. a Claude-proposed variation (an extra case, a narrower variant, a different layer);
3. free text ("Other").

Batch up to 4 questions per `AskUserQuestion` call.

## Questions for someone else — PM, backend, frontend

When the answer isn't in the code, the context docs or the ticket, the options for that question are:
Claude's recommendation **(Recommended)** / the alternative / **«Ask PM»** / **«Ask backend»** /
**«Ask frontend»** / Other. Offer only the targets that make sense (a pure UI question has no
«Ask backend»; on a backend repo «Ask backend» means a teammate). Frontend = mobile + web.

What Claude prints, then **stops** (the dev re-runs the command with the answer pasted in):

| Target | Output |
|---|---|
| **PM** | one short message — the product question, the context in a sentence, Claude's suggested answer. Nothing technical. |
| **backend / frontend** | (1) **short message** — 3–5 lines for chat; (2) **brief for their Claude** — a fenced block they paste into their session: what we're building, what we already found (`file:line`, endpoint, fields, payload examples), the exact question, the answer format we need (e.g. JSON schema of the response, error codes, the state list). Their side answers with `/st-plug:answer`. |

Several open questions → one message per target, grouped.

## Product questions

When the expected behaviour isn't defined anywhere and two readings are reasonable, it's a PM
question — use «Ask PM» above.

## Nothing stays open

During the build, a decision nobody agreed on:
- changes behaviour, the model or a contract (a new state, a locking strategy, a new error the
  client sees) → **stop and ask now**, recommendation first, then continue;
- is a convention-following detail (naming, a private helper, which existing base class) → **just
  do it**, don't mention it.

No notes "for later", no open-question lists, no record files.

## Subagent tiers

| Agent | Where | Model |
|---|---|---|
| `explorer` | all skills, only when Claude can't localize the code itself | `sonnet` (agent default) |
| `devils-advocate` | `story` (Mode C) | agent default (`opus`) — open-ended hunt |
| `devils-advocate` | `small-task` (Mode C), `fix` (Mode D) | `sonnet` (override) — bounded check |
| `reviewer` | `task-review` | `sonnet` (agent default) |

## Language

Everything Claude writes for people — questions, messages to PM / backend / frontend, briefs for
another Claude, answers — is in **the language the dev is using in the session**. Code, tests and
identifiers stay English. Prose in `docs/contexts/` matches the language of the file being edited; a
new file follows `CLAUDE.md` if it says, else the dev's language.

## Handoff

Every building skill ends the same way — a few lines, no report:
1. the gate result in one line (e.g. `phpunit ✓ phpstan ✓ deptrac ✓ ecs ✓`) — the gate is each
   skill's **structural self-check**; a red or skipped tier is named, never hidden;
2. the `task-review` result: what it fixed in this diff (one line) + spotted outside the diff
   (`file:line` — problem, not fixed);
3. «Review the diff and commit it yourself».
