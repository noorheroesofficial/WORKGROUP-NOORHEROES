# B-01 — Device Profile Binding Service

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). This is the feature's single highest-priority guarantee: Firebase issues one FCM token per installation, not per child, so NoorHeroes implements per-child notification targeting via an **exclusive active-profile binding** (PRD FR-8/FR-9). Zero tolerance for cross-profile misdelivery (PRD §1.4, §12.1).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-01 Device Profile Binding Service

## 4. Objective
Implement `POST /v1/devices` (installation/token registration) and `PATCH /v1/devices/{id}/active-profile` (atomic exclusive binding switch) so that at any moment exactly one target (parent or one child) is bound to a given installation, with the switch implemented as a single indivisible transaction.

## 5. Business Requirements
- Firebase issues one token per app installation, not per child (FR-8) — targeting is achieved entirely through the binding layer, never by assuming token-to-child uniqueness.
- The installation token is bound to either the Parent Profile or exactly one selected child at any given time (FR-8).
- On every profile switch, the previous binding is deactivated and the new binding is activated **atomically** — never a window with zero or two simultaneously active bindings (FR-8, Acceptance Criteria §1.9).
- Two devices belonging to the same family may have independent bindings (FR-9) — e.g., Device 1 bound to Child A while Device 2 is bound to Child B or the Parent Profile.
- Logout revokes all bindings for that session/device (FR-9).
- A device with no active binding (e.g., immediately post-logout) is the expected, safe default state — not an error (Edge Case 8).

## 6. Existing Architecture
- Extends the existing `notifications` bounded context at `src/noorheroes/modules/notifications/` (`NotificationPreference` model, `NotificationRepository`, `NotificationService(BaseService)`, `NotificationRouter` — per `FAST-API-INSTRUCTIONS.md` §5.8). The existing `register_push_token()` method on `NotificationService` is the natural anchor point to extend into `POST /v1/devices`; do not create a parallel token-registration path.
- Follow the standard Router → Service(`BaseService`) → Repository(`BaseRepository[ModelT]`) → PostgreSQL layered architecture (`FAST-API-INSTRUCTIONS.md` §1).
- Use `get_current_parent` / `get_current_child` dependencies from `src/noorheroes/core/deps.py` for auth context.

## 7. Existing Code to Reuse
- `NotificationService.register_push_token()` — extend rather than duplicate.
- `BaseService` / `BaseRepository[ModelT]` base classes.
- `get_current_parent`, `get_current_child`, `get_db_session` dependencies.

## 8. Files to Create
- `src/noorheroes/modules/notifications/binding_service.py` — `DeviceBindingService(BaseService)` with `register_installation()` and `switch_active_profile()`.
- `src/noorheroes/modules/notifications/binding_repository.py` — `DeviceBindingRepository(BaseRepository[DeviceProfileBinding])`.
- Extend `models.py`: `PushInstallation`, `PushToken`, `DeviceProfileBinding`.
- `alembic/versions/<rev>_create_device_binding_tables.py`.
- Extend `schemas.py`: `DeviceRegisterRequest`, `DeviceRegisterResponse`, `ActiveProfileSwitchRequest`, `ActiveProfileSwitchResponse`.
- Extend `api.py`: `POST /v1/devices`, `PATCH /v1/devices/{id}/active-profile`.
- `tests/modules/notifications/test_binding_service.py`.

