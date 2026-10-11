---
name: small-task
model: inherit
effort: medium
agents: [explorer, devils-advocate]
description: >
  Use for a small change that doesn't need modelling: a field, a filter, an endpoint variant, a rule
  tweak, a CLI option — one behaviour group, one session, no documents. Claude finds where it goes
  and the existing pattern to follow, checks it isn't secretly a big feature (offers /st-plug:story if it
  is), agrees the behaviour + tests with the dev before writing code, builds it test-first, and
  leaves the change uncommitted. Triggers on "/st-plug:small-task", "small task", "quick change",
  "add a field / filter / option to …", "невелика задача", "маленька фіча", "дрібна зміна", "додай поле".
---

# Skill: small-task

For work that is too small for `story` and should still beat auto mode: Claude follows the repo's
**existing pattern** instead of inventing one, catches the moment a "small" task is actually a feature,
and agrees behaviour + tests with the dev **before** code.

**Same house rules as `story` and `fix`:** no documents to read — every stop is one screen of
decisions; nothing committed by Claude; nothing left open (ask the moment a decision appears, or just
do it when it's a convention-following detail). Conventions come from `CLAUDE.md` + the code. Full rules → [`../_shared/house-rules.md`](../_shared/house-rules.md).

## Inputs

- The task text (ticket, a sentence, a Slack message). Required.
- Optional: a design (Figma link with Figma MCP connected, or screenshots) and an API contract
  (Swagger / OpenAPI link or file) → [`../_shared/inputs.md`](../_shared/inputs.md).
- `CLAUDE.md` + the code.
- `docs/contexts/<Context>/language.md` (if present) — terms + invariants of the touched context
  → [`../_shared/contexts.md`](../_shared/contexts.md).

## Protocol

### 1. Find the place and the pattern

Grep/Read yourself (no subagent by default; dispatch [`explorer`](../../agents/explorer.md) **with
`model: sonnet`** only when the task names no module, endpoint or entity). Establish:
- **where** the change goes (context / module, the files);
- **the closest existing implementation of the same kind** — the endpoint, filter, handler or test that
  this change should look like. The build follows it; a deviation is a decision for step 3.
- whether the task **changes existing behaviour** or only **adds** something next to it;
- the **surface** ([`../_shared/surfaces.md`](../_shared/surfaces.md)); UI work → design per
  [`../_shared/inputs.md`](../_shared/inputs.md) (folder + «Done» / «No design»); a Swagger link →
  download and extract only the touched paths.

### 2. Is it really small?

Recommend `/st-plug:story` instead when **any** holds:
- a new entity / aggregate, or a new state / transition on an existing one;
- more than one bounded context changes (beyond reading by UUID);
- more than ~3 behaviours to agree in step 3;
- a schema change that touches existing rows (backfill, new non-null field, changed enum).

Then one `AskUserQuestion`: «Switch to /st-plug:story» **(Recommended)** / «Keep it small — I know the
scope» / Other. Staying small is the dev's call.

**Changes existing behaviour?** Dispatch [`devils-advocate`](../../agents/devils-advocate.md) in
**Mode C** **with `model: sonnet`** with the task text, the step-1 places, the surface and — if
present — the design folder and contract extract. Purely additive changes skip it. Findings are **not truncated** — how many there are is itself the signal:
- **≤ 3 material findings** → they become questions in step 3 (recommendation / alternative /
  «Ask PM» / «Ask backend» / «Ask frontend» / Other); any «Ask …» → the messages per
  [`../_shared/house-rules.md`](../_shared/house-rules.md) and **stop**;
- **more than 3** → the task isn't small: one `AskUserQuestion` — «Switch to /st-plug:story» **(Recommended)**,
  carrying the findings over / «Stay small — walk me through all of them» / Other.

### 3. Agree before code

One `AskUserQuestion` call, one question per behaviour (≤ 3):

> **<Behaviour>**
> I'm doing: <the change, in domain terms> — following `<ExistingThing>` (`File.php`).
> I'm testing it from: <levels per the surface — [`../_shared/surfaces.md`](../_shared/surfaces.md)>.

Options — no "reject":
- «Yes, do it» **(Recommended)**;
- a Claude-proposed variation (an extra case, or a narrower variant);
- free text ("Other").

Devil's-advocate findings (if any) go into the same call, before the behaviours.

### 4. Build — TDD, no commit

Per [`../_shared/tdd-loop.md`](../_shared/tdd-loop.md): `RED → GREEN →
REFACTOR → GATE`, **COMMIT replaced by STOP**. Gate commands per `CLAUDE.md` /
[`../_shared/tdd-loop.md`](../_shared/tdd-loop.md).
Schema / local-storage change → the surface's persistence rule ([`../_shared/surfaces.md`](../_shared/surfaces.md)). An unagreed decision that changes behaviour or a contract → ask now; a convention-following
detail → just do it.

### 5. Review

Run [`task-review`](../task-review/SKILL.md) on the diff: in-diff problems fixed right away, outside
ones listed.

### 6. Hand over

- New term, invariant or provider rule surfaced → add it to the context's `language.md` in the same diff.
- Hand over per [`../_shared/house-rules.md`](../_shared/house-rules.md) 
  one line with the gate result, then «Review the diff and commit it yourself». Never `git add` /
  `git commit`.

## Definition of Done

- The change follows the named existing pattern, or the deviation was agreed.
- Behaviours + tests were agreed before code; nothing left open.
- The "is it really small" check ran; the dev chose to stay small or switched to `story`.
- `task-review` ran; in-diff findings fixed, outside ones listed.
- Gate green; nothing committed by Claude.
- The per-task GATE is this skill's **structural self-check** ([`../_shared/house-rules.md`](../_shared/house-rules.md));
  its result is the handoff line.

## Anti-patterns

- **Inventing a new pattern** when the repo already has one for this kind of change.
- **Letting a feature hide in a small task** — new entity, new state, several contexts → offer `story`.
- **Writing documents or plans** for a small task.
- **Committing** — the dev owns the commit.
