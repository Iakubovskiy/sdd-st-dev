package notify

import "context"

// EmailNotifier delivers notifications over SMTP.
type EmailNotifier struct {
	Host string
}

// Compile-time check: EmailNotifier must satisfy Notifier.
var _ Notifier = (*EmailNotifier)(nil)

func (e *EmailNotifier) Send(ctx context.Context, to, subject, body string) error {
	// Stub: a real implementation would talk to an SMTP server.
	return nil
}
