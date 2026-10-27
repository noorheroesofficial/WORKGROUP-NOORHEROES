# B-05 — Immutable Audit Log Service

## 1. Feature Context
Part of E.28. Every other Admin Portal module's mutating actions and sensitive reads write to this single, shared log — never a per-module independent log (FR-12). This blueprint includes a **breaking change** to existing code: the current `AdminRouter` exposes a client-facing `POST /v1/admin/audit-logs` endpoint, which PRD FR-6 explicitly forbids ("Sensitive reads and all mutations are audited at the service layer, not just logged at the gateway... the audit-write must happen inside the business-logic service itself").

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-05 — Immutable Audit Log Service

## 4. Objective
Guarantee that audit entries are created exclusively via internal service-to-service calls from each Admin module's own backend code — no client-facing write endpoint exists anywhere — and that the `audit_log` table itself is append-only at the database-permission level (FR-6, FR-12).

## 5. Business Requirements
- FR-6: sensitive reads and all mutations audited at the service layer, not the gateway — a compromised gateway cannot suppress the audit trail.
- FR-12: audit log immutable, queryable by actor/resource/action, retained per compliance schedule.
- Acceptance Criteria: a sensitive mutation anywhere in the Admin Portal has a corresponding immutable audit entry, written at the service layer regardless of gateway state.
- Edge Case 8: query spanning a pre-deployment date range returns an empty result for that portion, never an error.

## 6. Existing Architecture — Breaking Change Notice
- **Current state (must change):** `src/noorheroes/modules/admin/models.py` has `AdminAuditLog`; `AdminAuditRepository.log_action()/list_logs()`; `AdminRouter` exposes both `GET /v1/admin/audit-logs` (requires `admin:read`) **and** `POST /v1/admin/audit-logs` (requires `admin:write`) per the existing FastAPI instructions manual (§6 API Routers, entry #2 `AdminRouter`).
- **Required change:** the `POST /v1/admin/audit-logs` **client-facing route must be removed**. PRD §3.4 is explicit: "This endpoint/internal-call-pattern is the only way an audit entry is ever created — there is no client-facing 'log this' API." Existing callers of the old client-facing POST (if any exist in early E.28-adjacent code) must be migrated to call `AuditLogService.log_action()` directly from their own service layer, in-process.
- This is flagged per the project's "Architecture Improvement" process (system instructions §24): Existing Architecture (client-writable audit endpoint) → Problem (violates FR-6's gateway-cannot-suppress guarantee) → Proposed Improvement (internal-only service call) → Impact (any code currently POSTing to this endpoint breaks and must be migrated to a direct service call) → Implementation (this blueprint) → Documentation Update (Task 08).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `AdminAuditLog` model | `modules/admin/models.py` | Base for extended `audit_log` schema (extend with `resource_type`, `resource_id`, `action`, `metadata`) |
| `AdminAuditRepository.list_logs()` | `modules/admin/repository.py` | Base for the read-only query path |
| `BaseRepository[ModelT]` | `common/base_repository.py` | Repository scaffolding |
| `Clock` | `common/utils/clock.py` | `occurred_at` timestamping |

## 8. Files to Create
- `src/noorheroes/modules/admin/audit/service.py` — `AuditLogService` (internal-only)
- `src/noorheroes/modules/admin/audit/schemas.py` — `AuditLogEntryResponse`, `AuditLogQueryFilters`
- `alembic/versions/xxxx_extend_audit_log_and_lock_permissions.py` — schema extension + `REVOKE UPDATE, DELETE` grant migration
- `tests/modules/admin/audit/test_audit_log_service.py`
- `tests/architecture/test_no_client_facing_audit_write.py`
- `tests/modules/admin/audit/test_audit_log_db_permissions.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/models.py` — extend `AdminAuditLog` with `resource_type`, `resource_id`, `action`, `metadata jsonb`; rename conceptually to represent the platform-wide `audit_log` table (keep table name stable if already deployed, or migrate — see Task 01 for the decision point)
- `src/noorheroes/modules/admin/repository.py` — extend `AdminAuditRepository` with `log_action(actor_admin_id, resource_type, resource_id, action, metadata)` (internal) and `query(actor=, resource=, action=, cursor=, limit=)` (external-read-safe)
- `src/noorheroes/modules/admin/api.py` — **remove** `POST /v1/admin/audit-logs`; keep and harden `GET /v1/admin/audit-logs?actor=&resource=&action=`
- `src/noorheroes/modules/admin/service.py` — remove any `AdminService` method that exposes a writable audit path to a router; `AuditLogService.log_action()` is called only from other services' own code (e.g., B-04's `MakerCheckerService`, B-06's flag service, B-09's deactivation service), never from a router handler taking client input

