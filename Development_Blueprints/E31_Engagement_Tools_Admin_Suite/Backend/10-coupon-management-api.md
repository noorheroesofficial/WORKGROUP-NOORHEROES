# B-10 — Coupon Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers a new, lightweight Coupon Service for promotional coupon CRUD with atomic, race-condition-proof redemption-cap enforcement. Source: PRD §1.7 FR-8, §3.4, §5 item 6.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.10 Coupon Management API (Backend ID: **B-10**)

## 4. Objective
Let content admins manage promotional coupons with mandatory usage caps and expiry, while structurally guaranteeing that redemption enforcement is atomic — never a race-prone read-then-write — so concurrent redemption attempts can never exceed the configured cap.

## 5. Business Requirements
- FR-8 (PRD §1.7): screens — coupon list, coupon editor, redemption report. CRUD: create/read/update/deactivate `coupons`.
- **Hard rule:** discount percentage/amount bounds enforced server-side.
- **Hard rule:** usage caps and expiry are mandatory fields, not optional.
- Edge Case 6 (PRD §1.10): a coupon's usage cap is reached exactly as two different parents attempt to redeem it within the same second — server-side usage-cap enforcement must correctly allow only up to the cap, using an atomic counter-check, never a race-prone read-then-write.

## 6. Existing Architecture
New, lightweight service per PRD §3.3. FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering, consistent with B-09.

## 7. Existing Code to Reuse
- E.28's audit log client + RBAC dependency.
- C.24's Subscription/Billing infrastructure, if coupon redemption is triggered from the billing checkout flow (cross-ref; this sub-feature is authoring-only — actual redemption-triggering integration lives wherever checkout is implemented, but the atomic redemption-increment primitive belongs to this service since it owns the `coupon` table).

