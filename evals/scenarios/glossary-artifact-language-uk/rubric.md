# Rubric — glossary-artifact-language-uk

The fixture's `.claude/sdd.local.md` sets `artifact_language: uk`; the prompt supplies two term
definitions in English and never names a language itself — so Ukrainian prose can only come from
the skill honouring the setting.

PASS requires ALL of:

1. `docs/features/rate-limit-bump/CONTEXT.md` exists with **English structure**: the `## Glossary`
   heading verbatim (never «Глосарій»), no other Ukrainian/translated headings anywhere in the
   file, and English frontmatter keys+values (`status: Living`, `updated_at: <date>`).
2. Both terms (`quota window`, `burst credit`) appear under `## Glossary`, one line each in the
   `- <term> — <definition>.` shape, and **each definition's prose is Ukrainian** (Cyrillic carries
   the meaning — e.g. «ковзний 60-секундний інтервал…», not the English sentence copied verbatim).
   The `quota window` entry keeps a NOT-boundary (`NOT` token or an equivalent Ukrainian boundary
   clause naming the billing period).
3. No `<!-- … -->` template comments are copied into the written file, in any language.
4. The run's final message contains a stage-handoff block (What I did / Review before continuing /
   Run next — the utility variant: resume the backbone stage).

FAIL on: English-only definitions (the setting was ignored), a translated `## Glossary` heading or
translated frontmatter (structure leaked into the switch), leftover template comments, a missing
term, or no handoff block.
