# Bounded-context docs — `docs/contexts/`

> **Reference-only.** Docs describe **bounded contexts** (modules / sub-domains), not features.
> A feature is a change *to* a context; the context docs are what the next dev — or Claude — reads
> first to speak that context's **Ubiquitous Language**.

## Layout

```
docs/contexts/
  README.md            ← context map: one line per context + relations (events, shared UUIDs)
  <Context>/
    language.md        ← the context's Ubiquitous Language
    model.md           ← aggregates (classDiagram) + named flows (sequenceDiagram) + decision log
```

`<Context>` = the module directory name (e.g. `Account`, `Identity`, `Trip`).

## language.md

```md
# <Context> — Ubiquitous Language

## Terms
- **<Term>** — <one-sentence meaning in THIS context>. NOT <the homonym / neighbouring concept>.

## Invariants
- <X always must / can never …>  (source: `path/File.php:line`)
```

The same word may mean different things in different contexts — that's the point. Example: `Driver`
in Account (an earning balance holder) vs `Driver` in Identity (a person who can log in) — same UUID,
different concept. Each context defines its own; neither is "the" Driver.

## model.md

```md
# <Context> — Model

## Aggregates
```mermaid
classDiagram
  ...only aggregates, key VOs/enums, and cross-context references (as UUID fields, not associations)
```
<2–4 lines: what each aggregate guards>

## Flows
### <Flow name>
```mermaid
sequenceDiagram
  ...
```

## Decisions
- <date> · <story slug> — <decision> because <reason>.
```

## Bootstrap (no docs yet)

When `story` touches a context with no `docs/contexts/<Context>/`:

1. Draft from code only — entities, VOs, enums (with their cases/transitions), domain services,
   events published/consumed. No guessing beyond what the code states.
2. Show the dev a 5-line summary of the draft (term count, aggregates, invariants found) and one
   `AskUserQuestion`: accept draft / correct (Other).
3. Add a row for the context to `docs/contexts/README.md` (create it if absent).

The bootstrap is per touched context, never repo-wide — docs grow where work happens.

## Updating

`story` step 4 edits only the touched sections. Every edit lands in the dev's diff, so it gets the
same review as the code. Never rewrite a whole file to change one aggregate.
