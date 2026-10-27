# B-01 — Favorite Toggle API

## 1. Feature Context
Part of Feature B.14 Favorites — NoorHeroes Islamic Learning App for Children. This blueprint covers the content-type-agnostic add/remove toggle endpoint consumed identically by Stories (A.3), Quran/Arabic (A.5), and Dua Learning (A.6) detail screens.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
1.1 Favorite Toggle API — `B-01`

## 4. Objective
Implement a single, idempotent, optimistic-safe `POST /v1/favorites` endpoint that adds or removes a favorite for any favoritable content type, re-validating content accessibility on add only, and guaranteeing zero duplicate rows under concurrent or repeated requests.

## 5. Business Requirements
- FR-5: toggle is idempotent and optimistic — rapid repeated taps never produce a duplicate record or inconsistent final state.
- FR-6: favoriting never bypasses age-band/entitlement/unlock-state restrictions; the add path re-validates access server-side.
- Removal has no accessibility gate — a child can always unfavorite something regardless of current accessibility (Edge Case 2, Edge Case 9).
- Source: PRD §1.7 FR-5/FR-6, §3.4 `POST /v1/favorites`, §5 AI Code-Generation Prompt items 1–2.

## 6. Existing Architecture
FastAPI modular monolith, `src/noorheroes/modules/content/` bounded context (`api.py`, `service.py`, `repository.py`, `models.py`, `schemas.py`). Auth via `Depends(get_current_child)` → `ChildSessionContext(family_id, child_id, session_id)`. Errors via `DomainError` subclasses in `core/exceptions.py` (`ValidationError`→422, `AuthorizationError`→403, `ConflictError`→409). No manual commits in service/repository layer — commit happens in `get_db_session`.

**Note (from cross-blueprint research):** A.3 already ships `POST /v1/favorites` / `DELETE /v1/favorites/{episode_id}` on `ContentRouter`, scoped to `episode_id` only, no `content_type`. This blueprint's single-endpoint `POST` with a `favorited: bool` body flag supersedes that shape once B-03's schema reconciliation lands. Do not implement this blueprint before B-03's migration is applied, or implement both in the same PR with B-03 as the first commit.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_child`
- `core/exceptions.py` (`NotFoundError`, `ValidationError`, `AuthorizationError`)
- `common/base_service.py`, `common/base_repository.py`
- `src/noorheroes/modules/content/favorite_models.py::FavoriteOrm` (post-B-03 generic shape)

**Resolved research finding — no existing accessibility-check interface to reuse:** a targeted search of A.3's (`09-story-favorites-api.md`) and A.6's (`04-dua-favorites-api.md`) backend blueprints, plus a repo-wide grep for `can_access`/`check_access`/`AccessibilityChecker`/`is_unlocked`/`entitlement_check`, found no per-content accessibility-check interface anywhere in the codebase. The only accessibility-adjacent service found (`C24_Subscription_Billing/Backend/06-platform-entitlement-check-service.md` — `SubscriptionService.get_entitlement()` / `EntitlementRepository.check(feature, childId)`) is plan-level *subscription entitlement*, not per-episode/per-surah/per-dua age-band or unlock-state accessibility. **This means the content-type-dispatched accessibility check FR-6 requires is a genuinely new capability, not a reuse of an existing interface.** Task 05 below reflects this — it must be designed in coordination with A.3/A.5/A.6's module owners (each of whom presumably has *some* internal notion of "can this child open this episode/surah/dua right now," even if it isn't exposed as a named service today), rather than assumed to already exist.

