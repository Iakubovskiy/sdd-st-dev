---
name: story
model: inherit
effort: high
agents: [explorer, devils-advocate]
description: >
  Use to build a feature from a PM user story — not from an idea, not from a spec. The dev pastes
  the story (or a ticket key); Claude scouts the code, asks only what the story + code can't answer,
  runs a devil's-advocate pass for flow gaps and conflicts with existing behaviour, sizes the scope,
  models the domain (class / sequence diagrams only when the scope needs them, code-first), agrees
  every slice's behaviour + tests with the dev interactively BEFORE writing code, then runs the TDD
  loop. Never commits — the dev reviews and commits each slice (ownership stays with the dev).
  Triggers on "/sdd:story", "story {slug}", "implement this story", "here's the story",
  "ось сторі", "зроби сторі", "реалізуй сторю", "фіча по сторі".
---

# Skill: story

The front door for **big features that arrive as a PM story**. The product decision is already made —
this skill does not re-interview the idea. Its job is to (1) find what the story got wrong *before*
coding, (2) model only what the scope needs, (3) agree behaviour + tests with the dev in small
interactive steps, (4) build it test-first, and (5) leave every change uncommitted for the dev.

**Reading budget.** The dev never gets a document "to read". Every stop is one screen: what Claude
decided (one line each) + `AskUserQuestion` for what needs the dev. Diagrams go to files; chat shows
only the *delta* vs today ("`Trip` gets status `Cancelled`; new transition `InProgress → Cancelled`").

**Not used by this skill:** the Socratic loop, the critic, the ideation agents, `spec.md`, Arc42,
staged SQL, `tasks.json`. Conventions come from the repo's `CLAUDE.md` + the code, not `survey`.

## Inputs

- The story text (pasted), or a ticket key when a tracker MCP is connected. Required.
- `<slug>` — optional; derived from the story title if absent (kebab-case, confirmed in step 1).
- `CLAUDE.md` + the code — the convention source (layering, test style, commands).
- `docs/contexts/<Context>/language.md` + `model.md` for every touched context — read if present,
  bootstrapped if absent (step 1) → [`./references/contexts.md`](./references/contexts.md).
- Working state: `.sdd/stories/<slug>.md` (gitignored) — answers, findings, decisions, slice
  status. Lets the run stop (PM blocker) and resume with `/sdd:story <slug>`.

## Protocol

### 1. Read → scout → ask

1. Read the story. Ensure `.sdd/` is in `.gitignore`; write the story verbatim to `.sdd/stories/<slug>.md`.
2. Dispatch [`explorer`](../../agents/explorer.md) **with `model: sonnet`** (override — this map feeds
   the conflict hunt, haiku misses semantic links). Ask for: touched bounded contexts (modules),
   entities + their states/transitions, use cases / endpoints / CLI / Messenger handlers already
   doing something similar, invariants enforced in code, cross-context links (shared UUIDs, events).
   Output ≤ 40 lines, `file:line` anchored.
3. For each touched context, load `language.md` + `model.md`. Missing → bootstrap a draft from the
   code per [`./references/contexts.md`](./references/contexts.md) (one confirm question per context).
4. Ask the dev **only** what neither the story nor the code answers — one `AskUserQuestion` call,
   ≤ 4 questions, each with Claude's recommended answer first. Zero questions is a valid outcome.

### 2. Devil's advocate — story vs system

Dispatch [`devils-advocate`](../../agents/devils-advocate.md) in **Mode C** with: the story, the
step-1 answers, the explorer map, the touched contexts' docs paths. It returns ≤ 7 findings,
severity-ordered, each `[code]` (story line + `file:line`) or `[logic]` (story line + a realistic
scenario that it has verified is reachable in the system).

Present each finding as one `AskUserQuestion` (batch ≤ 4 per call):
- option 1 — Claude's recommendation + one-line why **(Recommended)**;
- option 2 — the credible alternative, if there is one;
- option 3 — **«Defer to PM»**;
- free text ("Other") — the dev's own answer.

