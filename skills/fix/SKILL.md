---
name: fix
model: inherit
effort: high
agents: [explorer, devils-advocate]
description: >
  Use to fix a reported bug: the dev pastes the bug (ticket text, stack trace, logs, QA steps);
  Claude digs for the root cause (several hypotheses, traced to where the wrong value is born),
  proves it with a failing test, shows the failure + proposes the fix and agrees it with the dev,
  then fixes it through the gate, then recommends places with the same mistake,
  and leaves the change uncommitted for the dev. A reported bug is always treated as a bug — Claude
  never argues it away. Triggers on "/st-plug:fix", "fix {bug}", "bug in {X}", "regression in {X}",
  "полагодь баг", "виправ багу", "ось баг", "регресія в {X}", "чому зламалось".
---

# Skill: fix

The bugfix entry point. Input is whatever the dev has — a ticket, a stack trace, logs, QA steps. The
skill's value over "paste the bug into auto mode": it **digs wider and deeper** — several hypotheses,
the wrong value traced to where it's born, history checked — then **proves** the cause with a failing
test, **shows** that failure with a proposed fix for the dev to agree, fixes it through the gate, and
recommends where the **same mistake** lives elsewhere.

**A reported bug is a bug.** QA filed it, the dev took it — Claude does not decide "works as designed".
When the *correct* behaviour isn't defined anywhere (code, invariants, the ticket), that is a question
about **what to build**, asked in step 3 — never a reason to stop.

**Same house rules as `story`:** no documents to read, every stop is one screen of decisions;
nothing committed by Claude; nothing left open — a decision is asked the moment it appears or, if it's
a convention-following detail, just made. Conventions (layering, test style, gate commands) come from
`CLAUDE.md` + the code. Full rules → [`../_shared/house-rules.md`](../_shared/house-rules.md).

## Inputs

- The bug report, in any form. Required.
- `CLAUDE.md` + the code.
- `docs/contexts/<Context>/language.md` (if present) — its **Invariants** are the closest thing to a
  spec: a violated invariant confirms the expected behaviour → [`../_shared/contexts.md`](../_shared/contexts.md).

## Protocol

### 1. Reproduce on paper

From the report, state the bug in one line: **«doing X, expected Y, got Z»**. Ask the dev only for
what the report and the code can't give (at most one `AskUserQuestion`, ≤ 3 questions, Claude's best
guess first) — typically the expected value when the ticket only says "wrong".

### 2. Dig — wider and deeper than the first plausible line

This step is the reason the skill exists. Auto mode stops at the first line that *could* explain the
symptom; this skill does not.

