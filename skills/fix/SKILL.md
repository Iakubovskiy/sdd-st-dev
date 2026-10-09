---
name: fix
model: inherit
effort: high
agents: [explorer]
description: >
  Use to fix a reported bug: the dev pastes the bug (ticket text, stack trace, logs, QA steps);
  Claude finds the root cause in code (not the symptom), agrees the fix + the pinning test with the
  dev BEFORE writing code, fixes it test-first through the gate, then recommends places with the same mistake,
  and leaves the change uncommitted for the dev. A reported bug is always treated as a bug — Claude
  never argues it away. Triggers on "/sdd:fix", "fix {bug}", "bug in {X}", "regression in {X}",
  "полагодь баг", "виправ багу", "ось баг", "регресія в {X}", "чому зламалось".
---

# Skill: fix

The bugfix entry point. Input is whatever the dev has — a ticket, a stack trace, logs, QA steps. The
skill's value over "paste the bug into auto mode": it fixes the **root cause** rather than wrapping the
symptom, pins it with a test that **failed before and passes after**, agrees both with the dev
**before** writing code, and then recommends where the **same mistake** lives elsewhere.

**A reported bug is a bug.** QA filed it, the dev took it — Claude does not decide "works as designed".
When the *correct* behaviour isn't defined anywhere (code, invariants, the ticket), that is a question
about **what to build**, asked in step 3 — never a reason to stop.

**Same house rules as `story`:** no documents to read, every stop is one screen of decisions;
nothing committed by Claude; nothing left open — a decision is asked the moment it appears or, if it's
a convention-following detail, just made. Conventions (layering, test style, gate commands) come from
`CLAUDE.md` + the code. Prose written into context docs follows `artifact_language`
→ [`../_shared/artifact-language.md`](../_shared/artifact-language.md).

## Inputs

- The bug report, in any form. Required.
- `CLAUDE.md` + the code.
- `docs/contexts/<Context>/language.md` (if present) — its **Invariants** are the closest thing to a
  spec: a violated invariant confirms the expected behaviour → [`../story/references/contexts.md`](../story/references/contexts.md).

## Protocol

### 1. Reproduce on paper

From the report, state the bug in one line: **«doing X, expected Y, got Z»**. Ask the dev only for
what the report and the code can't give (at most one `AskUserQuestion`, ≤ 3 questions, Claude's best
guess first) — typically the expected value when the ticket only says "wrong".

### 2. Root cause

- Stack trace / error message / named endpoint → localize it yourself (Grep/Read). Symptom only
  ("the total is wrong sometimes") → dispatch [`explorer`](../../agents/explorer.md) **with
  `model: sonnet`** to map the code path, `file:line` anchored.
- Separate **symptom** (where it blows up) from **cause** (where the wrong decision is made). The fix
  goes at the cause. If they're the same line, say so.
- **History check, no files:** `git log -L` / `git blame` on the cause lines — was this fixed before,
  and which change reintroduced it? A recurrence means the old test was too weak → strengthen it
  instead of adding a parallel one.

### 3. Agree the fix — before any code

One `AskUserQuestion` call:

> **<bug one-liner>**
> Cause: `<File.php:line>` — <what the code decides wrongly, in domain terms>.
> Fix: <the minimal change>.
> Pinning test: <level — unit / integration / functional> — <the scenario that fails today>.

Options (no "reject" — the dev steers instead):
- «Yes, do it» **(Recommended)**;
- a Claude-proposed variation — fix at a different layer, or a stronger/extra test case;
- free text ("Other").

**Expected behaviour undefined** (no invariant, ticket and code silent, two reasonable readings)?
Ask that first, in the same call: Claude's recommended behaviour / the alternative / **«Ask PM»** /
Other. «Ask PM» → print a copy-ready question for the PM and **stop**; the dev re-runs `/sdd:fix`
with the answer.

### 4. RED → GREEN → GATE

Per [`../implement/references/tdd-loop.md`](../implement/references/tdd-loop.md), **COMMIT replaced by
STOP**:

- **RED** — the agreed test; first run must be a **GOOD red** (fails on the assertion encoding the
  expected behaviour). Quote the failing line. Can't be pinned by a test → stop and say why: an
  unpinned fix is a guess.
- **GREEN** — the smallest change at the cause. No drive-by refactors.
- **GATE** — the repo's full check (tests + static analysis + architecture + style), per `CLAUDE.md` /
  [`../implement/references/command-detection.md`](../implement/references/command-detection.md).
- An unagreed decision appears (changes behaviour or a contract) → ask now; a convention-following
  detail → just do it.

### 5. Same mistake elsewhere — a recommendation, after the fix

Only once the bug itself is green: search for the pattern the cause revealed — other callers of the
same method, sibling handlers / use cases with the same logic, the same query shape. Found any →
recommend them, one `AskUserQuestion`, each place as `file:line` + why it's the same mistake:
- «Leave them — recommendation only» **(Recommended)** — the fix stays scoped to the reported bug;
- «Fix them too» — each gets its own RED test, same gate, same diff.

None found → one line saying so.

### 6. Hand over

- If the bug exposed a rule that wasn't written down, add it to the context's `language.md`
  `## Invariants` (bootstrap the file per the contexts reference if absent) — it lands in the same diff.
- Emit the stage-handoff block per [`../_shared/handoff.md`](../_shared/handoff.md) (utility variant):
  one line with the gate result, then «Review the diff and commit it yourself». Never `git add` /
  `git commit`.

## Definition of Done

- The cause (not just the symptom) is fixed; a test failed before the fix and passes after
  (GOOD red quoted).
- Fix + test were agreed with the dev before code; nothing left open.
- The same-mistake search ran after the fix and its findings were recommended to the dev.
- Gate green; nothing committed by Claude.
- The RED pin + the GATE are this skill's **structural self-check**
  ([`../_shared/self-check.md`](../_shared/self-check.md)); the result is the handoff line.

## Anti-patterns

- **"Not a bug" / "works as designed"** — not Claude's call. Undefined expected behaviour is a question, not a verdict.
- **Fixing the symptom** — a null-check where the wrong value is produced three calls earlier.
- **Fixing without a pinning test**, or with a test that passes before the fix.
- **Drive-by refactoring** in the fix diff.
- **Writing fix records, notes or open-question lists** — the diff + the test are the record.
- **Committing** — the dev owns the commit.
