# specify — delta over the shared critic

Read [`../../_shared/critic.md`](../../_shared/critic.md) for the canonical dispatch and F1–F6 skeleton. specify supplies only the deltas below; the skill fills the placeholders and dispatches one clean-context `Agent`.

## Placeholders

- **`{{ARTIFACT_NAME}}`** = "Product spec (context / goals / user stories / acceptance criteria / NFRs / KPIs)".
- **`{{DRAFT}}`** = the in-memory `spec.md` draft.
- **`{{EDITS_LOG}}`** = the step-7 edits-log.
- **`{{UPSTREAM_FILES}}`** (the critic Reads these itself):
  - `docs/features/<slug>/CONTEXT.md` — canonical glossary (roles, domain terms).
  - any reference module / doc the user named in step 5 (paths only).

## F5 structural floor (this artifact)

- §4 holds ≥1 US per glossary role + per §2 goal.
- §5 holds ≥1 AC of each of the 5 coverage types **after** drops + OQ-migrations.
- §6 NFR rows all carry a numeric target + measurement (no adjectives, no lone TBD).
- §8 Open Questions has a row for every `save_as_oq` with owner + due.

## F6 specialization — forbidden-token leak (the load-bearing check)

This is specify's primary F6. Scan §5 AC text for the forbidden tokens in [`draft-generation.md`](./draft-generation.md) (HTTP verbs, URL paths, status numerics, `module.error_name` strings, JSON fragments, SQL/driver constructs). **List every hit**, one bullet per AC line:

```
- **[F6] AC-NN contains forbidden tokens** — line: "<verbatim snippet>"; hits: <token1>, <token2>; suggested: rewrite into business form (actor-observable outcome) OR move the HTTP/error/schema detail to `api`.
```

Also flag any concrete technology name (datastore / broker / framework / library) appearing in §1–§3 — those belong to `design`.

## F1 specialization — approach drift

If the edits-log dropped/edited a US or AC tied to the committed approach in §1 ¶3, check that §1 ¶3 still states that approach accurately. A spec whose body no longer matches its own «committed approach» paragraph is drift.
