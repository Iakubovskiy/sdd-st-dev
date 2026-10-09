# Rubric — tasks applies the contract-task rule (no standalone interface-only task)

The fixture holds `spec.md` + `sad.md` + one Accepted ADR (+ `.size` = S, `.route` = quick)
for `batch-notify` — every input the tasks gate requires — plus a Go module where the shared
`internal/notify/notifier.go` `Notifier` interface has **two** existing implementations
(`email.go`, `sms.go`), each pinned by a compile-time `var _ Notifier = (*Impl)(nil)`
assertion. The feature extends `Notifier` with `SendBatch` (sad §5, ADR 0001), so a task that
changes **only** the interface file can never be committed green: the assertions break both
implementers. PASS requires ALL of:

1. `docs/features/batch-notify/tasks.json` exists and is valid JSON matching the skill's
   contract: every task has `id`, `title`, `layer`, `deps`, `acs`, `dod`, `files_hint`;
   `deps` reference only ids present in the file and form an acyclic graph; every spec §5 AC
   (AC-01 and AC-02) appears in at least one task's `acs`.
2. **Key check — no standalone contract task.** There is NO task whose `files_hint` touches
   ONLY `internal/notify/notifier.go` while no other task lists `internal/notify/notifier.go`
   in its `files_hint`. Both resolutions the skill allows are a PASS:
   (a) **fold** — the interface change lives inside an implementing task whose `files_hint`
   contains `notifier.go` TOGETHER with other files (e.g. `email.go` / `sms.go`); or
   (b) **compile-coupled lane** — a separate contract task exists, but `notifier.go` appears
   in the `files_hint` of at least 2 tasks (the shared contract file marks the lane).
3. `docs/features/batch-notify/tasks/_epic.md`, `tasks/tracker.md`, and one `tasks/<task>.md`
   per task all exist.
4. The tail of the run's final message contains the stage-handoff block (*What I did* /
   *Review* / *Run next*).

FAIL if an interface-only task exists with no second task sharing `notifier.go` in its
`files_hint`, or `tasks.json` is missing/invalid, or the run refused — the fixture contains
every gate artifact (spec.md + sad.md + Accepted ADR), so a refusal means the run
misread an intact fixture.
