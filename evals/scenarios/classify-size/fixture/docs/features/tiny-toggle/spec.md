---
status: draft
---

# Tiny toggle — raise the default rate limit

## 1. Context

Operators keep asking support to raise the default per-user rate limit. It is a single
configuration default in one existing service — no new module, no schema change, no new API.

## 2. Goals

- The default limit can be changed without a redeploy.

## 3. Non-goals

- Per-customer overrides.

## 4. User stories

- As an operator, I change the default rate limit so busy customers stop being throttled.

## 5. Acceptance criteria

- AC-01 (happy): given a new default is configured, requests under the new limit succeed.
- AC-02 (error): given a request exceeds the configured limit, it is rejected with the
  documented throttling outcome.

## 8. Open questions

(none)
