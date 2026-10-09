CREATE TABLE IF NOT EXISTS feedback (
    id         UUID PRIMARY KEY,
    lesson_id  UUID          NOT NULL REFERENCES lessons(id),
    author_id  UUID          NOT NULL REFERENCES users(id),
    body       VARCHAR(2000) NOT NULL,
    created_at TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_feedback_lesson_id ON feedback(lesson_id);
CREATE INDEX IF NOT EXISTS idx_feedback_author_id ON feedback(author_id);
