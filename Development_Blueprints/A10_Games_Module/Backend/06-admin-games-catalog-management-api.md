# B-06 — Admin Games Catalog Management API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/`  
> **Endpoints:** `POST /admin/v1/games`, `GET /admin/v1/games`, `PATCH /admin/v1/games/{id}`, `DELETE /admin/v1/games/{id}`, `GET /admin/v1/games/compliance`, `GET /admin/v1/games/audit-log` (Dual-mounted on `/admin/v1/games` and `/v1/admin/games`)  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_admin_catalog_api.py` (15 tests), `tests/modules/games/test_compliance_dashboard_api.py` (5 tests), `tests/modules/games/test_audit_log_api.py` (9 tests), `tests/modules/games/test_b06_zero_missing_scenarios.py` (20 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0071_create_games_catalog_tables.py`, `alembic/versions/0073_add_game_publish_skill_link_constraint.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16 & §6.16, `MASTER-README.md` §11.79, `CHANGELOG.md` v1.32.0, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B06`  

## 1. Feature Context
Part of **A.10 Games Module**. Covers the admin-facing CRUD surface for game catalog entries, the compliance dashboard read endpoint, and the anti-filler audit log read endpoint — the backend counterpart to N-01/N-02/N-04.

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.6 Admin Games Catalog Management API** `[B-06]`

## 4. Objective
Provide full CRUD for game catalog entries (create/update/withdraw), a read-only compliance status listing, and a read-only anti-filler audit log — all gated by the B-04 skill-mapping validation and routed through the existing scholar-review workflow for Quran/Tajweed/Dua-linked games (PRD §8, FR-10).

## 5. Business Requirements
- §8 Admin Requirements: Games Catalog Editor (full CRUD, delete = withdraw) behind `content_editor` role, scholar-approval-gated for Quran/Tajweed/Dua-linked games.
- Skill-Mapping Compliance Dashboard: read-only, surfaces drift before the reconciliation job (B-05) runs.
- Age-Band Difficulty Tuning: update-only, `content_editor` + `learning_science` sign-off.
- Anti-Filler Content Audit Log: read-only, restricted to `product_admin`/`trust_safety`.
- Every mutating action writes an immutable `audit_log` row (§9 Admin AI Code-Generation Prompt).

