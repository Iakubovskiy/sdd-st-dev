# Rubric — classify-size

PASS requires ALL of:

1. `docs/features/tiny-toggle/.size` exists and its content is exactly ONE bare token from
   {XS, S, M, L, XL} (no comments, no extra lines beyond a trailing newline). For this obvious
   one-line-config fixture, XS or S are the sane classes.
2. `docs/features/tiny-toggle/.route` exists and is exactly one of {quick, standard, full}.
3. The run's final message contains a stage-handoff block (What I did / Review before continuing /
   Run next — the utility variant: resume the backbone stage).

FAIL on a multi-line or annotated `.size`, a missing/malformed `.route`, or no handoff block.
