-- STAGED migration for feedback-reactions (not yet promoted to the live migrations/ tree).
CREATE TABLE IF NOT EXISTS feedback_reactions (
    id          UUID PRIMARY KEY,
    feedback_id UUID        NOT NULL REFERENCES feedback(id),
    author_id   UUID        NOT NULL REFERENCES users(id),
    emoji       VARCHAR(16) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_feedback_reactions_author_feedback_emoji
    ON feedback_reactions(author_id, feedback_id, emoji);
