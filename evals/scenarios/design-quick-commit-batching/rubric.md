# Rubric — design batches commits on route quick + depth easy

The fixture holds `spec.md` (+ `.size` = S, `.route` = quick) for `rate-limit-bump` and nothing
else — greenfield, no source code, no `docs/architecture-map.md`. The design skill's step-6
Commit cadence says: on route `quick` + depth `easy`, sections are still written to disk as they
resolve, but commits **batch — at most 3 for the pass** (or a single `design: <slug> sad (quick)`
commit for an uninterrupted pass) on top of the step-4 bootstrap commit — instead of the default
per-section commit (which would produce ~12–14 commits). PASS requires ALL of:

1. `docs/features/rate-limit-bump/sad.md` exists, all 12 Arc42 sections (§1–§12) are filled
   OR carry an explicit `<!-- N/A: <reason> -->` marker, and its frontmatter `target_surfaces`
   is non-empty.
2. **Commit count (the key check).** Count the commits in the git log made after the fixture
   commit `baseline`: there are **at most 4** in total (the step-4 bootstrap commit
   `design: … bootstrap sad.md` plus up to 3 batched section/finalization commits). Fewer is
   also PASS — one or two commits after `baseline` (e.g. a single `design: rate-limit-bump
   sad (quick)`) satisfies this item. **FAIL if there are 5 or more commits after `baseline`**
   — that means the per-section cadence leaked into quick+easy.
3. The sections really landed on disk: `sad.md` with its section content is present in the
   file tree (committed, or visible in the uncommitted diff) — batching commits did not cancel
   the write-after-resolve behavior.
4. The tail of the run's final message contains the stage-handoff block (*What I did* /
   *Review* / *Run next*), and *Run next* points at a next SDD stage — `/sdd:sequences
   rate-limit-bump`, or an auto-skip to `/sdd:data-model rate-limit-bump` or
   `/sdd:api rate-limit-bump`: ANY of these is legal on route quick; do not require one
   specific stage.

FAIL if there are 5+ commits after `baseline`, if `sad.md` is missing or has unfilled sections
without an `<!-- N/A: … -->` marker, or if the final message lacks the handoff block.
