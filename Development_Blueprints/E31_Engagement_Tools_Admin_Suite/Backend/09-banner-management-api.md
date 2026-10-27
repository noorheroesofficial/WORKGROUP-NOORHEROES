# B-09 — Banner Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers a new, lightweight Banner Service for promotional/seasonal banner CRUD. Source: PRD §1.9 FR-7, §3.4, §5 item 7.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.9 Banner Management API (Backend ID: **B-09**)

## 4. Objective
Let content admins manage promotional/seasonal banners with a placement scheduler, while structurally guaranteeing that no child-facing banner may ever link to an external (non-NoorHeroes) destination, while permitting external links for parent-facing placements where intentionally reviewed.

## 5. Business Requirements
- FR-7 (PRD §1.7): screens — banner list, banner editor, placement scheduler. CRUD: create/read/update/delete `banners`.
- **Hard rule:** banner imagery passes the content-safety pipeline.
- **Hard rule:** no banner may link to an external destination for child-facing placements.
- Edge Case 8 (PRD §1.10): a child-facing placement's external destination link is rejected at validation time; the same banner type configured for a parent-facing placement (e.g., Subscription upsell) may legitimately link externally — the restriction is scoped to child-facing placements specifically, not banners universally.

## 6. Existing Architecture
New, lightweight service per PRD §3.3 — not an extension of an existing engine, since no prior feature specified banners as a first-class engine. Follows the same FastAPI/SQLAlchemy 2.0/PostgreSQL Router → Service → Repository layering as every other module in this suite for consistency.

## 7. Existing Code to Reuse
- E.28's audit log client + RBAC dependency.
- E.29's shared content-safety/upload-validation pipeline for banner imagery — no parallel upload-safety check implemented here.

## 8. Files to Create
- `app/routers/admin/banners_router.py`
- `app/schemas/admin/banner_schemas.py`
- `app/services/admin/banner_admin_service.py`
- `app/repositories/admin/banner_admin_repository.py`
- `app/models/banner.py`
- `tests/admin/test_banner_admin_api.py`
- `migrations/versions/xxxx_create_banner_table.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`banner.created`, `banner.updated`, `banner.deleted`, `banner.external_link_child_facing_blocked`)

## 10. Backend Requirements
- **Database:** new `banner` table per PRD §4.2 — `banner_id PK`, `placement`, `destination_url`, `is_child_facing`, `starts_at`, `ends_at`, `status`.
- **Migration:** new table, additive.
- **Model:** `Banner`.
- **Schema/DTO:** `BannerCreate` (`placement`, `destination_url`, `is_child_facing`, `starts_at`, `ends_at`, `image_asset_id`), `BannerUpdate`, `BannerRead`.
- **Repository:** `create()`, `list()`, `update()`, `delete()`.
- **Service:** `BannerAdminService` — validates `destination_url` against an internal-domain pattern (`noorheroes://` or `noorheroes.com`) whenever `is_child_facing=true`; routes imagery through E.29's pipeline; audit logs.
- **Router:** `POST /v1/admin/banners`, `GET /v1/admin/banners`, `PATCH /v1/admin/banners/{id}`, `DELETE /v1/admin/banners/{id}`.
- **Dependency Injection:** `require_role("content_editor")`.
- **Validation:** `is_child_facing=true` → `destination_url` must match internal-domain pattern, else `422`; `is_child_facing=false` → any valid URL permitted; `starts_at < ends_at`.
- **Business Rules:** the external-link restriction is scoped specifically to `is_child_facing=true` placements (Edge Case 8) — the service must not apply this restriction universally.
- **Exception Handling:** `422 EXTERNAL_LINK_NOT_ALLOWED_CHILD_FACING`.
- **Logging:** log every rejected external-link-for-child-facing attempt as a security signal (`banner_external_link_child_facing_blocked`).
- **Caching:** invalidate cached "active banners by placement" list on write.
- **Transaction:** create/update + audit log in one transaction.
- **Pagination/Filtering/Sorting:** list paginated, filterable by placement/status/is_child_facing.

## 11. KMP Requirements
N/A — admin-only. The KMP app consumes active banners via its own existing home-dashboard/content-surface endpoints (A.2), unaffected by this admin-authoring layer beyond the data it produces.

## 12. NextJS Requirements
Consumed by **N-09 Banner Management UI**, whose Banner Editor must conditionally show/validate `destination_url` based on the selected placement's `is_child_facing` flag, mirroring this backend's scoped validation.

## 13. API Contract

### `POST /v1/admin/banners`
- **Request (child-facing, must be internal):**
```json
{ "placement": "child_home_top", "destination_url": "noorheroes://stories/ramadan-collection", "is_child_facing": true, "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-08T00:00:00Z", "image_asset_id": "uuid" }
```
- **Request (parent-facing, external permitted):**
```json
{ "placement": "parent_subscription_upsell", "destination_url": "https://noorheroes.com/pricing", "is_child_facing": false, "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-08T00:00:00Z", "image_asset_id": "uuid" }
```
- **Response (201):** `BannerRead`
- **Errors:** `401`, `403`, `422 EXTERNAL_LINK_NOT_ALLOWED_CHILD_FACING`, `422 IMAGE_UPLOAD_REJECTED`

