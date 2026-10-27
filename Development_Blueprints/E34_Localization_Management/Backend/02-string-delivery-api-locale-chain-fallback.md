# B-02 — String Delivery API & Locale-Chain Fallback

## 1. Feature Context
The single most important guarantee in this entire module: the actual client-facing endpoint every screen in the app calls to render text, structurally incapable of returning a draft/machine-assisted translation or a raw internal key — because its query only ever selects published rows, and any gap resolves through a chain that is mathematically guaranteed to terminate in a fully-covered locale.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
1.2 String Delivery API & Locale-Chain Fallback (ID: **B-02**)

## 4. Objective
Build `GET /v1/strings`, querying exclusively `status='published'` version rows, with recursive locale-chain fallback resolution terminating in a database-constrained, always-active, 100%-covered terminal locale (English).

## 5. Business Requirements
- FR-3: draft/machine translations flagged and never served to children; missing translations fall back through an explicit locale chain rather than rendering a raw key.
- §3.4/§3.5: only `status='published'` string versions are ever included in this response, structurally excluded, never client-side filtered; chain resolution never bottoms out into a raw key.
- §5 Backend AI prompt items 1–2: structural exclusion of unreviewed translations (highest priority in the entire deliverable); recursive multi-level locale-chain resolution with a DB-constrained terminal locale.
- Edge Case 3: a multi-level fallback gap still resolves to the guaranteed terminal locale, never bottoming out.

## 6. Existing Architecture
`localization` bounded context, `app/localization/routers/string_delivery_router.py` — the actual public/client-facing contract, heavily cached (Redis, per-locale bundle), invalidated on publish events.

## 7. Existing Code to Reuse
- B-01's `locale_string`/`locale_string_version` schema (read-only consumption here)
- Redis caching infrastructure (existing platform pattern)

## 8. Files to Create
- `app/localization/routers/string_delivery_router.py`
- `app/localization/services/string_delivery_service.py`
- `app/localization/repositories/string_delivery_repository.py` — the query that structurally filters to `status='published'` only
- `app/localization/services/locale_chain_resolver.py` — recursive fallback logic
- `app/localization/schemas/string_delivery_schema.py`
- `alembic/versions/xxxx_add_terminal_locale_constraint.py`

## 9. Files to Modify
- `app/localization/routers/__init__.py` — register router

