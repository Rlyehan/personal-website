import * as Sentry from '@sentry/react';
import { Integrations } from '@sentry/tracing';

const sentryDsn = 'your-sentry-dsn';

Sentry.init({
  dsn: sentryDsn,
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0, // Set the sample rate for performance monitoring (0.0 to 1.0)
});