## 9. Files to Modify
- `src/noorheroes/modules/notifications/service.py` — no functional change; `NotificationService` continues to own dispatch, `DeviceBindingService` owns binding lifecycle (kept as a distinct service per single-responsibility, since binding is this feature's highest-stakes guarantee).

## 10. Backend Requirements
- `POST /v1/devices`: upsert `PushInstallation` by `(parent_id, fcm_token)`; create/refresh a `PushToken` row (`state='active'`).
- `PATCH /v1/devices/{id}/active-profile`: within a single DB transaction — (a) load the installation's current `device_profile_bindings` row if any, (b) set it inactive (or delete/replace, per single-row-per-installation design in PRD §4.2), (c) insert/activate the new binding row targeting `parent` or `target_child_id`, (d) commit as one unit.
- `device_profile_bindings` is schema-designed as a single-row-per-installation table (PK = FK `installation_id`), so "exactly one active binding" is structurally guaranteed rather than enforced via a partial unique index over a multi-row table (PRD §4.2) — implement the switch as an UPSERT on this PK, not an insert-then-deactivate-old-row pattern across multiple rows.
- Validate `target_child_id` belongs to the authenticated parent's family before activating.

## 11. KMP Requirements
`DeviceBindingManager` (K-01) calls this API as part of every profile-switch transition flow; not implemented in this backend blueprint.

## 12. NextJS Requirements
Not applicable — no admin UI surface for this sub-feature; visibility is via N-05 Device Binding Health Monitor (read-only, consumes B-08's reporting API).

## 13. API Contract

**Required API 1**
- **HTTP Method:** POST
- **Endpoint:** `/v1/devices`
- **Request:** `{ "fcm_token": "string", "app_version": "string", "locale": "string", "timezone": "string" }`
- **Response 200:** `{ "installation_id": "uuid" }`
- **Authentication:** Bearer (parent or child session)
- **Authorization:** N/A beyond valid session
- **Validation:** `fcm_token` non-empty; `locale`/`timezone` well-formed
- **Error Responses:** `401` unauthorized

**Required API 2**
- **HTTP Method:** PATCH
- **Endpoint:** `/v1/devices/{id}/active-profile`
- **Request:** `{ "target": "parent" }` or `{ "target_child_id": "uuid" }`
- **Response 200:** `{ "bound": true, "target": "parent|child_id" }`
- **Authentication:** Bearer (parent session; child switch initiated on the parent's/child-mode authority per A.1/B.16 transition flow)
- **Authorization:** `target_child_id` must belong to the authenticated family
- **Validation:** exactly one of `target` / `target_child_id` present
- **Error Responses:** `401` unauthorized, `403` child not in family, `404` installation not found, `409` (rare) transaction conflict — retryable

## 14. Database Requirements
- `push_installations`: `installation_id UUID PK`, `parent_id UUID FK`, `app_version VARCHAR`, `locale VARCHAR`, `timezone VARCHAR`.
- `push_tokens`: `token_id UUID PK`, `installation_id UUID FK`, `fcm_token VARCHAR`, `state VARCHAR CHECK IN ('active','rotated','invalid')`, `expiry TIMESTAMPTZ`; index `(installation_id, state)`.
- `device_profile_bindings`: `installation_id UUID PK_FK`, `target VARCHAR CHECK IN ('parent','child')`, `target_child_id UUID NULL`, `active BOOLEAN`, `updated_at TIMESTAMPTZ`. Single-row-per-installation design (PRD §4.2) — no additional index needed for the exclusivity guarantee itself.

## 15. Validation
- `target_child_id` must reference a child in the authenticated parent's family (or the currently authenticated child's own id when child-initiated).
- Reject request with both `target` and `target_child_id` set, or neither.

## 16. Authentication
Bearer JWT via `get_current_parent` / `get_current_child`.

## 17. Authorization
Binding switches to a `target_child_id` outside the caller's family are rejected with `403`.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Concurrent switch requests for the same installation | Serialized via transaction; last committed write wins, no intermediate ambiguous state |
| Invalid `target_child_id` | `403 Forbidden` |
| Installation not found | `404 Not Found` |
| Database failure mid-transaction | Full rollback; no partial binding state persisted |
| Logout | All bindings for the session's installation(s) explicitly deactivated (target set to none) |

## 19. Offline First
N/A (backend). Client queues the switch call for retry on reconnect (K-01).

## 20. Local Data
N/A.

## 21. Localization
`locale`/`timezone` stored as installation metadata only; no localized copy in this sub-feature.

## 22. RTL
N/A.

## 23. Analytics
`notification_binding_activated` (`target: parent|child_id`), `notification_binding_deactivated` — emitted by this service on every successful switch.

## 24. Performance
Binding switch must be low-latency (single-row UPSERT); no N+1 queries; index-covered lookups.

## 25. Security
The binding-switch transaction is this service's most security-critical operation (PRD §12.3) — any regression here risks a child receiving a notification meant for a different profile. No monetization or admin bypass may set an active binding without going through this validated transaction.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, Alembic, pytest, pytest-asyncio.

## 27. Testing
- Unit: `switch_active_profile()` transaction logic with mocked repository.
- Integration: serializable-isolation test confirming no queryable moment has zero or multiple active bindings for one installation, per PRD §5 backend prompt item 1.
- Integration: rapid consecutive switch requests do not corrupt final state.
- Regression: full suite re-run on any change to `binding_service.py` or `binding_repository.py` (DevOps §10 mandatory CI gate).

## 28. Documentation
OpenAPI docs for both endpoints; inline comment on `device_profile_bindings` schema explaining the single-row-per-installation exclusivity design decision, cross-referencing PRD §4.2.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Database Models & Migration**
- Objective: Add `PushInstallation`, `PushToken`, `DeviceProfileBinding` SQLAlchemy models and Alembic migration.
- Why Required: Foundational schema for the entire binding architecture.
- Existing Architecture to Follow: `BaseRepository[ModelT]` model conventions used elsewhere in `notifications/models.py`.
- Files to Create: `models.py` extension, migration file.
- Validation: CHECK constraints on `state`/`target` enums.
- Do Not Change: existing `NotificationPreference` model.
- Definition of Done: migration applies cleanly; constraints enforced at DB layer.

**Task 02 — Implement DeviceBindingRepository**
- Objective: Data-access layer for installations, tokens, and bindings.
- Files to Create: `binding_repository.py`.
- Implementation Details: `upsert_installation()`, `upsert_token()`, `get_active_binding()`, `upsert_binding()` (single UPSERT on PK for exclusivity).
- Tests: unit tests with an in-memory/test DB session.
- Definition of Done: repository methods covered by unit tests.

**Task 03 — Implement DeviceBindingService.register_installation()**
- Objective: Back `POST /v1/devices`.
- Files to Create: `binding_service.py` (partial).
- Existing Files to Reuse: `NotificationService.register_push_token()` as reference pattern.
- Business Rules: FR-8.
- Tests: unit test for upsert-by-token behavior.
- Definition of Done: endpoint registers/refreshes token correctly.

**Task 04 — Implement DeviceBindingService.switch_active_profile() as an Atomic Transaction**
- Objective: Back `PATCH /v1/devices/{id}/active-profile` with the exclusive-binding guarantee.
- Why Required: PRD's single highest-priority correctness guarantee (§5 backend prompt item 1).
- Implementation Details: single DB transaction; UPSERT on `device_profile_bindings.installation_id`.
- Business Rules: FR-8, FR-9.
- Security: validate `target_child_id` family ownership before commit.
- Tests: serializable-isolation test asserting no zero/multi-active-binding state is ever queryable.
- Do Not Change: the single-row-per-installation schema design without architecture sign-off.
- Definition of Done: atomicity test passes; CI gate wired per DevOps §10.

**Task 05 — Implement API Endpoints**
- Objective: Wire `POST /v1/devices` and `PATCH /v1/devices/{id}/active-profile` into `api.py`.
- Files to Modify: `api.py`.
- Validation: request schema validation via Pydantic.
- Authentication/Authorization: `get_current_parent`/`get_current_child`; family-ownership check.
- Error Handling: `401/403/404` per §18.
- Tests: endpoint-level integration tests.
- Definition of Done: endpoints pass integration tests and match API Contract (§13) exactly.

**Task 06 — Add Analytics Emission**
- Objective: Emit `notification_binding_activated`/`notification_binding_deactivated` on every switch.
- Files to Modify: `binding_service.py`.
- Analytics: parameters per §23.
- Definition of Done: events verified in integration test via event-bus test double.

**Task 07 — Add Logging & Observability**
- Objective: Structured logging for every registration and switch (installation_id, previous/new target, timestamp).
- Files to Modify: `binding_service.py`.
- Security: no PII beyond installation/child id in logs.
- Definition of Done: logs verified in test output; ready for N-05 monitoring consumption.

**Task 08 — Write Exhaustive Test Suite & Update API Documentation**
- Objective: Finalize unit + integration + concurrency tests; update OpenAPI docs.
- Tests: full suite per §27.
- Documentation: OpenAPI descriptions, inline schema comment per §28.
- Definition of Done: all tests green; CI-blocking gate active; documentation reviewed.

## 30. Definition of Done
- Both endpoints implemented, tested, and documented exactly per the API Contract (§13).
- Atomic exclusive-binding guarantee verified via a concurrency/serializable-isolation test — no installation ever observed with zero or multiple active bindings.
- Family-ownership validation enforced for `target_child_id`.
- Analytics and structured logging in place.
- CI gate for the atomicity test is mandatory and non-bypassable (DevOps §10).

## 31. Final Verification Checklist
- [ ] `POST /v1/devices` registers/refreshes installation + token correctly
- [ ] `PATCH /v1/devices/{id}/active-profile` switches bindings atomically (concurrency test passes)
- [ ] No queryable moment with zero or multiple active bindings for one installation
- [ ] `target_child_id` family-ownership validated, unauthorized targets rejected (403)
- [ ] Logout path deactivates all bindings for the session's installation(s)
- [ ] Analytics events fire correctly on activation/deactivation
- [ ] Structured logs capture every switch for audit/monitoring
- [ ] Full test suite (unit + integration + concurrency) passes and is wired as a CI-blocking gate
- [ ] OpenAPI documentation matches implemented contract exactly