## 10. Backend Requirements
- `StringDeliveryRepository.get_published()`: the query's `WHERE` clause hardcodes `status = 'published'` — there is no parameter or code path that could widen this filter; this is the structural guarantee, not a default that a caller could override.
- `LocaleChainResolver.resolve()`: for a requested `(key, locale_code)` with no published version, recursively walks `locale_chain_config.fallback_locale_code` until a published version is found; if the chain is somehow exhausted before reaching a published version (should be structurally impossible given the terminal-locale constraint), the key is omitted from the response entirely — never the raw key string.
- Database migration adds a `CHECK`/trigger on `locale` ensuring the designated terminal locale (English) cannot be set `active=false` while it remains any locale's chain terminus, and a separate integrity job (or a `CHECK`-adjacent trigger) that would reject any state leaving English below 100% published coverage — confirmed as the practical backstop making chain exhaustion structurally impossible.
- Redis cache invalidated per-locale-bundle on any `publish` transition (B-05's review-completion event).

## 11. Required API / API Contract
`GET /v1/strings?locale=&keys=` → `200 { "ur.home.greeting": "...", "ur.habit.streak_label": "..." }`.

## 12. Database Requirements
Reads `locale_string_version` (structural `status='published'` filter), `locale_chain_config`. Migration: `CHECK`/trigger preventing the terminal locale from being deactivated or falling below 100% published coverage.

## 13. Validation
`locale` must reference an existing locale; `keys` a non-empty list.

## 14. Authentication
Public/service-to-service auth appropriate for a high-volume client-facing endpoint (standard app-client auth, not admin auth — distinct from every other endpoint in this module).

## 15. Authorization
No admin scope — this is the consumer-facing contract, authenticated via the standard mobile/web client auth mechanism.

## 16. Error Handling
Missing key after full chain exhaustion: omitted from response (not an error, not a raw key). Invalid `locale`: `400`.

## 17. Security
This is the module's defining guarantee. Mandatory test: a fixture string with only a `draft` or `machine_assisted` version (explicitly no `published` version) is NEVER returned by this endpoint for that locale, regardless of how complete its draft content looks. Second mandatory test: a multi-level fallback (e.g., `ur → en`) correctly resolves, and the terminal locale is confirmed database-CONSTRAINED to always remain active — this constraint, not application logic alone, is the practical guarantee against ever bottoming out into a missing-key scenario.

## 18. Analytics
`locale_chain_fallback_triggered` (internal/quality signal) per §1.19 — logged whenever a requested key resolves via fallback rather than a direct published translation in the requested locale, feeding the translation-completeness quality dashboard.

## 19. Performance
Redis-cached per-locale bundle, invalidated on publish; this is explicitly called out (§10 DevOps) as a high-call-volume, latency-sensitive service consumed by every client screen render.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Redis client. No new libraries.

## 21. Testing
Unit: chain-resolution recursion logic. Integration: **mandatory** — draft/machine-assisted-only string never returned regardless of content completeness; **mandatory** — multi-level fallback resolves correctly, and an attempt to deactivate/under-cover the terminal locale is rejected by the DB constraint; cache-invalidation-on-publish test.

## 22. Documentation
OpenAPI docstring explicitly stating this endpoint structurally cannot return unreviewed content, with a link to the guardrail rationale doc.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for the Terminal-Locale Constraint**
Objective: `CHECK`/trigger preventing terminal-locale deactivation or sub-100% coverage. Files: `alembic/versions/xxxx_add_terminal_locale_constraint.py`. Tests: **mandatory** — direct DB-level attempt to deactivate/under-cover the terminal locale is rejected. Definition of Done: test passes.

**Task 02 — Implement `StringDeliveryRepository` with Hardcoded Published Filter**
Objective: Query with no parameterizable status filter. Files: `repositories/string_delivery_repository.py`. Dependencies: B-01's schema. Tests: **mandatory** — draft/machine-assisted-only fixture never returned. Definition of Done: test passes.

**Task 03 — Implement `LocaleChainResolver`**
Objective: Recursive fallback resolution. Files: `services/locale_chain_resolver.py`. Dependencies: Task 02. Tests: **mandatory** — multi-level fallback resolution test. Definition of Done: test passes.

**Task 04 — Implement `StringDeliveryService`**
Objective: Compose repository + resolver, omit-not-raw-key on full exhaustion. Files: `services/string_delivery_service.py`. Dependencies: Task 02, Task 03. Tests: exhaustion-omits-key test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoint with Redis Caching**
Objective: `GET /v1/strings`, cached per-locale bundle. Files: `routers/string_delivery_router.py`. Dependencies: Task 04. Tests: endpoint integration + cache-hit tests. Definition of Done: tests pass.

**Task 06 — Wire Cache Invalidation on Publish**
Objective: Publish events (B-05) invalidate the relevant locale-bundle cache entry. Dependencies: Task 05, B-05. Tests: invalidation-on-publish test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm the published-status filter is genuinely hardcoded with zero override path, and the terminal-locale constraint is enforced at the database level, not just application logic. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Query structurally filters to `status='published'` only, no override path exists — mandatory test passing
- [ ] Multi-level locale-chain fallback resolves correctly — mandatory test passing
- [ ] Terminal locale is database-constrained to remain active and fully covered — mandatory test passing
- [ ] Full chain exhaustion omits the key, never returns a raw key string
- [ ] Redis cache invalidates correctly on publish events

## 25. Definition of Done
Every child/parent-facing client consumes a string table that is structurally guaranteed to never leak an unreviewed translation or a raw key, with a mathematically-backstopped fallback chain — this module's single highest-priority engineering guarantee.
