---
name: small-task
model: inherit
effort: medium
agents: [explorer, devils-advocate]
description: >
  Use for a small change that doesn't need modelling: a field, a filter, an endpoint variant, a rule
  tweak, a CLI option — one behaviour group, one session, no documents. Claude finds where it goes
  and the existing pattern to follow, checks it isn't secretly a big feature (offers /sdd:story if it
  is), agrees the behaviour + tests with the dev before writing code, builds it test-first, and
  leaves the change uncommitted. Triggers on "/sdd:small-task", "small task", "quick change",
  "add a field / filter / option to …", "невелика задача", "маленька фіча", "дрібна зміна", "додай поле".
---

# Skill: small-task

For work that is too small for `story` and should still beat auto mode: Claude follows the repo's
**existing pattern** instead of inventing one, catches the moment a "small" task is actually a feature,
and agrees behaviour + tests with the dev **before** code.

**Same house rules as `story` and `fix`:** no documents to read — every stop is one screen of
decisions; nothing committed by Claude; nothing left open (ask the moment a decision appears, or just
do it when it's a convention-following detail). Conventions come from `CLAUDE.md` + the code. Prose
written into context docs follows `artifact_language` → [`../_shared/artifact-language.md`](../_shared/artifact-language.md).

## Inputs

- The task text (ticket, a sentence, a Slack message). Required.
- `CLAUDE.md` + the code.
- `docs/contexts/<Context>/language.md` (if present) — terms + invariants of the touched context
  → [`../story/references/contexts.md`](../story/references/contexts.md).

## Protocol

### 1. Find the place and the pattern

Grep/Read yourself (no subagent by default; dispatch [`explorer`](../../agents/explorer.md) **with
`model: sonnet`** only when the task names no module, endpoint or entity). Establish:
- **where** the change goes (context / module, the files);
- **the closest existing implementation of the same kind** — the endpoint, filter, handler or test that
  this change should look like. The build follows it; a deviation is a decision for step 3.
- whether the task **changes existing behaviour** or only **adds** something next to it.

### 2. Is it really small?

Recommend `/sdd:story` instead when **any** holds:
- a new entity / aggregate, or a new state / transition on an existing one;
- more than one bounded context changes (beyond reading by UUID);
- more than ~3 behaviours to agree in step 3;
- a schema change that touches existing rows (backfill, new non-null field, changed enum).

Then one `AskUserQuestion`: «Switch to /sdd:story» **(Recommended)** / «Keep it small — I know the
scope» / Other. Staying small is the dev's call.

**Changes existing behaviour?** Dispatch [`devils-advocate`](../../agents/devils-advocate.md) in
**Mode C** **with `model: sonnet`**, capped at **3 findings**, with the task text + the step-1 places.
Purely additive changes skip it. Findings become questions in step 3 (recommendation / alternative /
«Ask PM» / Other); «Ask PM» → copy-ready question for the PM and **stop**.

### 3. Agree before code

One `AskUserQuestion` call, one question per behaviour (≤ 3):

> **<Behaviour>**
> I'm doing: <the change, in domain terms> — following `<ExistingThing>` (`File.php`).
> I'm testing it from: <unit — …>; <integration — …>; <functional — request → full response …>.

Options — no "reject":
- «Yes, do it» **(Recommended)**;
- a Claude-proposed variation (an extra case, or a narrower variant);
- free text ("Other").

Devil's-advocate findings (if any) go into the same call, before the behaviours.

### 4. Build — TDD, no commit

Per [`../implement/references/tdd-loop.md`](../implement/references/tdd-loop.md): `RED → GREEN →
REFACTOR → GATE`, **COMMIT replaced by STOP**. Gate commands per `CLAUDE.md` /
[`../implement/references/command-detection.md`](../implement/references/command-detection.md).
Code-first schema change → generate the migration with the repo's diff tool after the entity change is
green. An unagreed decision that changes behaviour or a contract → ask now; a convention-following
detail → just do it.

### 5. Hand over

- New term or invariant surfaced → add it to the context's `language.md` in the same diff.
- Emit the stage-handoff block per [`../_shared/handoff.md`](../_shared/handoff.md) (utility variant):
  one line with the gate result, then «Review the diff and commit it yourself». Never `git add` /
  `git commit`.

## Definition of Done

- The change follows the named existing pattern, or the deviation was agreed.
- Behaviours + tests were agreed before code; nothing left open.
- The "is it really small" check ran; the dev chose to stay small or switched to `story`.
- Gate green; nothing committed by Claude.
- The per-task GATE is this skill's **structural self-check** ([`../_shared/self-check.md`](../_shared/self-check.md));
  its result is the handoff line.

## Anti-patterns

- **Inventing a new pattern** when the repo already has one for this kind of change.
- **Letting a feature hide in a small task** — new entity, new state, several contexts → offer `story`.
- **Writing documents or plans** for a small task.
- **Committing** — the dev owns the commit.
