# Surfaces — what changes per stack

> **Reference-only.** Not a skill. `story`, `small-task` and `fix` detect the surface of the repo
> they run in and take the stack-specific rules from here: what a *context* is, what to model, how
> schema changes happen, which test levels exist. Everything else (house rules, devil's advocate,
> agree-before-code, the TDD loop) is the same everywhere. `CLAUDE.md` always wins over this table.

## Detect (first match; a monorepo can have several — work per touched directory)

| Signal | Surface |
|---|---|
| `composer.json` with `symfony/*` | **backend-symfony** |
| `package.json` with `@nestjs/*`, `express`, `fastify`, `koa` (no UI framework) | **backend-node** |
| `package.json` with `vue` / `nuxt` (or `react` / `next`, `svelte`, `angular`) | **web** |
| `pubspec.yaml` with `flutter` | **flutter** |
| `build.gradle(.kts)` + `AndroidManifest.xml` | **android** (Kotlin) |
| `*.xcodeproj` / `*.xcworkspace` / `Package.swift` with iOS targets | **ios** (Swift) |

## Context — what `docs/contexts/<Context>/` maps to

| Surface | A context is | Example |
|---|---|---|
| backend-symfony | a module under `src/Module/<Name>` | `Account`, `Trip` |
| backend-node | a module / bounded folder (`src/modules/<name>`, Nest module) | `billing` |
| web | a feature folder (`src/features/<name>`, `src/modules/<name>`) or a route area | `checkout` |
| flutter | a feature (`lib/features/<name>`) | `onboarding` |
| android | a feature module (`:feature:<name>`) or package | `feature-profile` |
| ios | a feature module / SPM package / folder | `ProfileFeature` |

Frontend and mobile contexts mirror the backend's language where they show the same thing — reuse
the backend term (`Trip`, `Payout`) rather than inventing a UI synonym.

## Model — what to draw, and when (story step 4)

Draw only what the scope has. Wiring (a field, a list screen bound to an existing endpoint) → nothing.

| Surface | Scope has | Diagram |
|---|---|---|
| backend-* | new / changed entity, VO, aggregate | `classDiagram` + what it guards |
| backend-* | >1 collaborator after the use case, async (Messenger / queues), transaction + locking, external integration | `sequenceDiagram` |
| backend-* | an entity status with transitions | `stateDiagram-v2` |
| web, flutter, android, ios | a screen / feature with **more than load → show**: loading / empty / error / retry / offline / partial / pagination | `stateDiagram-v2` of the screen state (BLoC / ViewModel / store states and the events between them) |
| web, flutter, android, ios | a new or changed **navigation flow**: several screens, auth / permission branches, deep links, back-stack rules | `flowchart` |
| web, flutter, android, ios | app ↔ API ↔ local storage choreography: offline sync, token refresh, optimistic update, push → screen | `sequenceDiagram` |
| flutter, android, ios | new local models / repositories / cache | `classDiagram` (local side only) |

## Schema & persistence

| Surface | Rule |
|---|---|
| backend-symfony | **Code-first**: change the ORM mapping; generate the migration with the repo's diff tool (`doctrine:migrations:diff`) once the entity change is green; never hand-written SQL. Existing rows are a devil's-advocate question. |
| backend-node | Follow the repo's ORM (TypeORM / Prisma / MikroORM / Drizzle): its generate command, never hand-written SQL where it generates. |
| web | No schema. Client-side storage (localStorage / IndexedDB) changes need a version / migration of the stored shape. |
| flutter | Local DB (Drift / Isar / Hive / sqflite): bump the schema version and write the migration step the library expects; old data on the device is the "existing rows" question. |
| android | Room: bump the version + an `AutoMigration` or a `Migration`; export the schema if the repo does. |
| ios | Core Data / SwiftData: a new model version + lightweight or custom migration; GRDB: a registered migration. |

## Test levels (the "I'm testing it from …" line)

| Surface | Levels |
|---|---|
| backend-symfony | unit (domain rule) · integration (persistence, handlers) · functional (request → full response, per `CLAUDE.md`) |
| backend-node | unit · integration (DB / queue) · e2e (HTTP) |
| web | unit (store / composable / util) · component (Vue Test Utils / Testing Library) · e2e (Playwright / Cypress) — whichever the repo has |
| flutter | unit (BLoC / cubit / repository) · widget · integration (`integration_test`) |
| android | unit (ViewModel / use case, JUnit) · instrumented / Compose UI test |
| ios | unit (XCTest / Swift Testing) · UI test (XCUITest) |

For `fix` on a client: UI-only bugs that can't be pinned below the UI level get a widget / component
test; a device- or OS-specific bug that can't be reproduced in tests is treated like an external
integration in `fix` step 3 — evidence instead of proof, our handling pinned with a fake.

## Usual suspects for `fix`, per surface

- **backend**: existing DB rows, transactions / locking, time zones, money rounding, async ordering.
- **web**: stale cache / store not reset, race between requests, hydration, time zones in the browser.
- **mobile**: lifecycle (background / resume / process death), stale local cache vs server, offline → online,
  token expiry mid-flow, OS-version / device differences, permissions denied, double taps.