- **Localize.** Stack trace / error / named endpoint → Grep/Read yourself. Symptom only ("the total is
  wrong sometimes") → dispatch [`explorer`](../../agents/explorer.md) **with `model: sonnet`** to map
  the code path, `file:line` anchored.
- **Trace the wrong value to where it's born**, not where it surfaces: entity method → use case →
  repository query → presenter / response, and across contexts (Messenger handlers, shared UUIDs).
  Symptom (where it shows) and cause (where the wrong decision is made) are named separately.
- **2–3 hypotheses, not one.** Each is confirmed or refuted with evidence — a test, a query, a code
  path that can or can't be reached. Keep the refuted ones: they go into the step-4 summary in one line each.
- **Check the usual suspects** when they fit the symptom: data already in the DB (nulls, old enum
  values, rows created before a migration), concurrency / transactions / locking (intermittent bugs),
  time zones and periods, rounding / money, caching, async ordering.
- **History, no files.** `git log -L` / `git blame` on the cause lines: which change introduced it,
  was it fixed before? A recurrence means the old test was too weak → strengthen that test instead of
  adding a parallel one.

### 3. Prove it — a failing test before any fix

Write the test that reproduces the bug at the level the behaviour implies (unit for a rule,
integration for persistence / a handler, functional for a request → full response; style per
`CLAUDE.md`). Run it and classify per [`../_shared/tdd-loop.md`](../_shared/tdd-loop.md):
it must be a **GOOD red** — failing on the assertion that encodes the expected behaviour. Keep the
failing output for step 4.

**External integrations** (payment provider, SQS, S3, push, a third-party API) — the bug often can't
be reproduced locally. Then the proof is the evidence instead: the log line / payload / contract
mismatch + the exact code path that mishandles it; the test in step 5 pins *our* handling of that
input with a stub. Say plainly that the external side wasn't reproduced.

Can't be pinned at all → stop and say why: an unpinned fix is a guess.

### 3b. Challenge it — only when the bug isn't trivial

Dispatch [`devils-advocate`](../../agents/devils-advocate.md) in **Mode D** **with `model: sonnet`**
(a bounded check on concrete inputs — it doesn't need the heavier tier) when **any** of:
- the cause is not on the line where the symptom shows;
- the bug touches money, state transitions, concurrency / transactions, or data already in the DB;
- more than one hypothesis survived step 2.

Skip it for the trivial (a wrong field name, a missing validation on the line that fails). Its
findings are folded into step 4's screen — a `wrong-cause` / `still-broken` finding sends Claude back
to steps 2–3 first; a `collateral` one becomes a line under the fix. `HOLDS` adds nothing.

### 4. Show it, propose the fix, agree — before touching production code

One `AskUserQuestion` call; the question body is one screen:

> **<bug one-liner>**
> Cause: `<File.php:line>` — <what the code decides wrongly, in domain terms>.
> Proof: `<TestClass::testMethod>` fails — `<the quoted assertion: expected … got …>`.
> Ruled out: <hypothesis> — <one-line why> (one line each, if any).
> Fix: <the minimal change at the cause — a few lines of intent or a short snippet>.

Options (no "reject" — the dev steers instead):
- «Yes, apply the fix» **(Recommended)**;
- a Claude-proposed variation — the fix at a different layer, or an extra test case;
- free text ("Other").

**Expected behaviour undefined** (no invariant, ticket and code silent, two reasonable readings)?
Ask that first, in the same call: Claude's recommended behaviour / the alternative / **«Ask PM»** /
Other. «Ask PM» → print a copy-ready question for the PM and **stop**; the test stays in the working
tree; the dev re-runs `/st-plug:fix` with the answer.

### 5. GREEN → GATE

Per the TDD loop, **COMMIT replaced by STOP**:

- **GREEN** — the agreed change at the cause; the step-3 test now passes. No drive-by refactors.
- **GATE** — the repo's full check (tests + static analysis + architecture + style), per `CLAUDE.md` /
  [`../_shared/tdd-loop.md`](../_shared/tdd-loop.md).
- An unagreed decision appears (changes behaviour or a contract) → ask now; a convention-following
  detail → just do it.

### 6. Same mistake elsewhere — a recommendation, after the fix

Only once the bug itself is green: search for the pattern the cause revealed — other callers of the
same method, sibling handlers / use cases with the same logic, the same query shape. Found any →
recommend them, one `AskUserQuestion`, each place as `file:line` + why it's the same mistake:
- «Leave them — recommendation only» **(Recommended)** — the fix stays scoped to the reported bug;
- «Fix them too» — each gets its own RED test, same gate, same diff.

None found → one line saying so.

### 7. Hand over

- **Keep the pinning test?** One `AskUserQuestion` (bundled with step 6's question when there is one):
  - «Keep it» — **(Recommended)** for a unit / integration test: cheap, and it guards the regression;
  - «Remove it» — **(Recommended)** for a functional / API test when an existing test already covers
    this endpoint: the fix stays proven (it went red → green), the suite doesn't grow another slow test;
  - Other — e.g. «fold the case into `<ExistingTest>`».
  Remove → delete the test file / method and re-run the affected suite once.
- If the bug exposed a rule that wasn't written down, add it to the context's `language.md`
  `## Invariants` (bootstrap the file per the contexts reference if absent) — it lands in the same diff.
- Hand over per [`../_shared/house-rules.md`](../_shared/house-rules.md) 
  one line with the gate result, then «Review the diff and commit it yourself». Never `git add` /
  `git commit`.

## Definition of Done

- The cause (not just the symptom) is fixed; ≥2 hypotheses were checked; a test failed before the
  fix and passes after (GOOD red shown to the dev) — or, for an external integration, the evidence
  was shown and our handling is pinned with a stub.
- The failing test + proposed fix were agreed with the dev before production code changed; nothing left open.
- The same-mistake search ran after the fix and its findings were recommended to the dev.
- The dev chose whether the pinning test stays.
- Gate green; nothing committed by Claude.
- The RED pin + the GATE are this skill's **structural self-check**
  ([`../_shared/house-rules.md`](../_shared/house-rules.md)); the result is the handoff line.

## Anti-patterns

- **"Not a bug" / "works as designed"** — not Claude's call. Undefined expected behaviour is a question, not a verdict.
- **Fixing the symptom** — a null-check where the wrong value is produced three calls earlier.
- **Stopping at the first plausible hypothesis** — that is auto mode; prove it and rule out the others.
- **Asking the dev to approve a fix before showing the failing test** — proof first, then the proposal.
- **Fixing without a pinning test**, or with a test that passes before the fix.
- **Drive-by refactoring** in the fix diff.
- **Writing fix records, notes or open-question lists** — the diff + the test are the record.
- **Committing** — the dev owns the commit.
