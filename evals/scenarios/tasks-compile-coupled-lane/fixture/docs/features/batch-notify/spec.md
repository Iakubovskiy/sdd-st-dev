---
status: approved
---

# Batch notify

## 1. Context

The service notifies users one at a time through the shared `Notifier` interface
(`internal/notify`), which has two implementations: email and SMS. Course announcements need
to reach many recipients in one call; today the caller loops and loses track of which sends
failed.

## 2. Goals

- A caller can send one notification to a batch of recipients in a single operation and learn
  exactly which recipients failed.

## 3. Non-goals

- New notification channels (push, webhooks).
- Scheduling / deferred delivery.
- Retry policies — the caller decides what to do with failed recipients.

## 4. User stories

- US-1: As a course operator, I send one announcement to a list of recipients and get back the
  list of recipients that could not be reached, so I can follow up only where delivery failed.

## 5. Acceptance criteria

- AC-01 (happy): given a batch of recipients, when I send an announcement, every recipient in
  the batch receives it and the result reports zero failures.
- AC-02 (error): given a batch where some deliveries fail, when I send an announcement, the
  operation completes for the reachable recipients and the result names each failed recipient
  with the documented failure outcome.

## 8. Open questions

(none)
