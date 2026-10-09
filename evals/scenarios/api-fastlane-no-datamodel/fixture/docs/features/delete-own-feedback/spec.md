---
status: approved
---

# Delete own feedback

## 1. Context

Students leave feedback on lessons. Today feedback can only be created and listed; authors
cannot remove their own entries, so support deletes rows by hand. The `feedback` table already
exists — this feature adds **no new entity, column, or index**.

## 2. Goals

- An author can delete their own feedback entry.

## 3. Non-goals

- Moderator/admin deletion of other people's feedback.
- Editing feedback.

## 4. User stories

- US-1: As a student, I delete a feedback entry I authored, so an outdated comment disappears.

## 5. Acceptance criteria

- AC-01 (happy): given a feedback entry I authored, when I delete it, it no longer appears in
  the lesson's feedback list.
- AC-02 (error): given a feedback entry authored by someone else, when I try to delete it, the
  operation is rejected with the documented not-owned outcome and the entry remains.
- AC-03 (error): given a feedback id that does not exist, the delete is rejected with the
  documented not-found outcome.

## 8. Open questions

(none)
