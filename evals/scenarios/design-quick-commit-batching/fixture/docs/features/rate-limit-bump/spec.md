---
status: approved
---

# Rate limit bump — raise the default per-user rate limit

## 1. Context

Operators keep asking support to raise the default per-user rate limit. It is a single
configuration default in one existing backend service — no new module, no schema change,
no new API surface.

## 2. Goals

- The default per-user rate limit can be raised via configuration without a redeploy.

## 3. Non-goals

- Per-customer overrides.
- Changing the rate-limiting algorithm.

## 4. User stories

- US-1: As an operator, I raise the default rate limit so busy customers stop being throttled.

## 5. Acceptance criteria

- AC-01 (happy): given a higher default is configured, requests under the new limit succeed.
- AC-02 (error): given a request exceeds the configured limit, it is rejected with the
  documented throttling outcome.

## 6. NFR

- A changed default takes effect within 60 seconds of the configuration change (measured
  from config write to the first request evaluated under the new limit).

## 8. Open questions

(none)
