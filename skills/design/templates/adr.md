<!-- Format: MADR (Markdown Any Decision Record). -->
<!-- Spawned by `design` when a decision crosses the blast-radius gate (references/blast-radius.md),
     and also written by `decide-adr` for post-hoc decisions. -->

---
status: Accepted                                # Proposed → Accepted → Superseded by NNNN. `design` writes Accepted directly.
owner: "<decision owner — usually Architect>"   # who is accountable for the decision
reviewers: []                                   # who reviewed before merge (usually Tech Lead, + Security if relevant)
updated_at: "<YYYY-MM-DD>"                       # last update (for Superseded — the date of replacement)
feature_size: "<from .size: XS/S/M/L/XL>"
ticket: "<tracker ticket that triggered the feature>"
---

# NNNN — <title in imperative: e.g. "Use a sliding-window counter for rate limiting">

<!-- IMPORTANT: the title describes the DECISION, not the problem. -->
<!-- ✓ "Store content as a table of typed blocks"  -->
<!-- ✗ "Content storage strategy"                  -->

- **Status:** Accepted
- **Date:** <YYYY-MM-DD>
- **Deciders:** <names — usually the Architect + the user during the Socratic walk>

## Context

<2–4 sentences: what is happening, why this decision must be made now. Pull from sad.md §3 (Context)
+ the section that triggered this ADR.>

## Decision drivers

<bullets — the quality goals / constraints that pushed the choice. Each bullet comes from spec §6 NFR,
or §2 SAD Constraints, or a §1 top-3 quality goal. Don't invent drivers — this filters out pet decisions.>

- <e.g. latency target from spec §6 NFR>
- <e.g. multi-tenant isolation requirement from spec §6.1>
- <e.g. an existing capability already in the stack — no new infra cost>

## Considered options

<List ALL options presented in the AskUserQuestion, including the rejected ones. One line each.
Do NOT add a strawman — an option an existing constraint already excludes (a critic F6 hit).>

1. **<Option A>** — <one sentence>.
2. **<Option B>** — <one sentence>.
3. **<Option C>** — <one sentence>.

## Decision outcome

**Chosen:** Option <letter or name>. <1–2 sentences — why this won over the alternatives, citing the
decision drivers above.>

## Consequences

**Positive**
- <e.g. the dominant quality goal is met naturally>
- <e.g. reuses an existing capability — no new infra>

**Negative**
- <e.g. more memory/space per item than the simpler option>
- <e.g. the logic is a little harder to reason about>

**Neutral**
- <e.g. switching to the alternative later is possible but needs a data backfill>

<!-- An honest consequence log fills Negative and Neutral too, not only Positive. -->

## Links

<!-- Without this section an ADR is an orphan. An ADR lives in three links:
       1) up to the spec (which user story triggered it)
       2) up to a §N of the SAD (which section it attaches to)
       3) sideways to a sibling ADR (if together they form one contract) -->

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §<N>
- Related ADR: <[[NNNN-other]] if any>
