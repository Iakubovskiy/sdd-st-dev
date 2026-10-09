# TDD loop — RED → GREEN → REFACTOR → GATE → STOP

> **Reference-only.** Not a skill. The build cycle `story`, `small-task` and `fix` run for every
> agreed behaviour / fix. There is no COMMIT step: the cycle ends in **STOP** — the dev reviews and
> commits ([`house-rules.md`](./house-rules.md)).

## Commands

Resolve once per run, first hit wins:
1. **`CLAUDE.md`** — the commands it documents (e.g. `composer ci:phpunit`, `composer ci:static-analysis`,
   `composer ci:architecture`, `composer ci:code-style`; or one aggregate like `composer ci:pack`).
2. **Repo scripts** — `composer.json` `scripts`, `Makefile` targets, `package.json` scripts.
3. **Toolchain defaults** — e.g. `vendor/bin/phpunit`, `vendor/bin/phpstan`.
4. Nothing found → ask the dev once. Never guess.

If the repo runs inside a container (`docker compose exec <svc> …` in `CLAUDE.md`), run the commands
the same way. Print the resolved set in one line before the first RED.

## RED — the failing test first

1. Write the test(s) for the agreed behaviour **before any production code**, where and how the repo
   keeps tests for that layer (`CLAUDE.md` style rules apply: e.g. one scenario per test method,
   full-response assertions for API tests).
2. Run just those tests and **classify the first run** — say it out loud:

   | Class | Looks like | Action |
   |---|---|---|
   | **GOOD red** | runs, fails on the assertion / «not implemented» | → GREEN |
   | **BAD red** | the test itself doesn't compile / wrong symbol in the test | fix the test, re-run |
   | **false-pass** | green before any production code | the test asserts nothing real — strengthen it |
   | **NON-red** | skipped (a dependency like Docker/DB unavailable) | not a pass; make it runnable or name it in the handoff |

3. **Quote the failing line** (expected vs actual) before writing production code.

## GREEN — the least code that passes

Only what turns the quoted assertion green. No speculative generality, no unrelated edits. Re-run;
the quoted failure is green and nothing else broke.

**Code-first schema:** when the change touches ORM mapping, generate the migration with the repo's
diff tool (e.g. `doctrine:migrations:diff`) once the entity change is green, and include it.

## REFACTOR — tidy while green

Names, extractions, duplication — re-running after each change. A refactor that goes red and isn't
trivially fixable is reverted.

## GATE — not done until clean

The repo's full check: tests + static analysis + architecture rules + code style (whatever step 1
resolved). Any failure → fix it; never hand over around a red gate. After 3 failed attempts on the
same red, stop and show the dev the failure with Claude's best hypothesis.

## STOP

Leave everything in the working tree. Report the gate in one line per the house-rules handoff.
