package notify

import "context"

// SMSNotifier delivers notifications over an SMS gateway.
type SMSNotifier struct {
	Gateway string
}

// Compile-time check: SMSNotifier must satisfy Notifier.
var _ Notifier = (*SMSNotifier)(nil)

func (s *SMSNotifier) Send(ctx context.Context, to, subject, body string) error {
	// Stub: a real implementation would call the SMS gateway.
	return nil
}
