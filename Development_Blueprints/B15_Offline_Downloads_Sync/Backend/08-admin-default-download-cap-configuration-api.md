# B-08 — Admin Default Download Cap Configuration API

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Lets `product_admin` configure the fallback per-plan default download cap consumed by B-03 whenever a parent hasn't set a custom cap — the write-side counterpart to N-03's settings form.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-08 — Admin Default Download Cap Configuration API

## 4. Objective
Implement `GET`/`PUT /v1/admin/downloads/default-caps`, mapping subscription plan codes to default per-child download caps, restricted to `product_admin`, writing an immutable audit-log row on every change, and guaranteeing changes never retroactively override a parent's already-configured custom cap.

## 5. Business Requirements
- §8 Admin Requirements: Per-Plan Default Download Cap Configuration — admin-tunable default caps per subscription tier, Update-only behind `product_admin`.
- §9 Admin AI Prompt item 3: settings form mapping plan codes to default caps, restricted to `product_admin`; changes here only affect future defaults, never retroactively altering a parent's already-configured custom cap.
- §12.5 Admin Security: cap-default changes don't retroactively override parent settings.

## 6. Existing Architecture
New table + routes in the `downloads` bounded context (`src/noorheroes/modules/downloads/`), reusing the `admin` module's `AdminAuditRepository`/`AdminService.log_action()` for the audit trail rather than building a parallel audit mechanism.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_admin`, `require_admin_scope("admin:write")`.
- `admin` module's `AdminAuditRepository.log_action()` — writes the immutable audit row.
- `common/base_repository.py` → `BaseRepository[ModelT].update_with_optimistic_lock()` for concurrent-edit safety.
- `subscriptions` module's `SubscriptionPlan` model — the plan-code source of truth this table's `plan_code` foreign-keys against.

## 8. Files to Create
- `src/noorheroes/modules/downloads/models.py` (extend) — `DownloadDefaultCapConfigOrm`.
- `src/noorheroes/modules/downloads/schemas.py` (extend) — `DefaultCapConfigResponse`, `DefaultCapConfigUpdateRequest`.
- `src/noorheroes/modules/downloads/repository.py` (extend) — `DefaultCapConfigRepository`.
- `tests/modules/downloads/test_admin_default_cap_config_api.py`.
- `tests/modules/downloads/test_default_cap_non_retroactive.py`.
- Alembic migration: `create_download_default_cap_config_table.py`.

## 9. Files to Modify
- `modules/downloads/service.py` — add `DefaultCapConfigService` (or extend `DownloadService`) with `get_default_caps()`, `update_default_cap(plan_code, cap_bytes, admin_ctx)`.
- `modules/downloads/api.py` — add `GET`/`PUT /v1/admin/downloads/default-caps`.

