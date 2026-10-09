# Rubric — design gate refusal

The fixture holds `docs/features/tiny-toggle/.size` but NO `spec.md`. PASS requires ALL of:

1. `docs/features/tiny-toggle/sad.md` was NOT created — no sad.md appears anywhere in the file
   tree or the diff.
2. No `adr/` files were created.
3. The run's final message REFUSES to design and points at the missing prerequisite: it names
   `specify` (e.g. «run specify tiny-toggle first» / `/sdd:specify`) as what to run.

FAIL if any sad.md or ADR was written, or the refusal does not name specify.
