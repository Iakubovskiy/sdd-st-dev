# Rubric — api hard-refuses when data-model.md is missing AND a schema change exists

The fixture holds `spec.md` + `sad.md` (+ `.size` = S, `.route` = quick) for
`feedback-reactions`, live `migrations/` defining the existing tables, and **NO**
`docs/features/feedback-reactions/data-model.md`. Unlike the fast-lane twin, this feature
CHANGES the schema: sad §5 declares a new `reaction` entity (`feedback_reactions` table) and a
**staged** migration sits at `docs/features/feedback-reactions/migrations/01_create_feedback_reactions.up.sql`
(+ `.down.sql`). This is the hard-refuse branch of the api three-way gate. PASS requires ALL of:

1. The run REFUSED and points at the missing prerequisite: the final message names
   `data-model` for this slug (e.g. «run `data-model feedback-reactions` first» /
   `/sdd:data-model feedback-reactions`) as what must run before the contract can be derived.
2. No contract artifact was generated: `docs/features/feedback-reactions/contracts/openapi.yaml`
   — and no `contracts/` directory at all — appears anywhere in the file tree, the git log, or
   the diff. Same for `api-sync-report.md` and `events.md`.
3. The run did NOT create `docs/features/feedback-reactions/data-model.md` itself (nor any stub
   of it) anywhere in the tree, log, or diff — the gate points at the upstream stage; it is
   never self-served.

FAIL if any contract file was written, if the refusal does not name `data-model`, or if the run
wrote a data-model.md to satisfy its own gate.
