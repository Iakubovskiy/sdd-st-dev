# Review checklist — what `task-review` hunts for

> **Reference-only.** Not a skill. The `reviewer` agent checks the diff against this list — a fixed
> list is cheaper and quieter than an open-ended "find problems". Things the repo's config and gate
> already enforce (HTTP client timeouts, endpoint access rules, style, static analysis) are **not** re-checked.

## Everywhere

- **Infinite recursion and event loops** — a function / listener / handler that can call or trigger
  itself without a guaranteed exit (an event handler that re-dispatches its own event, a setter that
  fires the change it reacts to).
- **Race conditions** — check-then-act on shared state (read → decide → write without a lock / unique
  constraint / atomic update), two requests or taps hitting the same resource.
- **Retries without idempotency** — a retried call / message / webhook that applies twice.
- **Swallowed errors** — empty catch, error turned into a success / default value silently.
- **Secrets or personal data in logs.**

## Backend

- **N+1** — a query or lazy association access inside a loop (look at the loop + the repository /
  ORM call it makes).
- **Missing index** for a new query's filter / join / order column.
- **Unbounded reads** — `findAll()` / queries without limit or pagination on a growing table, loading
  a whole collection into memory.
- **Memory leaks** — long-running workers / consumers / commands that accumulate: the ORM unit of work
  never cleared, static or service-level caches / arrays that only grow, listeners added per message.
- **Deadlocks** — rows / tables locked in different orders on different paths; long transactions
  holding locks.
- **External calls inside a transaction** (HTTP, queue publish before commit).
- **Duplicates under concurrency** — no unique constraint / idempotency key for webhooks, messages,
  "create if not exists".
- **ORM pitfalls** — `flush()` inside lifecycle listeners, circular references in serialization.

## Web

- **Memory leaks** — event listeners, intervals / timeouts, watchers, store subscriptions, observers
  not removed on unmount.
- **Reactivity loops** — a watcher / effect that writes the state it watches; computed with side effects.
- **Request races** — an older response overwriting a newer one (no abort / no "latest only"), state
  set after the component is gone.
- **Double submit / duplicate requests.**
- **Huge lists without virtualization / pagination.**
- **XSS** — raw HTML rendering (`v-html`, `innerHTML`, `dangerouslySetInnerHTML`) of user data.
- **Tokens in `localStorage`**, SSR hydration mismatches.

## Mobile (Flutter / Android / iOS)

- **Memory leaks** —
  Flutter: controllers, `StreamSubscription`s, listeners, timers without `dispose` / `cancel`;
  Android: coroutines / flows collected outside a lifecycle-bound scope, `Context` / views held by
  singletons or long-lived objects;
  iOS: retain cycles in closures without `[weak self]`, delegates not `weak`, observers / Combine
  subscriptions never cancelled.
- **Rebuild / recomposition loops** — `setState` / emit / state change during build; `LaunchedEffect` /
  `remember` with unstable keys; SwiftUI `onChange` / `onAppear` writing the state it reacts to.
- **Main-thread work** — I/O, JSON parsing, image decoding, DB on the UI thread.
- **Work after the screen is gone** — callbacks updating disposed state, background → resume, state
  lost after process death.
- **Double taps** starting the same action twice; **offline queue duplicates**.
- **Unbounded caches** — images / responses without size limits.