## 10. Backend Requirements
- `GET /v1/admin/downloads/default-caps`: returns all plan-code → cap mappings.
- `PUT /v1/admin/downloads/default-caps`: updates one or more plan-code mappings; uses `update_with_optimistic_lock()` against each row's `version` to reject stale concurrent edits with a clear conflict error rather than silently overwriting.
- Every successful update calls `AdminService.log_action()` writing an immutable `AdminAuditLog` row capturing `admin_id`, `plan_code`, `old_cap_bytes`, `new_cap_bytes`, `timestamp`.
- Writing here never touches C.23's parent-custom-cap table — B-03's `resolve_effective_cap()` only consults this table when no parent-custom cap exists, so an admin default change is structurally incapable of overriding an existing custom cap (enforced by B-03's read-order, not by any logic in this endpoint).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by N-03 (Per-Plan Default Download Cap Configuration) via its settings-form hook.

## 13. API Contract
**Endpoint 1:** `GET /v1/admin/downloads/default-caps`
**Response 200:**
```json
{ "caps": [ { "plan_code": "free", "cap_bytes": 1073741824, "version": 3 } ] }
```
**Endpoint 2:** `PUT /v1/admin/downloads/default-caps`
**Request:**
```json
{ "updates": [ { "plan_code": "free", "cap_bytes": 2147483648, "version": 3 } ] }
```
**Response 200:** updated `caps[]` in the same shape as the `GET`.
**Error Responses:** `409` (optimistic-lock version mismatch — a concurrent edit occurred), `422` (invalid `cap_bytes`, unknown `plan_code`), `403` (missing `admin:write`).
**Auth (both):** Bearer, admin, `Depends(get_current_admin)` + `admin:write` scope.

## 14. Database Requirements
- New table `downloads_default_cap_config`: `plan_code VARCHAR PK/FK → subscription_plan`, `cap_bytes BIGINT NOT NULL CHECK (cap_bytes >= 0)`, plus `TimestampMixin` (`created_at`, `updated_at`, `version`).
- No PostgreSQL/Redis credential changes.

## 15. Validation
- `cap_bytes` non-negative, bounded to a sane maximum (e.g., prevent an accidental typo setting an effectively-unlimited cap).
- `plan_code` must reference an existing `SubscriptionPlan`.
- `version` required on every update entry (optimistic-lock enforcement — a request omitting it is `422`, not treated as "always overwrite").

## 16. Authentication
`Depends(get_current_admin)` on both routes.

## 17. Authorization
`admin:write` scope required for `PUT`; `GET` may use the broader `admin:read` (consistent with B-07's read-only pattern) since viewing current defaults is lower-risk than changing them.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Concurrent edit (stale `version`) | `409`, no partial write; client must re-fetch and retry |
| Invalid `cap_bytes` | `422` |
| Unknown `plan_code` | `422` |
| Missing `admin:write` scope | `403` |
| Update succeeds | `200`, audit log row written in the same transaction |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A — admin-portal-side localization handled by N-03's rendering layer.

## 22. RTL
N/A.

## 23. Analytics
No dedicated client event; every change is captured in the `AdminAuditLog` (queryable via the existing `AdminRouter`'s audit-log endpoints), which is the authoritative change history for this configuration.

## 24. Performance
Small, low-cardinality table (one row per subscription plan) — no special performance considerations beyond standard indexed PK lookups.

## 25. Security
- Stricter scope (`admin:write`) than the two read-only health monitors (B-07), reflecting its higher-risk, state-mutating nature.
- Non-retroactive-override guarantee is structural (B-03's read-order), not merely a documented convention — verified by a dedicated test (§27) that changing a plan default has zero effect on a fixture family with an existing parent-custom cap.
- Every write is audit-logged immutably; no update path bypasses `AdminService.log_action()`.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), asyncpg. No new libraries.

## 27. Testing
- Unit: valid update succeeds, audit log row written with correct old/new values.
- Unit: stale-`version` update rejected with `409`, no partial write.
- **Non-retroactive-override test (mandatory):** fixture family with an existing parent-custom cap; admin changes the plan default; assert `B-03.resolve_effective_cap()` for that family is unaffected (still returns the parent-custom value), while a different family on the same plan **without** a custom cap correctly picks up the new default.
- RBAC test: `GET` without `admin:read` and `PUT` without `admin:write` both correctly rejected.

## 28. Documentation
OpenAPI summaries for both routes; explicit doc note on the optimistic-lock `version` requirement and the non-retroactive-override guarantee, cross-referenced to B-03 §5.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create DownloadDefaultCapConfigOrm Model & Migration**
Files to create: extend `modules/downloads/models.py`, migration file.

**Task 02 — Define Schemas**
Files to create: extend `modules/downloads/schemas.py`.

**Task 03 — Implement DefaultCapConfigRepository**
Objective: standard CRUD via `BaseRepository`, `update_with_optimistic_lock()` for the update path.
Files to modify: `modules/downloads/repository.py`.

**Task 04 — Implement Service Layer with Audit Logging**
Objective: `get_default_caps()`, `update_default_cap()` calling `AdminService.log_action()`.
Files to modify: `modules/downloads/service.py`.

**Task 05 — Implement Admin Routes**
Objective: `GET`/`PUT /v1/admin/downloads/default-caps`, scope-gated.
Files to modify: `modules/downloads/api.py`.

**Task 06 — Add Non-Retroactive-Override Test (highest priority)**
Tests: `test_default_cap_non_retroactive.py`.
Definition of done: CI-blocking gate.

**Task 07 — Add Full Test Suite & OpenAPI Docs**

**Task 08 — Final Code Review**
Objective: confirm every write path calls `AdminService.log_action()`; confirm B-03's read-order (custom-then-default) is unchanged by this sub-feature.

## 30. Definition of Done
- Both routes live, matching §13 contracts.
- Optimistic-lock conflict handling verified.
- Non-retroactive-override guarantee verified by test.
- Every write produces an audit log row.

## 31. Final Verification Checklist
- [ ] `admin:write` required for mutation, `admin:read` sufficient for read.
- [ ] Stale-version concurrent edits rejected with `409`, no silent overwrite.
- [ ] Changing a plan default never affects a family with an existing custom cap — verified by test.
- [ ] Every successful update writes an immutable audit log row.
- [ ] `cap_bytes` validated non-negative and bounded.
- [ ] No PostgreSQL/Redis credentials modified.
