# Blueprint: Parent Notifications Inbox API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). This blueprint extends the **existing** `notifications` bounded context (`src/noorheroes/modules/notifications/`) — it does not create a new context. It delivers the parent-queryable read model over the notification history that B.17 already writes via its Notification Intent Service/Policy Engine.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support (`PRD_Documents/Parent Area — In-App (19-26)/Feature_C25_Notifications_Parent_Support.md`)

## 3. Sub-feature
B-01 — Parent Notifications Inbox API

## 4. Objective
Implement `GET /v1/parent/notifications` and `POST /v1/parent/notifications/{id}/mark-read` as a parent-scoped read/update surface over the **shared** `notification_deliveries` table already introduced by B.17 — no schema fork, no parallel delivery-history table.

## 5. Business Requirements
Source: PRD §1.7 FR-1, FR-2, FR-12; §1.9 Acceptance Criteria (inbox render, deep-link revalidation); §1.10 Edge Case 1, 6; §1.11 Error Handling; §2.3 Tab Structure; §3.3–3.4; §5 Backend AI Code-Generation Prompt item 6.
- Inbox lists all system/safety/marketing notifications for the authenticated parent, with read/unread state and `type` filtering (FR-1).
- Mark-read and "open related screen" actions (FR-2); the deep-link-open path itself is reused from B.17, not reimplemented here (FR-12, out of scope for this sub-feature — see B.17's Deep Link Resolution Service).
- Must reuse `notification_deliveries` exactly as B.17 defined it — "this feature's notification-delivery mechanics reuse B.17's exact shared infrastructure... no parallel, divergent implementation" (§1.8 Non-Functional: Shared Architecture Reuse).
- Parent-Session-Only Gate: "child-mode token rejected" (§5 item 6, mirrors C.20's B-01 pattern).
- Muting every non-safety-critical category must never break or hide the inbox itself (Edge Case 1) — this endpoint has no dependency on preference state to function.
- Offline/cache-staleness handling is a KMP-side concern (K-01); this API's only obligation is to always return the true current server state on a successful call.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md`:
- Layering: Router → Service → Repository → DB via `Depends()`; single request-scoped `AsyncSession` per §7.
- `notifications` context already exists (§5.8): `NotificationPreference` model, `NotificationRepository.get_preferences_by_user_id()`, `NotificationService(BaseService).register_push_token()/dispatch_notification()`, `NotificationRouter`.
- `core/deps.py` already defines `ParentSessionContext`, `get_current_parent()`. C.20 established the "Parent-Session-Only Gate" pattern (router-mount-level `Depends()`, rejecting child-mode tokens with a distinct error code) — this blueprint follows that identical pattern rather than inventing a new one.
- `BaseRepository[ModelT]` (`common/base_repository.py`) provides `list_paginated(cursor, limit) -> PageResult[ModelT]` — the correct base for cursor-paginated inbox listing.
- `common/schemas.py` → `NoorHeroesBaseModel` (Pydantic v2 camelCase base) — all new DTOs must inherit this.

## 7. Existing Code to Reuse
- `notification_deliveries` table/ORM model as defined by B.17 — read directly, do not duplicate or add a competing table.
- `NotificationRepository` (extend, do not fork) — add inbox-specific query methods here rather than creating a second repository class for the same table.
- `BaseRepository.list_paginated()` for cursor pagination.
- `get_current_parent()` / the Parent-Session-Only Gate pattern established in C.20's B-01 (`src/noorheroes/modules/dashboard/deps.py` as the reference implementation — mirror its structure for the `notifications` router mount, or confirm whether `notifications` already has an equivalent gate before adding a duplicate).
- `DomainError` subclasses (`NotFoundError`, `AuthenticationError`, `AuthorizationError`) from `core/exceptions.py`.

## 8. Files to Create
- `tests/modules/notifications/test_parent_inbox_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/notifications/models.py` — confirm `NotificationDelivery` ORM model exists (from B.17); do not redefine if present.
- `src/noorheroes/modules/notifications/schemas.py` — add `ParentNotificationResponse`, `ParentNotificationListResponse`, `MarkReadResponse`.
- `src/noorheroes/modules/notifications/repository.py` — add `NotificationRepository.list_deliveries_for_parent(parent_id, type, read_status, cursor, limit)` and `mark_delivery_read(delivery_id, parent_id)`.
- `src/noorheroes/modules/notifications/service.py` — add `NotificationService.get_parent_inbox(...)` and `mark_notification_read(...)`.
- `src/noorheroes/modules/notifications/api.py` — add `GET /v1/parent/notifications`, `POST /v1/parent/notifications/{id}/mark-read` to `NotificationRouter`, gated by the Parent-Session-Only dependency.

## 10. Backend Requirements
- `GET /v1/parent/notifications?type=&read_status=`: validates `type` against `safety|system|marketing` and `read_status` against `read|unread` when present (both optional); returns `{ "notifications": [ { "id", "type", "title", "read", "deep_link", "occurred_at" } ] }` (PRD §3.4 exact shape).
- `POST /v1/parent/notifications/{id}/mark-read`: idempotent — marking an already-read notification read again returns `{ "read": true }` without error.
- Repository query scopes strictly to the requesting parent's `family_id` — cross-family delivery rows must never be returned or mutable (mirror the `ChildScopeViolationError` pattern used elsewhere in the codebase for the equivalent "cross-family" concept, or raise `NotFoundError` for a delivery not owned by this family so as not to leak existence).
- Repository method signatures accept `parent_id`/`family_id` derived from `ParentSessionContext` only — never an externally-supplied family identifier in the request body or query string (mirrors the family-scoping discipline already established in C.20's Dashboard endpoints).
- No dependency on `notification_preferences` read state for this endpoint to function — the inbox lists what was actually delivered, independent of current preference configuration (Edge Case 1).

## 11. KMP Requirements
N/A for this blueprint's backend scope — consumed by K-01's `NotificationsRepository.getInbox()/markRead()`.

## 12. NextJS Requirements
N/A — no admin surface for this specific read model (B.17's Admin Delivery/Engagement Report already covers aggregate delivery visibility).

## 13. API Contract
### `GET /v1/parent/notifications?type=&read_status=`
- **Auth:** Bearer (Parent session only)
- **Query Params:** `type: "safety"|"system"|"marketing"` (optional), `read_status: "read"|"unread"` (optional)
- **Response 200:** `{ "notifications": [ { "id": "string", "type": "safety|system|marketing", "title": "string", "read": false, "deep_link": "string", "occurred_at": "ISO8601" } ] }`
- **Error Responses:** `401` invalid/expired token; `403 CHILD_MODE_TOKEN_REJECTED` child-mode token.

### `POST /v1/parent/notifications/{id}/mark-read`
- **Auth:** Bearer (Parent session only)
- **Response 200:** `{ "read": true }`
- **Error Responses:** `404` if `id` doesn't belong to the requesting family; `401`/`403` per above.

## 14. Database Requirements
None new. Reads/updates the existing `notification_deliveries` table (B.17 §4.2: FK `template_id`, Index `(recipient_ref, sent_at DESC)`). Confirm the exact column used for "read" state (e.g., `opened_at IS NOT NULL` vs. a dedicated `read` boolean) against B.17's actual migration before implementing — do not invent a new column if `opened_at` already serves this purpose.

## 15. Validation
- `type`/`read_status` query params validated against their enum values; invalid values → `422`.
- `id` path param validated as the platform's standard ID format (ULID/UUID per `common/utils/ids.py`).

## 16. Authentication
Reuses `get_current_parent()` / JWT verification. No new auth mechanism.

## 17. Authorization
Parent-Session-Only Gate (reject child-mode tokens) plus family-scoped row ownership check on both endpoints.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Child-mode token | `403 CHILD_MODE_TOKEN_REJECTED` |
| Expired/invalid token | `401` |
| Notification `id` not found or not owned by family | `404` |
| Empty inbox (new account) | `200` with `{ "notifications": [] }`, not an error |
| Invalid `type`/`read_status` value | `422` |
| DB failure | `500` via standard `DomainError` → global handler, logged with request ID |

## 19. Offline First
N/A server-side. This endpoint's only obligation is correctness on a successful call; KMP (K-01) owns caching/staleness/offline queueing of mark-read actions.

## 20. Local Data
N/A.

## 21. Localization
Notification `title` content is stored/rendered per B.17's existing localized-template rendering pipeline — this endpoint does not introduce a second localization path.

## 22. RTL
N/A (backend).

## 23. Analytics
No server-side analytics emission required beyond existing structured request logging; `notifications_inbox_viewed` and `notification_marked_read` (PRD §1.19) are client-fired events (K-01).

## 24. Performance
- Cursor-based pagination via `BaseRepository.list_paginated()` — never full-table scan per parent.
- Index reuse: `(recipient_ref, sent_at DESC)` already exists on `notification_deliveries` (B.17 §4.2); confirm `recipient_ref` maps to the parent-scoping column used here, or add a covering index if the parent-facing query pattern differs materially from B.17's child-facing one.
- Optional Redis cache for the hot inbox-list read, keyed by `family_id` + filter params, invalidated on mark-read — only if load testing shows this table under sufficient parent-facing read volume to warrant it; do not add caching speculatively without a measured need.

## 25. Security
- Family-scoped row ownership check on every read/mutation — prevents cross-family notification-history disclosure (OWASP Broken Access Control).
- Parent-Session-Only Gate prevents a child-mode session from ever reading a parent's notification history.

## 26. Library Requirements
No new dependencies — existing FastAPI, SQLAlchemy 2.0 async, pytest.

## 27. Testing
1. Unit test: `list_deliveries_for_parent()` filters correctly by `type` and `read_status`, independently and combined.
2. Unit test: `mark_delivery_read()` is idempotent (calling twice on an already-read row succeeds without error).
3. Integration test: a child-mode token against both routes is rejected with `403 CHILD_MODE_TOKEN_REJECTED`.
4. Integration test: a notification belonging to a different family returns `404`, never `200` with another family's data.
5. Integration test: empty inbox for a new account returns `200` with an empty array.
6. Integration test: muting all non-safety-critical categories (simulated via `notification_preferences` state) does not affect this endpoint's ability to list whatever deliveries did occur (Edge Case 1 — confirms no accidental coupling to preference state).
7. Test: invalid `type`/`read_status` query value returns `422`.

## 28. Documentation
- OpenAPI descriptions for both endpoints, including the `403 CHILD_MODE_TOKEN_REJECTED` and `404` response schemas.
- Docstring on new repository/service methods citing PRD §3.4 and B.17 §4.1 (shared table reuse).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm and Extend Notification Delivery Schema Access**
- Task ID: B01-T01
- Objective: Verify the exact `notification_deliveries` column used for read-state and recipient scoping before writing any query.
- Why This Is Required: PRD mandates zero schema fork; guessing a column name risks a divergent implementation.
- Existing Architecture to Follow: B.17's `notification_deliveries` migration/model (`modules/notifications/models.py`).
- Existing Files to Reuse: `modules/notifications/models.py`.
- Files to Create: none.
- Files to Modify: none (read-only investigation task; document findings in the PR description if the exact column names differ from this blueprint's assumptions).
- Implementation Details: Inspect `NotificationDelivery` ORM class for `recipient_ref`/`family_id`/`parent_id`, `opened_at`/`read` fields, and `template_id` FK to determine `title`/`deep_link` sourcing (likely joined via `template_id` to a template table, or denormalized onto the delivery row — confirm which before Task 02).
- Business Rules: FR-11/§1.8 Shared Architecture Reuse.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: N/A (investigation task).
- Documentation: Note actual schema in code comments for Task 02.
- Dependencies: None.
- Do Not Change: Do not alter B.17's schema.
- Expected Result: Confirmed field mapping for Task 02.
- Definition of Done: No ambiguity remains about which columns to query.

**Task 02 — Implement Repository Methods**
- Task ID: B01-T02
- Objective: `list_deliveries_for_parent()` and `mark_delivery_read()` on `NotificationRepository`.
- Why This Is Required: Data-access layer for both endpoints.
- Existing Architecture to Follow: `BaseRepository[ModelT]` pattern, `list_paginated()`.
- Existing Files to Reuse: `common/base_repository.py`.
- Files to Create: none.
- Files to Modify: `modules/notifications/repository.py`.
- Implementation Details: Family-scoped `WHERE` clause using the session's `family_id`; optional `type`/`read_status` filters; cursor pagination.
- Business Rules: FR-1, FR-2.
- Validation: N/A (service layer validates enums).
- Error Handling: Returns `None`/empty for not-found rather than raising (service layer converts to `404`).
- Security: Family-scoping is the core control here.
- Performance: Uses existing `(recipient_ref, sent_at DESC)` index.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: Do not modify `BaseRepository` itself.
- Expected Result: Methods return correctly scoped, filtered, paginated results.
- Definition of Done: Matches §10 requirements.

**Task 03 — Implement Service Methods**
- Task ID: B01-T03
- Objective: `NotificationService.get_parent_inbox()` / `mark_notification_read()`.
- Why This Is Required: Business-rule and error-mapping layer between router and repository.
- Existing Architecture to Follow: `BaseService` pattern, `DomainError` subclasses.
- Existing Files to Reuse: `common/base_service.py`, `core/exceptions.py`.
- Files to Create: none.
- Files to Modify: `modules/notifications/service.py`.
- Implementation Details: Validate `type`/`read_status` enums (422 via `ValidationError` if invalid); raise `NotFoundError` if the delivery isn't owned by the family; call idempotent mark-read.
- Business Rules: Edge Case 1 (no preference-state coupling).
- Validation: Enum validation.
- Error Handling: Per §18.
- Security: Family ownership check before mutation.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings citing PRD §3.4.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Service layer fully testable against a mock repository.
- Definition of Done: All §18 error scenarios covered.

**Task 04 — Add Routes to NotificationRouter with Parent-Session-Only Gate**
- Task ID: B01-T04
- Objective: Expose both endpoints, gated against child-mode tokens.
- Why This Is Required: PRD §5 item 6 mandates this exact gate pattern.
- Existing Architecture to Follow: C.20 B-01's Parent-Session-Only Gate reference implementation.
- Existing Files to Reuse: `get_current_parent()`, or the dedicated gate dependency if `notifications` already has an equivalent (confirm before duplicating C.20's `dashboard`-specific one — this may warrant a shared, reusable gate dependency in `core/deps.py` rather than a second module-specific copy; raise this as a note if `notifications` and `dashboard` end up with duplicated gate logic).
- Files to Create: none.
- Files to Modify: `modules/notifications/api.py`.
- Implementation Details: `GET /v1/parent/notifications`, `POST /v1/parent/notifications/{id}/mark-read`, both under the Parent-Session-Only dependency.
- Business Rules: FR-1, FR-2.
- Validation: Pydantic query/path param validation.
- Error Handling: Per §18.
- Security: Router-level (not per-handler) gate, matching C.20's structural pattern.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI descriptions.
- Dependencies: Task 03.
- Do Not Change: Do not remove/alter existing `NotificationRouter` routes (`push-tokens`, `dispatch`).
- Expected Result: Both routes live and gated.
- Definition of Done: Matches §13 API Contract exactly.

**Task 05 — Write Test Suite**
- Task ID: B01-T05
- Objective: Cover §27.
- Why This Is Required: Standard test coverage plus the Edge Case 1 non-coupling guarantee.
- Existing Architecture to Follow: pytest + existing fixture patterns.
- Existing Files to Reuse: Existing auth/session test fixtures.
- Files to Create: `tests/modules/notifications/test_parent_inbox_api.py`.
- Files to Modify: none.
- Implementation Details: All 7 cases from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes/error bodies.
- Security: Cross-family and child-mode-token tests are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing PRD sections.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`GET /v1/parent/notifications` and `POST /v1/parent/notifications/{id}/mark-read` live under `NotificationRouter`, reusing B.17's `notification_deliveries` table with zero schema fork, family-scoped and Parent-Session-Only gated, all tests green.

## 31. Final Verification Checklist
- [ ] No new `notification_deliveries`-equivalent table created
- [ ] Child-mode token rejected on both routes
- [ ] Cross-family delivery access returns `404`, not another family's data
- [ ] Empty inbox returns `200` with empty array, not an error
- [ ] Mark-read is idempotent
- [ ] Muted-preferences state does not affect inbox listing (Edge Case 1)
- [ ] No PostgreSQL/Redis credential files touched
- [ ] Existing `NotificationRouter` routes (push-tokens, dispatch) unmodified
