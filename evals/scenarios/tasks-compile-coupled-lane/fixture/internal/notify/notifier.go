package notify

import "context"

// Notifier sends a single notification to one recipient.
type Notifier interface {
	Send(ctx context.Context, to, subject, body string) error
}