## 8. Files to Create
- `app/routers/admin/coupons_router.py`
- `app/schemas/admin/coupon_schemas.py`
- `app/services/admin/coupon_admin_service.py`
- `app/repositories/admin/coupon_admin_repository.py`
- `app/models/coupon.py`
- `tests/admin/test_coupon_admin_api.py`
- `migrations/versions/xxxx_create_coupon_table.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`coupon.created`, `coupon.updated`, `coupon.deactivated`, `coupon.redemption_cap_reached`)

## 10. Backend Requirements
- **Database:** new `coupon` table per PRD §4.2 — `coupon_id PK`, `code UNIQUE`, `discount_type`, `discount_value`, `usage_cap`, `redeemed_count`, `expires_at`, `active`.
- **Migration:** new table with `CHECK (redeemed_count <= usage_cap)`, `CHECK (expires_at IS NOT NULL)`, `CHECK (usage_cap IS NOT NULL)`.
- **Model:** `Coupon`.
- **Schema/DTO:** `CouponCreate` (`code`, `discount_type`, `discount_value`, `usage_cap` **required**, `expires_at` **required**), `CouponUpdate`, `CouponRead` (includes `redemption_report` summary).
- **Repository:** `create()`, `list()`, `update()`, `deactivate()`, `atomic_redeem(coupon_id)` — implemented as a **single** `UPDATE coupon SET redeemed_count = redeemed_count + 1 WHERE coupon_id = ? AND redeemed_count < usage_cap AND active = true AND expires_at > now() RETURNING *`, never a SELECT-then-UPDATE pattern.
- **Service:** `CouponAdminService` — server-side bounds-checks `discount_value` (e.g., percent ∈ (0, 100]); enforces `usage_cap`/`expires_at` as mandatory at the schema level (non-Optional Pydantic fields, no default); calls `atomic_redeem` for the redemption path (exposed here since this service owns the table, even though the triggering caller may be a billing/checkout flow elsewhere).
- **Router:** `POST /v1/admin/coupons`, `GET /v1/admin/coupons`, `PATCH /v1/admin/coupons/{id}`, `POST /v1/admin/coupons/{id}/deactivate`, `GET /v1/admin/coupons/{id}/redemption-report`.
- **Dependency Injection:** `require_role_any(["content_editor", "billing_ops"])`.
- **Validation:** `discount_value` bounds per `discount_type` (percent 1–100, fixed-amount positive and below a configured max); `usage_cap` positive integer, required; `expires_at` future timestamp, required; `code` unique.
- **Business Rules:** redemption-cap enforcement MUST be a single atomic SQL statement — this is the sub-feature's highest-priority guarantee (PRD §5 item 6, flagged highest-priority alongside B-01/B-05's no-retroactivity guarantees).
- **Exception Handling:** `409 USAGE_CAP_REACHED` when `atomic_redeem` returns no row; `409 COUPON_EXPIRED`; `409 COUPON_INACTIVE`.
- **Logging:** log every cap-reached rejection (`coupon_redemption_cap_reached`).
- **Caching:** N/A — redemption must always hit the DB for correctness; no cached counter permitted for the authoritative check.
- **Transaction:** the atomic `UPDATE ... RETURNING` statement is itself the transaction boundary for redemption; no separate read step.
- **Pagination/Filtering/Sorting:** coupon list paginated, filterable by active/expired status.

## 11. KMP Requirements
N/A — admin-only authoring. Coupon redemption itself is triggered from the parent-facing subscription/billing checkout flow (C.24), not from this admin layer or from the KMP child app directly.

## 12. NextJS Requirements
Consumed by **N-10 Coupon Management UI**, whose Redemption Report screen must correctly reflect atomic-cap-enforcement results (e.g., a concurrency test scenario's outcome).

## 13. API Contract

### `POST /v1/admin/coupons`
- **Request:**
```json
{ "code": "RAMADAN2026", "discount_type": "percent", "discount_value": 20, "usage_cap": 500, "expires_at": "2026-09-30T23:59:59Z" }
```
- **Response (201):** `CouponRead`
- **Errors:** `401`, `403`, `422 VALIDATION_ERROR` (missing/invalid `usage_cap`/`expires_at`/bounds), `409 DUPLICATE_CODE`

### `POST /v1/admin/coupons/{id}/deactivate`
- **Response (200):** `{ "id": "uuid", "active": false }`

### `GET /v1/admin/coupons/{id}/redemption-report`
- **Response (200):** `{ "usage_cap": 500, "redeemed_count": 487, "redemption_rate": 0.974 }`

### (Internal/cross-service) `POST /v1/internal/coupons/{id}/redeem`
- Not part of the admin-authoring surface but documented here since this service owns the atomic operation: single `UPDATE ... WHERE redeemed_count < usage_cap RETURNING *`; returns `409 USAGE_CAP_REACHED` if no row affected.

## 14. Database Requirements
- `coupon`: per PRD §4.2 — `CHECK (redeemed_count <= usage_cap)`, `CHECK (expires_at IS NOT NULL)`, `CHECK (usage_cap IS NOT NULL)`, `UNIQUE(code)`, index `(code)`.

## 15. Validation
`usage_cap` and `expires_at` non-nullable at both schema and DB CHECK level; `discount_value` bounds server-checked per `discount_type`.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+/`billing_ops`.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Redemption attempted beyond cap | `409 USAGE_CAP_REACHED` (via atomic no-row-returned) |
| Redemption attempted on expired coupon | `409 COUPON_EXPIRED` |
| Missing `usage_cap`/`expires_at` on create | `422 VALIDATION_ERROR` |
| Duplicate `code` | `409 DUPLICATE_CODE` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Coupon-related UI copy localized in the admin/parent surfaces; `code` itself is not localized.

## 22. RTL
N/A at API layer.

## 23. Analytics
`coupon_created`, `coupon_redemption_cap_reached` per PRD §1.19.

## 24. Performance
Single atomic `UPDATE ... RETURNING` for redemption is both a correctness and performance guarantee — avoids lock contention from a separate SELECT step; index on `code` for fast lookup.

## 25. Security
Atomic, race-condition-proof redemption enforcement is this sub-feature's primary economy-integrity contribution (PRD §12.7); mandatory bounds fields prevent misconfigured/unbounded discounts.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async (raw `UPDATE ... RETURNING` via Core or ORM `update().returning()`), Pydantic v2, pytest-asyncio, `asyncio.gather` for concurrency testing.

## 27. Testing
- Unit: discount-bounds validation.
- Integration: signature concurrency test — fire 10 concurrent redemption attempts against a coupon with `usage_cap=5`, confirm EXACTLY 5 succeed, never more, regardless of request timing (PRD §5 item 6, highest-priority guarantee).
- Edge cases: Edge Case 6 explicitly — two redemptions in the same second at the cap boundary.
- Negative cases: missing mandatory fields, duplicate code, expired coupon redemption attempt.

## 28. Documentation
OpenAPI docs explicitly describing the atomic single-statement redemption-cap enforcement mechanism, since this is easy to accidentally regress into a read-then-write pattern in future maintenance.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model & Migration**
- Task ID: B-10-T01
- Files to Create: `app/models/coupon.py`, migration per §14.
- Tests: migration test; direct-SQL test confirming `CHECK` constraints reject invalid rows.
- Dependencies: none.
- Definition of Done: migration applies cleanly.

**Task 02 — Atomic Redemption Repository Method**
- Task ID: B-10-T02
- Objective: Implement `atomic_redeem` as a single `UPDATE ... WHERE redeemed_count < usage_cap RETURNING *` statement.
- Files to Create: `app/repositories/admin/coupon_admin_repository.py`.
- Implementation Details: use SQLAlchemy Core `update().where(...).returning(...)` executed in one round-trip; no preceding SELECT.
- Tests: unit test confirming the generated SQL is a single statement (no separate read query issued).
- Dependencies: Task 01.
- Definition of Done: unit test green.

**Task 03 — Service & CRUD Endpoints**
- Task ID: B-10-T03
- Files to Create: `app/services/admin/coupon_admin_service.py`, `app/routers/admin/coupons_router.py`.
- Implementation Details: mandatory-field enforcement at Pydantic schema level (no `Optional`/default for `usage_cap`/`expires_at`).
- Dependencies: Task 02.
- Definition of Done: integration tests green.

**Task 04 — Concurrency Signature Test**
- Task ID: B-10-T04
- Objective: Prove Edge Case 6 / PRD §5 item 6's highest-priority guarantee.
- Implementation Details: seed a coupon with `usage_cap=5`; use `asyncio.gather` to fire 10 concurrent calls to `atomic_redeem`; assert exactly 5 return a row and 5 return `None`/`409`.
- Tests: `tests/admin/test_coupon_admin_api.py::test_concurrent_redemption_never_exceeds_cap`.
- Dependencies: Tasks 01–03.
- Definition of Done: test passes deterministically across repeated runs; part of CI-blocking suite per PRD §10.

**Task 05 — Documentation & Final Review**
- Task ID: B-10-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Atomic redemption-cap enforcement proven under concurrent load (exactly cap succeeds, never more); mandatory-field enforcement proven; full CRUD implemented, audited, and tested.

## 31. Final Verification Checklist
- [ ] `usage_cap` and `expires_at` mandatory at creation, rejected if missing (`422`)
- [ ] Discount bounds server-enforced per `discount_type`
- [ ] Redemption implemented as a single atomic `UPDATE ... RETURNING` statement (no read-then-write)
- [ ] 10 concurrent redemption attempts against `usage_cap=5` → exactly 5 succeed (regression test green)
- [ ] Expired/inactive coupon redemption rejected
- [ ] Duplicate `code` rejected
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
