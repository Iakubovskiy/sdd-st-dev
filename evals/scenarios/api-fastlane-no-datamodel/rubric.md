# Rubric — api accepts the legal fast-lane skip (no data-model.md, no schema change)

The fixture holds `spec.md` + `sad.md` (+ `.size` = S, `.route` = quick) for
`delete-own-feedback`, live `migrations/` defining the existing `feedback` table, and **NO**
`docs/features/delete-own-feedback/data-model.md`. The feature changes no schema (sad §5:
no new building blocks/entities; no staged `docs/features/delete-own-feedback/migrations/`).
PASS requires ALL of:

1. The run did NOT refuse and did NOT demand `data-model`: the final message contains no
   «run `data-model` … first» bounce, and no stub `data-model.md` was created just to satisfy
   a gate.
2. `docs/features/delete-own-feedback/contracts/openapi.yaml` was written and defines the
   delete operation (a DELETE on a feedback resource) with error responses beyond the happy
   path (the not-owned / not-found branches from the sad §6 `alt`).
3. The sync report (`contracts/api-sync-report.md`) or the final message names the **legal
   skip** — data-model.md absent + no schema change — and traces field origins to the
   **existing schema** (e.g. an origin like «existing schema — 000002_create_feedback»),
   not to invented columns.
4. The run's final message ends with the stage-handoff block (*What I did* / *Review* /
   *Run next*, pointing at `/sdd:tasks delete-own-feedback`).

FAIL if the run refused or bounced to `data-model`, invented fields with no origin in any
input, or wrote a `data-model.md` to appease the gate.
