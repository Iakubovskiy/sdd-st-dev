# Architecture map — feedback-svc

## Modules

- `internal/feedback` — lesson feedback (handler → service → repo).
- `internal/lesson` / `internal/user` — owning modules for lessons and users.

## Migrations

- Tool: golang-migrate, sequential 6-digit numbering (`000001_*.up.sql` / `.down.sql`)
  in the live `migrations/` tree.
- Current head: `000002_create_feedback`.

## Conventions

- Errors: neutral `module.error_name` codes (e.g. `feedback.not_found`).
- API: REST under `/api/v1`, Bearer auth, cursor pagination, error envelope
  `{code, message, details?}`.
- IDs: UUID; audit column `created_at` only (no `updated_at`).