Record every outcome in `.sdd/stories/<slug>.md`. **If anything was deferred to PM → STOP.** Print a
copy-ready message for the PM (story ref + each question with context + Claude's suggested answer)
and `/sdd:story <slug>` to resume. On resume, ask the dev for the PM's answers and continue from step 3.

### 3. Scope

Classify the change in the repo's own terms and show it as one screen:

- **wiring** — Action + UseCase + DTO, a repository method, a presenter, a CLI command, config;
- **domain** — new/changed entity, VO, enum/state, domain service, invariant, cross-context event;
- **data** — schema change (code-first: entity mapping changes; the migration is generated later),
  plus what happens to **existing rows** (new non-null field, changed enum, backfill).

Then cut it into **vertical slices**: one slice = one behaviour group (a few ACs) that ends with green
tests and carries **≤ 3 domain decisions**. Mechanical code (DTO, wiring, config, generated
migrations, imports/attributes) does not count toward that limit. **> 4 slices** → recommend
splitting the story into several PRs/stories (offer a PM message). One `AskUserQuestion`: accept
the scope + slices / adjust (Other).

### 4. Model — only what the scope demands

| Scope has | Produce | Where |
|---|---|---|
| new or changed entity / VO / aggregate | Mermaid `classDiagram` (only the touched part) + 2–4 lines **what it gives us**: the invariants it guards, why the aggregate boundary is here, cross-context links by UUID | update `docs/contexts/<Context>/model.md` |
| a non-trivial flow — >1 collaborator after the use case, async/Messenger, transaction + locking, external integration, or a state change | Mermaid `sequenceDiagram` of that flow | the same `model.md`, under the flow's name |
| a new term, or an existing term used differently | glossary line (term · definition · NOT-confused-with) | `docs/contexts/<Context>/language.md` |
| wiring only (list/get endpoint, repo method) | nothing | — |

**Code-first.** The model is PHP entities with ORM mapping — never hand-written SQL. Migrations are
produced by the repo's diff tool (e.g. `doctrine:migrations:diff`) **after** the entity slice is
green, and shown to the dev. Diagrams are validated per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md)
and presented as a prose delta, never dumped raw.

One `AskUserQuestion`: model accepted / adjust (Other).

### 5. Agree each slice — interactive, before any code

For the current slice, one `AskUserQuestion` call with **one question per behaviour** (≤ 4):

> **<Behaviour name>**
> I'm doing: <what changes, in domain terms — one or two lines>.
> I'm testing it from: <unit — rule/transition…>; <integration — …>; <functional — request → full response…>.

Options — **there is no "reject"** (a dead-end flow); the dev steers instead:
- «Yes, do it» **(Recommended)**;
- a Claude-proposed variation — an extra case it considered borderline, or a narrower variant;
- free text ("Other") — the dev's own correction.

Test levels and style follow `CLAUDE.md` (e.g. one scenario per test method, full-response
assertions for API tests). Agreed behaviours become the slice's task list (TaskCreate), visible
beside the chat — not a document.

### 6. Build the slice — TDD, no commit

Run the per-task cycle from [`../implement/references/tdd-loop.md`](../implement/references/tdd-loop.md):
`RED → GREEN → REFACTOR → GATE`, with **COMMIT replaced by STOP**. Gate commands come from
`CLAUDE.md` / the detection cascade ([`../implement/references/command-detection.md`](../implement/references/command-detection.md)).
Code-first schema: after the entity changes are green, generate the migration with the repo's tool
and include it in the slice.

**Nothing stays open.** If GREEN hits a decision that was not agreed in step 5:
- it changes behaviour, the model, or a contract (a new state, a locking strategy, a new error the
  client sees) → **stop and ask now**, one `AskUserQuestion` with Claude's recommendation first,
  then continue;
- it's a pure implementation detail that follows `CLAUDE.md` / existing patterns (naming, a private
  helper, which existing exception base class) → just do it, don't mention it.

Nothing is "recorded for later" — no notes, no open-question lists.

### 7. Hand the slice to the dev

Two lines, no report — every decision was already made with the dev in steps 5–6:

- one line: slice name, gate result (`ci:phpunit ✓ phpstan ✓ deptrac ✓ ecs ✓`);
- then: «Review the diff in your IDE and commit it yourself. Say *next* to start slice N+1.»

Never `git commit`, never `git add`. Repeat steps 5–7 per slice. After the last slice, offer
`/sdd:review <slug>` as an **optional** independent review — never a gate.

## Definition of Done

- Every devil's-advocate finding is resolved or was carried to the PM (and answered on resume).
- Touched contexts' `language.md` / `model.md` reflect the change (part of the dev's diff).
- Every behaviour was agreed in step 5 before its code was written; each has its test(s).
- Every decision made during the build was either agreed with the dev or is a convention-following detail; nothing is left open.
- Gate green per slice; nothing committed by Claude.

## Anti-patterns

- **Handing the dev a document to approve** — plans, task lists, tables. Ask decisions instead.
- **Modelling wiring** — a class diagram for a list endpoint.
- **Writing SQL / staging migrations** — this repo is code-first; the diff tool owns migrations.
- **A "reject" option** — it ends the flow; offer a steer instead.
- **Committing** — the dev owns the commit.
- **Re-interviewing the product** — the PM already decided *what*; ask only what blocks *how*.
