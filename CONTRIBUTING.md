# Contributing

## Skills

A skill lives in `skills/<name>/SKILL.md`: frontmatter (`name` = the dir name, a third-person
`description` with trigger phrases in EN + UA, `agents: [...]`) and a numbered protocol.

- **Follow the house rules** ([`skills/_shared/house-rules.md`](./skills/_shared/house-rules.md)) and
  link them — never restate them at length. Claude never commits; every stop is one screen of
  decisions; no "reject" options; nothing left open.
- **Shared mechanics live once** in `skills/_shared/` (`tdd-loop`, `contexts`, `mermaid-check`).
- **Keep it short.** A skill is read on every run — every line costs tokens for every dev.
- **Name the structural self-check** (usually the gate) in the Definition of Done.

## Agents

`agents/*.md` with `name` / `description` / `model` frontmatter. Use the cheapest tier that does the
job: `sonnet` for scouting and bounded checks, `opus` only for open-ended judgment.

## Before a PR

```bash
python3 scripts/validate_plugin.py
```

The same check runs in CI. Upstream lives at `genkovich/sdd` (remote `upstream`) — pull from it
selectively; this fork deliberately dropped most of its pipeline.