### `GET /v1/admin/banners` / `PATCH /v1/admin/banners/{id}` / `DELETE /v1/admin/banners/{id}`
Standard CRUD semantics per §10.

## 14. Database Requirements
- `banner`: per PRD §4.2 — application-layer CHECK (documented as binding rule, not a raw DB CHECK given regex constraints) that `is_child_facing=true` → `destination_url` matches internal-domain pattern. Index `(placement, starts_at, ends_at)`.

## 15. Validation
`destination_url` scoped internal-only when `is_child_facing=true`; `starts_at < ends_at`; `placement` valid enum/registry value.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | Response |
|---|---|
| External URL for child-facing placement | `422 EXTERNAL_LINK_NOT_ALLOWED_CHILD_FACING` |
| Image fails upload-safety pipeline | `422 IMAGE_UPLOAD_REJECTED` |
| `starts_at >= ends_at` | `422 VALIDATION_ERROR` |
| Unknown banner id | `404 NOT_FOUND` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Banner copy/alt-text should reference localization keys for multi-locale rendering (English/Hindi/Arabic/Urdu).

## 22. RTL
N/A at API layer (banner imagery RTL mirroring, if needed, handled at content-creation/design time).

## 23. Analytics
`banner_created`, `banner_external_link_child_facing_blocked` (internal/security signal) per PRD §1.19.

## 24. Performance
Active-banner-by-placement list cached in Redis, invalidated on write.

## 25. Security
Child-facing external-link restriction is this sub-feature's primary child-safety contribution (PRD §12.7), enforced as placement-scoped service-layer validation, not a UI-only convention.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, `urllib.parse` (or equivalent) for domain-pattern validation, pytest-asyncio.

## 27. Testing
- Unit: internal-domain pattern matching logic.
- Integration: signature test — external `destination_url` rejected for `is_child_facing=true`; second test confirming external `destination_url` permitted for `is_child_facing=false` (PRD §5 item 7, both required).
- Edge cases: Edge Case 8 explicitly.
- Negative cases: unauthorized, invalid date range.

## 28. Documentation
OpenAPI docs explicitly describing the placement-scoped (not universal) external-link restriction.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model & Migration**
- Task ID: B-09-T01
- Files to Create: `app/models/banner.py`, migration creating the `banner` table per §14.
- Tests: migration up/down test.
- Dependencies: none.
- Definition of Done: migration applies cleanly on staging.

**Task 02 — Internal-Domain Validation Utility**
- Task ID: B-09-T02
- Objective: Build a reusable domain-pattern validator (`noorheroes://` or `noorheroes.com`).
- Files to Create: part of `app/services/admin/banner_admin_service.py`, or a shared `app/core/url_validation.py` if reusable elsewhere.
- Tests: unit tests covering valid internal URLs, invalid external URLs, edge-case malformed URLs.
- Dependencies: Task 01.
- Definition of Done: validator unit-tested in isolation.

**Task 03 — Repository & Service Layers**
- Task ID: B-09-T03
- Files to Create: `app/repositories/admin/banner_admin_repository.py`, `app/services/admin/banner_admin_service.py`.
- Implementation Details: scoped validation applied only when `is_child_facing=true`.
- Dependencies: Task 02.
- Definition of Done: unit tests green.

**Task 04 — API Endpoints**
- Task ID: B-09-T04
- Files to Create: `app/routers/admin/banners_router.py`.
- Dependencies: Task 03.
- Definition of Done: integration tests green.

**Task 05 — Signature Scoped-Restriction Test**
- Task ID: B-09-T05
- Implementation Details: two-part test per PRD §5 item 7 — child-facing external link rejected, parent-facing external link permitted.
- Tests: `tests/admin/test_banner_admin_api.py::test_child_facing_external_link_rejected`, `::test_parent_facing_external_link_permitted`.
- Dependencies: Tasks 01–04.
- Definition of Done: both tests green, part of CI-blocking suite.

**Task 06 — Documentation & Final Review**
- Task ID: B-09-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Placement-scoped external-link restriction proven both ways (blocked for child-facing, permitted for parent-facing); full CRUD implemented, audited, and tested.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/banners` rejects external URL for `is_child_facing=true`
- [ ] `POST /v1/admin/banners` permits external URL for `is_child_facing=false`
- [ ] Image routed through E.29 upload-safety pipeline, rejection path tested
- [ ] `starts_at < ends_at` enforced
- [ ] Full CRUD (create/read/update/delete) functional
- [ ] Audit log entries written for every mutation, including blocked attempts
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