## 10. Backend Requirements
- **Model:** `audit_log(log_id PK, actor_admin_id FK, resource_type, resource_id, action, metadata jsonb, occurred_at)`, index `(actor_admin_id, occurred_at DESC)`, index `(resource_type, resource_id, occurred_at DESC)`.
- **`AuditLogService.log_action(actor_admin_id, resource_type, resource_id, action, metadata)`:** the sole write path; designed to be called in-process from within another service's own transaction/request-handling code (e.g., `MakerCheckerService.approve_proposal()` calls this directly after applying a change) — never exposed as a route handler parameter surface for arbitrary client-supplied audit data.
- **`GET /v1/admin/audit-logs?actor=&resource=&action=`:** paginated, read-only, no corresponding write-capable client endpoint.
- **DB permission lockout:** the `audit_log` table has no `UPDATE`/`DELETE` grant for any application database role — enforced via `REVOKE UPDATE, DELETE ON audit_log FROM <app_role>` in the migration, mirroring the `reward_ledger` permission-lockout pattern already established for A.11.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-06 — Audit Log Viewer` (read-only query UI).

## 13. API Contract
### `GET /v1/admin/audit-logs?actor=&resource=&action=&cursor=&limit=`
- **Auth:** `get_current_admin`
- **Authorization:** Role-scoped per resource type (via B-03's `require_admin_permission("audit-logs", "read")`, potentially further scoped by `resource_type` in query)
- **Response 200:**
```json
{ "items": [ { "log_id": "...", "actor_admin_id": "...", "resource_type": "role_permission", "resource_id": "role_01H...", "action": "approved", "metadata": {}, "occurred_at": "..." } ], "next_cursor": "...", "has_more": false }
```
- **Error Responses:** `401`, `403`, `422` (invalid filter params)

**No write-capable client endpoint exists.** This is a hard architectural property, verified by Task 04's test.

## 14. Database Requirements
- `audit_log`: append-only — `REVOKE UPDATE, DELETE` for the application's runtime DB role; only `INSERT`/`SELECT` permitted.
- Indexes per §10.
- Retention: per platform compliance schedule (PRD §4.5) — B-05 does not implement a deletion/archival job (contradicts immutability); if retention requires eventual archival, that is a separate, explicitly-approved compliance process outside this blueprint's scope, never a routine app-level DELETE.

## 15. Validation
- `resource_type`/`action` values validated against a known, extensible allow-list (extensible because E.29–E.34 will register their own resource types over time — do not hardcode an exhaustive closed enum that blocks future modules; use a registry pattern that new modules append to, consistent with the "extensible-registry-driven pattern" referenced in the PRD's N-02 frontend guidance for B.17 notification categories).
- Query filters validated (`cursor` format, `limit` bounds).

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
`GET` gated per B-03's role-scoped permission check; scope may vary per `resource_type` (e.g., a Support Agent might query only support-resource audit entries, not billing).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Query date range predates system deployment | Empty result for that portion, never an error, with a clear logging-coverage-start indicator in the response metadata (Edge Case 8) |
| Unauthorized query | `401`/`403` |
| Invalid filter params | `422` |
| Attempt to call a (now-removed) client-write endpoint | `404` (route no longer exists) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`resource_type`/`action` are stable identifiers; localized display labels are a client concern (N-06).

## 22. RTL
N/A at backend layer.

## 23. Analytics
Supports client-fired `audit_log_queried` event (PRD §1.19).

## 24. Performance
- Compound indexes support both actor-centric and resource-centric query patterns without full-table scans.
- Cursor-based (keyset) pagination, consistent with `BaseRepository.list_paginated()`'s existing pattern, avoiding OFFSET performance degradation on a large, append-only table.

## 25. Security
- **Service-layer-only audit writes (primary guarantee):** no client-facing write endpoint exists anywhere in the admin API surface. Verified by an architectural test (Task 04).
- **Append-only enforcement (second guarantee):** `audit_log` has no `UPDATE`/`DELETE` grant for any application role — verified by a database-permission test (Task 05) attempting and failing an `UPDATE`/`DELETE` as the app's runtime role.
- Audit entries include no unredacted secrets in `metadata` (e.g., never store raw passwords/tokens/2FA codes in audit metadata).

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: `AuditLogService.log_action()` persists correctly when called from a simulated caller service.
- Unit: query filters (actor/resource/action combinations, pagination).
- Unit: pre-deployment date-range query returns empty with coverage indicator (Edge Case 8).
- **Signature test A:** architectural test confirming no publicly-routable endpoint in the entire admin API surface allows direct client-supplied audit-log creation (§5 Backend AI prompt item 5).
- **Signature test B:** database-permission test confirming the `audit_log` table itself has no `UPDATE`/`DELETE` grant for any application role (§5 item 5).

## 28. Documentation
OpenAPI schema update reflecting the **removal** of `POST /v1/admin/audit-logs`; migration note for any team/module that previously called the old endpoint, redirecting them to `AuditLogService.log_action()` direct in-process calls; document the extensible `resource_type` registry pattern for E.29–E.34 authors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `audit_log` Schema & Decide Table Migration Strategy**
- Task ID: B-05-T01
- Objective: Add `resource_type`, `resource_id`, `action`, `metadata` to the existing `AdminAuditLog` table (or formally rename/migrate if the existing table's shape is materially incompatible).
- Why Required: Current `AdminAuditLog` model (per FastAPI instructions manual) is minimal; PRD's `audit_log` needs the fuller shape from §4.1.
- Existing Architecture to Follow: Extend in place rather than creating a parallel table, to avoid a dual-audit-log split-brain.
- Files to Modify: `modules/admin/models.py`.
- Implementation Details: Add nullable-safe new columns via migration; backfill strategy for any pre-existing rows (`resource_type`/`action` may be null for historical entries — acceptable, since Edge Case 8 already anticipates a pre-deployment "no data" period conceptually).
- Do Not Change: Do not delete or truncate any existing audit rows.
- Tests: Migration test confirming existing rows survive the schema extension.
- Definition of Done: Extended schema live, existing data intact.

**Task 02 — Implement `AuditLogService.log_action()` (Internal-Only)**
- Task ID: B-05-T02
- Objective: The sole write path for audit entries.
- Files to Create: `modules/admin/audit/service.py`.
- Implementation Details: Plain service method, no router surface; designed to be called from within another service's own request-handling code, sharing that caller's request-scoped `AsyncSession` (so the audit write commits atomically with the business mutation it's recording — consistent with "no manual commits" layer rule, since the outer request's `get_db_session()` still owns the commit).
- Business Rules: FR-6 — audit-write happens inside the business-logic service itself.
- Security: No route decorator anywhere near this method; it must be architecturally unreachable from a client request body.
- Tests: Unit test with a simulated caller.
- Dependencies: Task 01.
- Definition of Done: Method usable by B-04/B-06/B-07/B-09 as an internal call.

**Task 03 — Remove Client-Facing `POST /v1/admin/audit-logs`**
- Task ID: B-05-T03
- Objective: Eliminate the existing client-writable audit endpoint per FR-6.
- Why Required: This is a hard architectural requirement, not optional — a client-facing write path defeats the entire "gateway cannot suppress the audit trail" guarantee, since anything reachable by a client is reachable by whatever compromised the gateway/client.
- Files to Modify: `modules/admin/api.py` (delete the route), `modules/admin/service.py` (remove the now-orphaned service method used only by that route, if any).
- Business Rules: This is a breaking API change — document it (Task 08).
- Do Not Change: Do not remove `GET /v1/admin/audit-logs` — only the POST.
- Tests: Confirm `POST /v1/admin/audit-logs` now returns `404`.
- Dependencies: Task 02.
- Definition of Done: Route no longer exists; any prior internal caller migrated to Task 02's direct service call.

**Task 04 — Architectural No-Client-Write Test (Signature Test A)**
- Task ID: B-05-T04
- Objective: Prove no publicly-routable endpoint allows direct client-supplied audit-log creation anywhere in the admin API surface.
- Files to Create: `tests/architecture/test_no_client_facing_audit_write.py`.
- Implementation Details: Enumerate all registered routes across the admin API surface (introspect FastAPI's route table) and assert none accept a client-supplied audit-log-creation payload; specifically assert `POST /v1/admin/audit-logs` is absent.
- Dependencies: Task 03.
- Definition of Done: Test is CI-blocking and passes.

**Task 05 — Database Permission Lockout + Test (Signature Test B)**
- Task ID: B-05-T05
- Objective: `audit_log` has no `UPDATE`/`DELETE` grant for any application role.
- Files to Create: migration (`REVOKE UPDATE, DELETE ON audit_log FROM <app_role>`), `tests/modules/admin/audit/test_audit_log_db_permissions.py`.
- Implementation Details: Attempt an `UPDATE`/`DELETE` as the application's runtime DB role inside a test transaction and assert a permission-denied error is raised by PostgreSQL itself.
- Security: This mirrors the `reward_ledger` lockout pattern (A.11) — do not modify PostgreSQL credentials to achieve this, only grants on this specific table.
- Do Not Change: PostgreSQL credentials/connection settings.
- Dependencies: Task 01.
- Definition of Done: Both `UPDATE` and `DELETE` attempts fail at the database layer; `INSERT`/`SELECT` remain functional.

**Task 06 — Implement Hardened `GET /v1/admin/audit-logs` Query**
- Task ID: B-05-T06
- Objective: Read-only, paginated, filterable query endpoint.
- Files to Modify: `modules/admin/api.py`, `modules/admin/repository.py`.
- Implementation Details: Cursor-based pagination; `actor`/`resource`/`action` filters; pre-deployment date-range empty-result handling (Edge Case 8).
- Dependencies: Task 01, B-03 Task 05 (for permission gating).
- Definition of Done: Integration tests for all filter/pagination/edge-case-8 scenarios pass.

**Task 07 — Wire Callers Across Existing Admin Module**
- Task ID: B-05-T07
- Objective: Update `AdminService` and any other current admin-context callers to use `AuditLogService.log_action()` internally instead of the removed endpoint.
- Files to Modify: `modules/admin/service.py`.
- Dependencies: Task 02, Task 03.
- Definition of Done: No remaining code path attempts to reach the removed endpoint; all internal logging goes through the new service method.

**Task 08 — Documentation & Migration Note**
- Task ID: B-05-T08
- Objective: Document the removed endpoint and the new internal-call pattern for future E.29–E.34 authors.
- Files to Modify: OpenAPI schema (auto-exported), internal architecture doc.
- Dependencies: Tasks 01–07.
- Definition of Done: `classify_openapi_diff.py` shows the expected removal; doc explains the extensible `resource_type` registry and the internal-call pattern.

## 30. Definition of Done
- No client-facing audit-write endpoint exists anywhere.
- `audit_log` table append-only at the database-permission level.
- `AuditLogService.log_action()` is the sole write path, called internally by other services.
- `GET /v1/admin/audit-logs` fully functional with filtering/pagination and Edge Case 8 handling.
- Both signature tests (no-client-write, DB-permission-lockout) pass and are CI-blocking.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/audit-logs` no longer exists (404)
- [ ] Architectural test confirms no client-writable audit path anywhere in the API surface
- [ ] `audit_log` has no `UPDATE`/`DELETE` grant for the application DB role (verified by failing test attempt)
- [ ] `GET /v1/admin/audit-logs` supports actor/resource/action filters and cursor pagination
- [ ] Pre-deployment date-range query returns empty result, never an error (Edge Case 8)
- [ ] All existing/new callers (B-04, B-06, B-07, B-09) use `AuditLogService.log_action()` internally
- [ ] No secrets/PII leak into `metadata` jsonb
- [ ] Breaking-change migration note documented
