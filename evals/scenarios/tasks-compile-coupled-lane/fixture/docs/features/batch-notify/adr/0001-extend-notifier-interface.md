---
status: Accepted
owner: "Architect"
reviewers: ["Tech Lead"]
updated_at: "2026-07-01"
feature_size: "S"
ticket: "NOTIFY-42"
---

# 0001 — Extend the shared Notifier interface with SendBatch

- **Status:** Accepted
- **Date:** 2026-07-01
- **Deciders:** Architect + user (design walk)

## Context

Callers need batch delivery with per-recipient failure reporting (spec US-1). The notify
module exposes one shared `Notifier` interface with two live implementations (`EmailNotifier`,
`SMSNotifier`), each pinned by a compile-time `var _ Notifier = (*Impl)(nil)` assertion.
Where the batch operation lives determines whether batch semantics stay uniform across
channels.

## Decision drivers

- Batch semantics must be identical for every channel (spec §5 AC-01/AC-02 — per-recipient
  failure reporting is part of the contract, not a caller convention).
- Reuse the existing `internal/notify` module — no new packages or deployment units (sad §2).

## Considered options

1. **Extend `Notifier` with `SendBatch`** — one contract, every implementation must provide
   batch delivery; compile-time assertions enforce completeness.
2. **A separate `BatchNotifier` interface** — implementations opt in; callers must
   type-assert, and channels can silently lack batch support.

## Decision outcome

**Chosen:** Option 1 — extend the existing interface, do not create a separate
`BatchNotifier`. The contract stays single and uniform, and the existing `var _ Notifier`
assertions guarantee at compile time that no implementation ships without batch support.

## Consequences

**Positive**
- One contract; per-recipient failure reporting is uniform across email and SMS.

**Negative**
- The interface change does not compile until **both** existing implementations gain
  `SendBatch` — the change and the implementations cannot land green independently.

**Neutral**
- A future channel implements `SendBatch` from day one; no migration path needed.

## Links

- Spec: [[../spec.md]] (US-1)
- SAD: [[../sad.md]] §5