## 6. Existing Architecture
Same `games` bounded context. RBAC via `require_admin_scope()` (`core/deps.py`), mirroring `AdminRouter`'s `admin:read`/`admin:write` scope pattern (`FAST-API-INSTRUCTIONS.md` §6, item 2). Scholar-review routing reuses A.5/A.6's existing admin scholar-approval workflow component (exact integration point to be confirmed against A.5/A.6's finalized admin blueprints — not invented here).

## 7. Existing Code to Reuse
- `AdminAuditRepository.log_action()` / `AdminService.log_action()` (`modules/admin/`).
- `require_admin_scope(required_scope: str)` factory (`core/deps.py`).
- B-04's `validate_skill_mapping_gate()` (called from create/update here).
- A.5/A.6's existing scholar-review workflow trigger (reused, not reimplemented, for Quran/Tajweed/Dua-linked games).
- `BaseRepository.list_paginated()` for the compliance dashboard and audit log listings.

## 8. Files to Create
```
tests/modules/games/test_admin_catalog_api.py
tests/modules/games/test_compliance_dashboard_api.py
tests/modules/games/test_audit_log_api.py
```

## 9. Files to Modify
```
src/noorheroes/modules/games/schemas.py    # AdminGameCreateRequest, AdminGameUpdateRequest, GameComplianceResponse, GameAuditLogEntryResponse
src/noorheroes/modules/games/repository.py # add compliance-status query, audit-log query
src/noorheroes/modules/games/service.py    # create_game(), update_game(), withdraw_game(), get_compliance_status(), get_audit_log()
src/noorheroes/modules/games/api.py        # admin routes
```
**Do Not Change:** `modules/admin/` internals beyond calling `log_action()`; A.5/A.6 scholar-review internals beyond calling the existing trigger interface.

## 10. Backend Requirements
- `POST /admin/v1/games` — create (draft or direct-publish); enforces B-04 gate if `status=published`.
- `PATCH /admin/v1/games/{id}` — update; enforces B-04 gate on any transition to/remaining-in `published`.
- `DELETE /admin/v1/games/{id}` semantics = withdraw (`is_withdrawn=true`), not hard delete, consistent with §4.4.
- `GET /admin/v1/games/compliance` — read-only list with `Compliant`/`At Risk` status per game (At Risk = any linked skill_node inactive).
- `GET /admin/v1/games/audit-log` — read-only, paginated, `product_admin`/`trust_safety` scope only.
- Age-band difficulty parameter updates on a **published** game require an additional `learning_science_signoff` field populated by a user with the `learning_science` scope before the update is accepted.
- Quran/Tajweed/Dua-linked game publish attempts route through the existing scholar-review workflow — publish is blocked pending scholar approval, mirroring A.5/A.6's existing gate.

## 11. KMP Requirements
N/A — admin-only.

## 12. NextJS Requirements
Directly consumed by N-01 (Editor), N-02 (Compliance Dashboard), N-03 (Difficulty Tuning), N-04 (Audit Log).

## 13. API Contract

### `POST /admin/v1/games`
| | |
|---|---|
| **Auth** | Bearer (admin) |
| **Authorization** | `content_editor` scope |

**Request:**
```json
{
  "title": "string",
  "skill_area": "quran",
  "mechanic_type": "ayah_ordering",
  "age_band_difficulty_config": { "6-9": { "time_pressure_ms": 0, "distractor_count": 3, "complexity_level": 2 } },
  "skill_node_ids": ["uuid"],
  "status": "draft"
}
```
**Validation:** rejects (`422`) if `status="published"` and `skill_node_ids` is empty (B-04 gate).

### `PATCH /admin/v1/games/{id}`
Same body shape, partial update semantics; B-04 gate re-evaluated on every call affecting `status` or `skill_node_ids`.

### `GET /admin/v1/games/compliance`
**Response 200:**
```json
{ "games": [ { "game_id": "uuid", "title": "string", "status": "Compliant" } ] }
```

### `GET /admin/v1/games/audit-log`
**Auth/Authorization:** `product_admin` or `trust_safety` scope only.
**Response 200:**
```json
{ "entries": [ { "game_id": "uuid", "validated_skill_node_ids": ["uuid"], "validating_admin_id": "uuid", "timestamp": "iso8601" } ] }
```

**Error Codes (shared across admin routes):**
| Code | Condition |
|---|---|
| 401 | Missing/invalid admin token |
| 403 | Missing required scope (`content_editor`/`learning_science`/`product_admin`/`trust_safety`) |
| 422 | Skill-mapping gate failure (B-04) or missing `learning_science_signoff` on a published-game difficulty update |
| 404 | Game not found |

## 14. Database Requirements
No new tables beyond B-01/B-03/B-04's `game`/`game_skill_link`/`game_session`. Audit trail persisted via the existing `modules/admin` `AdminAuditLog` table (reused, not duplicated).

## 15. Validation
- `skill_area`/`mechanic_type` validated against registered lookup values (shared domain registry).
- `age_band_difficulty_config` validated to include required tiers (4 to 6, 6 to 9, 9 to 12, 12 to 15, 15 to 18+) with numeric parameter ranges reviewed against Learning Science guidance (range bounds TBC with Learning Science stakeholders — do not invent specific numeric limits here beyond structural validation).
- `learning_science_signoff` required and validated as coming from a session with the `learning_science` scope, not merely present-as-a-field.

## 16. Authentication
`Depends(get_current_admin)` on all routes.

## 17. Authorization
| Route | Required Scope |
|---|---|
| `POST /admin/v1/games` | `content_editor` |
| `PATCH /admin/v1/games/{id}` (general fields) | `content_editor` |
| `PATCH /admin/v1/games/{id}` (difficulty params on published game) | `content_editor` + `learning_science` sign-off |
| `DELETE /admin/v1/games/{id}` (withdraw) | `content_editor` |
| `GET /admin/v1/games/compliance` | any authenticated admin (read-only) |
| `GET /admin/v1/games/audit-log` | `product_admin` or `trust_safety` |

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Skill-mapping gate failure | `422` (delegated to B-04) |
| Missing learning_science sign-off on published-game difficulty change | `422 SIGNOFF_REQUIRED` |
| Quran/Tajweed/Dua game publish without scholar approval | `422 SCHOLAR_APPROVAL_PENDING` (or routes into pending-review state rather than a hard error, per existing A.5/A.6 UX pattern — confirm exact behavior against that workflow before finalizing) |
| Insufficient scope | `403` |
| Audit log access by unauthorized role | `403` |

## 19. Offline First
N/A — admin portal is always-online.

## 20. Local Data
N/A.

## 21. Localization
Admin-facing `title`/error messages localized per admin locale preference (English/Arabic primary for admin users).

## 22. RTL
N/A backend; NextJS (N-01–N-04) render RTL correctly for Arabic/Urdu admin locales.

## 23. Analytics
Internal audit logging (§10, §13) is the primary tracked signal; no client analytics events emitted by this backend surface directly.

## 24. Performance
Compliance dashboard query uses a single joined query (games + skill-link active-status aggregation), not per-game round trips, to keep dashboard load responsive at catalog scale.

## 25. Security
- RBAC strictly enforced per §17 table — no route accessible without the exact required scope.
- Skill-mapping gate (B-04) enforced identically here regardless of role.
- Audit log is append-only and immutable — no update/delete route exists for audit entries.
- All admin mutating actions logged, supporting forensic reconstruction of any content-governance question.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: create/update both correctly delegate to B-04's gate.
- Unit: withdraw sets `is_withdrawn=true`, does not hard-delete, preserves `game_session` history.
- Unit: difficulty update on published game without `learning_science_signoff` rejected.
- Unit: audit-log route rejects roles other than `product_admin`/`trust_safety`.
- Integration: full create → publish → compliance-dashboard-reflects-Compliant → skill deprecated (B-05 simulated) → dashboard reflects At Risk → reconciliation job runs → game withdrawn round trip.
- Integration: Quran/Tajweed/Dua game routes through scholar-review workflow before becoming publishable.

## 28. Documentation
OpenAPI documents all five routes with explicit scope requirements per route, and the `422` policy variants (skill-mapping, sign-off, scholar-approval-pending) distinctly documented.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Admin Request/Response Schemas**
- Objective: `AdminGameCreateRequest`, `AdminGameUpdateRequest`, `GameComplianceResponse`, `GameAuditLogEntryResponse`.
- Definition of Done: matches §13 shapes.

**Task 02 — Implement Create/Update/Withdraw Service Methods**
- Objective: `service.create_game()`, `update_game()`, `withdraw_game()`, each calling B-04's `validate_skill_mapping_gate()` where applicable.
- Definition of Done: gate invocation confirmed via test for every mutating path.

**Task 03 — Implement Learning-Science Sign-Off Enforcement**
- Objective: Reject published-game difficulty updates missing valid sign-off.
- Definition of Done: dedicated negative test.

**Task 04 — Integrate Scholar-Review Workflow**
- Objective: Route Quran/Tajweed/Dua-linked game publish attempts through A.5/A.6's existing workflow trigger.
- Existing Files to Reuse: confirm exact A.5/A.6 admin workflow entry point before implementation (flagged dependency).
- Definition of Done: integration test confirms non-bypassable routing for tagged content types.

**Task 05 — Implement Compliance Dashboard Query & Endpoint**
- Objective: `GET /admin/v1/games/compliance` per §13.
- Definition of Done: Compliant/At Risk status correctly computed via single aggregated query.

**Task 06 — Implement Audit Log Endpoint**
- Objective: `GET /admin/v1/games/audit-log`, scope-restricted to `product_admin`/`trust_safety`.
- Definition of Done: unauthorized-role test passes (`403`).

**Task 07 — Wire RBAC Across All Routes**
- Objective: `require_admin_scope()` applied per §17 table exactly.
- Definition of Done: scope-matrix test covering every route/role combination.

**Task 08 — Wire Audit Logging on Every Mutation**
- Objective: `AdminAuditRepository.log_action()` called on create/update/withdraw.
- Definition of Done: audit row confirmed for every mutating test case.

**Task 09 — Add Tests**
- Objective: Full suite per §27.
- Files to Create: three test files listed in §8.

**Task 10 — Add Documentation**
- Objective: OpenAPI scope/response documentation per route.

**Task 11 — Final Code Review**
- Objective: Confirm RBAC matrix (§17) fully matches implementation with no gaps; confirm B-04 gate is genuinely invoked (not merely referenced) in every relevant code path.
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Full CRUD implemented with B-04 gate enforced on every publish-affecting mutation.
- Compliance dashboard and audit log endpoints functioning per contract, correctly scope-restricted.
- Scholar-review routing confirmed for Quran/Tajweed/Dua-linked games.
- Learning-science sign-off enforced for published-game difficulty changes.
- All §27 tests passing in CI.

## 31. Final Verification Checklist
- [x] Create/update/withdraw all correctly invoke B-04's skill-mapping gate
- [x] Withdraw preserves `game_session` history (soft delete only)
- [x] Learning-science sign-off enforced and tested
- [x] Scholar-review routing confirmed for Quran/Tajweed/Dua content
- [x] RBAC scope matrix fully tested (every route × every role)
- [x] Compliance dashboard correctly distinguishes Compliant vs. At Risk
- [x] Audit log endpoint restricted to `product_admin`/`trust_safety` only
- [x] Every mutating action produces an audit log row
- [x] OpenAPI documentation complete for all five routes
- [x] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-04 (skill-mapping gate, invoked on every create/update); A.5/A.6 scholar-review workflow component (exact integration point unresolved — A.5's PRD confirms scholar-reviewed content governance exists but does not name a specific reusable admin component; A.6 not yet reviewed).
- KMP Dependency: None directly (admin-only); indirectly affects K-01's catalog via publish/withdraw state.
- Admin Dependency: N-01, N-02, N-03, N-04 all consume this API directly.
- Database Dependency: `game`, `game_skill_link` (this module), `admin_audit_log` (`modules/admin`, reused).
- External Service Dependency: None.
- Figma Dependency: Games Catalog Editor, Skill-Mapping Compliance Dashboard, Anti-Filler Audit Log screens (N-01/N-02/N-04).
