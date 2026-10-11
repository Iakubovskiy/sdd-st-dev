# Inputs — design and API contracts

> **Reference-only.** Not a skill. `story`, `small-task` and `fix` accept, besides the task text, a
> design source and an API contract. Both are optional; both are read **narrowly** — only the parts
> the task touches — because screenshots and full specs are the most expensive things to put in context.

## Design

Ask once — only for work that touches UI (web / mobile surfaces, per [`surfaces.md`](./surfaces.md))
and only when the dev gave no design:

1. **Figma MCP connected** (a Figma tool is in the session) and the dev gave a Figma link → use it:
   fetch only the frames / nodes the link points to (structured data first, an image only when
   layout matters). Not connected → don't suggest connecting it; go to 2.
2. **Screens folder.** Create `docs/design/<slug>/` (one folder per story / task / bug) and tell the
   dev in one line where to put the screenshots (exported frames, one state per file, any names).
   Then **one `AskUserQuestion`** — this blocks the skill until answered, so the run continues from
   the same step afterwards:
   - «Done — screens are in `docs/design/<slug>/`» **(Recommended)**;
   - «No design for this»;
   - Other.
   «Done» → list the folder, read the images (≤ 10; more → ask which ones matter). Empty folder →
   say so and ask again once.
3. No design → continue; UI states come from the story + existing screens in code.

What the design is used for: the screen states and navigation to model ([`surfaces.md`](./surfaces.md)),
the devil's-advocate check «story vs design», and the agree-before-code line («building screen X as in
`docs/design/<slug>/02-empty.png`»).

## API contract (Swagger / OpenAPI)

The dev may paste a link to the Swagger UI, to the JSON / YAML, or a path to a downloaded file.

1. **Find the JSON.** From a UI link, derive the spec URL; try in order, stop at the first `200`
   with JSON/YAML:
   - the URL the UI page itself loads (`curl` the page, look for `url:` / `spec-url` / `*.json`);
   - nelmio (Symfony): `/api/default.json` (area `default`; other areas `/api/<area>.json`), `/api/doc.json`;
   - `/openapi.json`, `/swagger.json`, `/v3/api-docs`, `/swagger/v1/swagger.json`, `/api-docs`.
2. **Download** with `curl` from the dev's machine (so staging / VPN the dev can reach works) into
   `.sdd/api/<host>.json` (`.sdd/` is gitignored — add it if missing). Re-use the file in the same
   session; re-download when the dev says the API changed.
3. **`401` / `403` / login page** → don't ask for credentials. Ask the dev to download the JSON in their
   browser and give the file path (one `AskUserQuestion`: «Saved — path: …» / «No contract» / Other).
4. **Read narrowly.** Never read the whole spec into context. Extract with `jq` (or `python -c`) only
   the paths, methods and `components.schemas` the task touches (follow `$ref`s one level at a time).

What the contract is used for: request / response models and error codes on the client, mocks /
fixtures in tests that match the real schema, and the devil's-advocate check «story vs contract»
(a field the story needs that the API doesn't return → «Ask backend»).
