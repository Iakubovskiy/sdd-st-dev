---
status: approved
---

# Feedback reactions

## 1. Context

Students leave feedback on lessons. Readers want a lightweight way to acknowledge an entry
without writing a comment. This feature introduces a **new entity — reaction** (an emoji a
student attaches to a feedback entry); no existing table can hold it.

## 2. Goals

- A student can add an emoji reaction to a feedback entry.
- A student can remove a reaction they added.

## 3. Non-goals

- Custom (non-emoji) reactions.
- Reacting to lessons or to other reactions.
- Aggregated reaction analytics.

## 4. User stories

- US-1: As a student, I add an emoji reaction to a feedback entry, so the author sees a quick
  acknowledgement.
- US-2: As a student, I remove a reaction I added, so it no longer counts.

## 5. Acceptance criteria

- AC-01 (happy): given a feedback entry, when I add an emoji reaction, it appears in that
  entry's reaction list.
- AC-02 (happy): given a reaction I added, when I remove it, it disappears from the entry's
  reaction list.
- AC-03 (error): given I already reacted to the same feedback entry with the same emoji, adding
  it again is rejected with the documented duplicate outcome — a reaction is unique per
  author + feedback + emoji.
- AC-04 (error): given a feedback id that does not exist, adding a reaction is rejected with
  the documented not-found outcome.

## 8. Open questions

(none)