## 8. Files to Create
- `src/noorheroes/modules/content/favorite_schemas.py` (if not already covering `content_type`/`content_id`) — `FavoriteToggleRequest`, `FavoriteToggleResponse`
- `tests/modules/content/test_favorite_toggle_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add/modify `POST /v1/favorites`
- `src/noorheroes/modules/content/service.py` (or `favorite_service.py`) — `FavoriteService.toggle(child_id, content_id, content_type, favorited, client_request_id)`
- `src/noorheroes/modules/content/repository.py` (or `favorite_repository.py`) — upsert/delete logic

## 10. Backend Requirements
- Single endpoint handles both add and remove via `favorited: bool`.
- Add path: call content-type-dispatched accessibility check before write; reject gracefully (not a crash) if inaccessible.
- Remove path: no accessibility check; always succeeds if a row exists, no-op success if not.
- Idempotency via `client_request_id` — unique constraint or dedupe lookup before insert.
- Database-level `UNIQUE(child_id, content_id, content_type)` as the second, authoritative line of defense against duplicates.

## 11. KMP Requirements
Consumed by K-01 (Shared Favorite Toggle Component) and K-03 (Favorites Repository). No KMP code in this blueprint; contract only.

## 12. NextJS Requirements
Not applicable — this is a child-facing user API, not surfaced in Admin.

## 13. API Contract
**Required API:** Favorite Toggle
**HTTP Method:** `POST`
**Endpoint:** `/v1/favorites`
**Request:**
```json
{
  "content_id": "string",
  "content_type": "story|surah|dua",
  "favorited": true,
  "client_request_id": "uuid"
}
```
**Response 200:**
```json
{ "favorited": true }
```
**Authentication:** Bearer (child-mode)
**Authorization:** Requesting child's own session only; `content_id` ownership is not required (any accessible content), but accessibility is required for `favorited:true`.
**Validation:** `content_type` must be in the extensible allowlist; `content_id` syntactically valid for its type.
**Error Responses:** `401` unauthorized (missing/invalid token), `403` inaccessible content (add path only), `422` invalid `content_type`/`content_id` format, `500` on database/downstream failure (never leaked as a raw 500 to the child-facing client without graceful messaging upstream in KMP).

*Contract source: PRD §3.4. Field names and codes are taken directly from the PRD; no fields invented. **Resolved:** the `403` error body requires no bespoke schema — `AuthorizationError` is an existing `core/exceptions.py` `DomainError` subclass already mapped to `403` platform-wide, so this endpoint returns the same standard error envelope every other `403` in the app uses (no new response shape to design).*

## 14. Database Requirements
Table: `favorite` (canonical shape per B-03) — `favorite_id PK`, `child_id FK`, `content_id`, `content_type`, `created_at`. `UNIQUE(child_id, content_id, content_type)`. `CHECK content_type IN ('story','surah','dua', ...)`. Index `(child_id, content_type, created_at DESC)`.

## 15. Validation
- `content_type` allowlist check (extensible enum, matches B-03's CHECK constraint).
- `content_id` non-empty, syntactically valid for its declared type.
- `client_request_id` present and well-formed UUID.

## 16. Authentication
Bearer JWT, child-mode session, via `Depends(get_current_child)`.

## 17. Authorization
Implicit — the endpoint only ever acts on the authenticated child's own `child_id`, never accepts a `child_id` from the request body.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network/transient failure | Client-side optimistic update already shown (K-01); server retried via idempotent request |
| Add on inaccessible content | `403`, graceful message, no row written |
| Duplicate `client_request_id` | Return the original result, not an error |
| Concurrent identical requests | Exactly one row persists; both requests return `200` |
| Database failure | `500` with structured error body, logged, never a raw stack trace |

## 19. Offline First
Not backend-owned; the client (K-01/K-03) queues offline and replays this endpoint on reconnect using the same `client_request_id`.

## 20. Local Data
N/A (backend blueprint).

## 21. Localization
N/A — this endpoint returns no user-facing strings.

## 22. RTL
N/A.

## 23. Analytics
Downstream: KMP fires `favorite_added`/`favorite_removed` on successful response (K-01 owns this). Backend does not fire analytics directly but should structured-log the toggle event (ids only, no PII) for the B-04 aggregate pattern report to consume.

## 24. Performance
Single-row upsert/delete, indexed by the unique constraint — sub-millisecond DB operation. Accessibility check is the dominant latency cost (downstream service call); should be async and short-timeout with graceful degradation (reject rather than hang) — confirm timeout budget with Backend Architect.

## 25. Security
- Server-side accessibility re-validation is the primary defense against a tampered client attempting to favorite inaccessible content (FR-6).
- No secrets or credentials touched by this endpoint.
- Do not modify PostgreSQL or Redis credentials as part of this work.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic (via B-03's migration, not this blueprint).

## 27. Testing
- Unit: idempotent add, idempotent remove, accessibility-gate rejection on add, no-gate on remove.
- Integration: 10 concurrent identical add requests → exactly one row, all `200`.
- Integration: accessibility check failure path → `403`, no row written.
- Integration: removal succeeds even when the child's current accessibility to that content has since changed.

## 28. Documentation
Update OpenAPI schema for `POST /v1/favorites` (request/response examples for both add and remove). Note the supersession of A.3's separate `POST`/`DELETE` shape in the module's internal changelog.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm B-03 Migration Applied.** Objective: verify `favorite` table has `content_id`/`content_type` columns before writing any code here. Do Not Change: skip if B-03 is not yet merged; block this task.
**Task 02 — Define/Extend Pydantic Schemas.** `FavoriteToggleRequest`, `FavoriteToggleResponse` in `favorite_schemas.py`.
**Task 03 — Implement Repository Upsert/Delete.** `FavoriteRepository.upsert(...)` / `.delete(...)`, using the DB unique constraint as the source of truth for dedup, not an application-level check alone.
**Task 04 — Implement Service Logic.** `FavoriteService.toggle(...)` — dispatches accessibility check by `content_type` on add only.
**Task 05 — Design and Wire Content-Type-Dispatched Accessibility Check.** No existing accessibility-check interface was found in A.3/A.5/A.6 (confirmed via targeted search, see §7) — this task must first define a small dispatch contract (e.g. `ContentAccessChecker.canAccess(child_id, content_type, content_id) -> bool`) and then coordinate with each module owner to implement it against their own existing eligibility logic (age-band/unlock-state for A.3, equivalent for A.5/A.6), rather than assuming a call site already exists.
**Task 06 — Add Router Endpoint.** `POST /v1/favorites` on `ContentRouter`, replacing/superseding A.3's separate verbs per B-03.
**Task 07 — Add Validation.** `content_type` allowlist, request schema validation.
**Task 08 — Add Error Handling.** Map accessibility-check failure to `403` via `AuthorizationError`.
**Task 09 — Add Structured Logging.** ids-only, no PII.
**Task 10 — Write Tests.** Per §27.
**Task 11 — Update OpenAPI Documentation.**
**Task 12 — Final Code Review.** Confirm no duplicate favorite mechanism remains from A.3's pre-migration endpoints.

## 30. Definition of Done
All tests in §27 pass; concurrent-duplicate test is green; accessibility-gate test is green; OpenAPI docs updated; A.3's legacy separate-verb endpoints are either removed or transparently proxy to this one (confirmed via B-03 coordination).

## 31. Final Verification Checklist
- [ ] No duplicate favorite rows under concurrent requests
- [ ] Accessibility re-check enforced on add, skipped on remove
- [ ] `client_request_id` idempotency verified
- [ ] `content_type` allowlist enforced
- [ ] Auth/authorization enforced (own child only, implicit)
- [ ] OpenAPI docs updated
- [ ] PostgreSQL/Redis credentials untouched
- [ ] Coordinated with B-03 migration timing
