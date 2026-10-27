# B-09 — Admin Skill Domain Registry API

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Gives Admin the CRUD surface for the `skill_domain` registry table introduced in B-01 — the prerequisite for FR-9's "add a domain via data alone" promise.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-09 — Admin Skill Domain Registry API (Admin API)

## 4. Objective
Implement full CRUD endpoints over `skill_domain` (`domain_key`, `display_name`, `active`), gated behind the `product_admin` role, feeding N-01's Admin UI and, indirectly, A.5's Curriculum Builder domain-selector dropdown.

## 5. Business Requirements
- Admin Requirements (A.9 PRD §8): "Skill Domain Registry: Admin CRUD for registering new learning domains — the prerequisite for FR-9's zero-new-code domain extensibility."
- CRUD permissions: full CRUD behind `product_admin` role.
- Acceptance Criterion: a new domain configured by Admin inherits state-machine evaluation, mastery scoring, and spaced-repetition scheduling automatically.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. `admin` bounded context handles RBAC/role-gating conventions; `learning` context owns the `skill_domain` model (from B-01). This endpoint lives in the `admin` context's router layer but delegates to `learning`'s `SkillDomainService`, consistent with how other admin-facing CRUD over domain-owned tables is structured elsewhere in the platform (mirror whichever existing admin-context pattern wraps a domain-context service — e.g., A.5's `09-admin-quran-skill-tree-curriculum-management-api.md` for precedent).

## 7. Existing Code to Reuse
- B-01's `SkillDomainService`/`SkillDomainRepository` — this endpoint is a thin admin-authorized wrapper, not a parallel data-access layer.
- Existing `admin` context RBAC dependency (`require_role("product_admin")` or equivalent).
- Existing audit-log write pattern used by other admin mutating endpoints.

## 8. Files to Create
- `src/noorheroes/modules/admin/schemas/skill_domain_admin.py` — `SkillDomainCreateRequest`, `SkillDomainUpdateRequest`, `SkillDomainResponse`.
- `tests/modules/admin/test_skill_domain_registry_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` (or the `learning` context's admin sub-router, whichever existing convention applies) — add `GET/POST/PUT /admin/v1/mastery/domains[/{domain_key}]` routes.

## 10. Backend Requirements
- **`GET /admin/v1/mastery/domains`** — list all domains (active + inactive, admin sees everything).
- **`POST /admin/v1/mastery/domains`** — create a new domain (`domain_key`, `display_name`, `active` default true).
- **`PUT /admin/v1/mastery/domains/{domain_key}`** — update `display_name`/`active`; `domain_key` itself immutable after creation (documented, not silently rejected without explanation).
- **Cache invalidation:** any mutating call invokes B-01's `SkillDomainService.invalidate_domain_cache()` so the change is immediately visible to B-05/B-07/B-08's cached reads.
- **Deactivation guard:** attempting to set `active=false` on a domain with existing `skill_node` rows returns a confirmation-required response (or requires an explicit `force=true` flag) rather than silently orphaning content — consistent with rule against harmful unreviewed changes.

## 11. KMP Requirements
N/A directly (admin-only surface).

## 12. NextJS Requirements
Directly backs N-01 (Skill Domain Registry Management); also the data source A.5's existing Curriculum Builder domain-selector dropdown must be updated to read from (`GET /admin/v1/mastery/domains`) instead of its current hardcoded enum.

## 13. API Contract

**`GET /admin/v1/mastery/domains`**
- **Auth:** Bearer (admin session), role `product_admin` (read may be broader — confirm whether `curriculum_editor` also needs read access for the dropdown use case; if so, this endpoint's GET should accept both roles while POST/PUT remain `product_admin`-only)
- **Response 200:** `[{ "domain_key": "quran", "display_name": "Quran", "active": true }]`

**`POST /admin/v1/mastery/domains`**
- **Auth:** `product_admin`
- **Request:** `{ "domain_key": "islamic_facts", "display_name": "Islamic Facts", "active": true }`
- **Response 201:** created domain object.
- **Error Responses:** `409` (duplicate `domain_key`), `422` (invalid format), `401`/`403`.

**`PUT /admin/v1/mastery/domains/{domain_key}`**
- **Auth:** `product_admin`
- **Request:** `{ "display_name": "...", "active": true|false }`
- **Response 200:** updated domain object.
- **Error Responses:** `404` (unknown domain_key), `409` (deactivation with existing content, if not forced), `401`/`403`.

## 14. Database Requirements
No schema changes beyond B-01's `skill_domain` table.

## 15. Validation
- `domain_key` format: lowercase snake_case, unique, immutable post-creation.
- `display_name` non-empty.
- Deactivation guard per §10.

## 16. Authentication
Bearer JWT, admin-session scope.

## 17. Authorization
`product_admin` role required for all mutating operations; read access role scope confirmed per §13 note.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `domain_key` on create | `409` |
| Unknown `domain_key` on update | `404` |
| Unauthorized/forbidden admin request | `401`/`403` |
| Deactivating a domain with active `skill_node` rows, no `force` flag | `409` with a clear message, not a silent no-op or silent orphaning |

## 19. Offline First
N/A (admin web endpoint).

## 20. Local Data
N/A.

## 21. Localization
`display_name` should support localized variants if the platform's Admin content model requires multi-language display names (consistent with §21 of B-01); if the existing admin content model is English-only for internal-facing labels, document that as the deliberate scope here.

## 22. RTL
N/A (backend; Admin UI RTL owned by N-01).

## 23. Analytics
No child-facing analytics; standard admin audit-log entry per mutating action.

## 24. Performance
Low-traffic admin endpoint; no special performance requirements beyond standard API latency norms.

## 25. Security
`product_admin`-only mutation prevents unauthorized domain registration (a governance-relevant action since it gates FR-9's extensibility promise). Every mutating action writes an immutable audit-log row (rule 22 of the top-level system instructions: mutating admin actions require audit logging).

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: CRUD operations, duplicate-key rejection, deactivation-guard logic.
- Integration: full create → read → update → deactivate-with-guard flow.
- RBAC test: non-`product_admin` roles rejected on mutating endpoints.

## 28. Documentation
OpenAPI schema; note that `GET /admin/v1/mastery/domains` is the required data source for A.5's Curriculum Builder dropdown (cross-reference for whoever implements N-01/updates the Curriculum Builder).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Admin CRUD Router for skill_domain**
- Task ID: B-09-T01
- Objective: Full CRUD wrapper over B-01's `SkillDomainService`.
- Why This Is Required: Prerequisite for N-01 and for the Curriculum Builder dropdown migration off its hardcoded enum.
- Existing Architecture to Follow: Existing `admin` context RBAC/router conventions.
- Existing Files to Reuse: `SkillDomainService`, `require_role` dependency, audit-log write helper.
- Files to Create: `schemas/skill_domain_admin.py`.
- Files to Modify: `admin/api.py` (or equivalent admin sub-router location).
- Implementation Details: Standard REST CRUD; invalidate B-01's cache on every mutation; deactivation guard per §10.
- Business Rules: `domain_key` immutable after creation; deactivation guard.
- Validation: Per §15. Error Handling: Per §18.
- Security: `product_admin` role enforced; audit log on every mutation.
- Performance: N/A (low traffic).
- Localization: Per §21 decision. RTL: N/A. Analytics: Audit log entry.
- Tests: `test_skill_domain_registry_api.py`.
- Documentation: OpenAPI schema.
- Dependencies: B-01.
- Do Not Change: B-01's `SkillDomainService` internals (call it, don't fork it).
- Expected Result: Working admin CRUD API.
- Definition of Done: Full CRUD + RBAC + deactivation-guard tests green.

## 30. Definition of Done
Admin CRUD for `skill_domain` live, `product_admin`-gated, audit-logged, cache-invalidating on mutation, ready to back N-01 and the A.5 Curriculum Builder dropdown migration.

## 31. Final Verification Checklist
- [x] Full CRUD working (create/read/update; delete intentionally unsupported — deactivate instead, consistent with soft-delete-only rule)
- [x] `product_admin` RBAC enforced on mutations (with read access extended to `curriculum_editor` for dropdowns)
- [x] Deactivation guard prevents silent orphaning of active `skill_node` rows (HTTP 409 unless `force=true`)
- [x] Cache invalidation confirmed on every mutation (`SkillDomainService.invalidate_domain_cache`)
- [x] Audit log entry written on every mutation (`AdminAuditRecord` with before/after state diffs)
- [x] `domain_key` immutability enforced (HTTP 422 on modification attempt)

## 32. Verification Evidence & Test Results
- **Dedicated B-09 Suite (`tests/modules/admin/test_skill_domain_registry_api.py`)**: 26 passed in 0.78s (100% green).
  - Listing & Retrieval: 4 passed in 0.12s (canonical and direct dual-mounts, `product_admin`, `curriculum_editor`, `super_admin`, 403 on `content_editor`).
  - Creation & Validation: 8 passed in 0.20s (`product_admin` 201 Created, camelCase and snake_case dual-wire acceptance, duplicate 409 Conflict, format 422, blank name 422, non-product admin 403, cache purge, audit log).
  - Updating & Safety Guards: 8 passed in 0.22s (valid update 200, 404 on missing, immutable domain_key 422, deactivation guard 409 when nodes exist without force, force=True deactivation 200, 403 on non-product admin, cache purge, audit log).
  - Soft-Delete Prohibition: 2 passed in 0.08s (DELETE returns HTTP 405 Method Not Allowed on both `/v1/admin/mastery/domains/{key}` and `/admin/v1/mastery/domains/{key}`).
  - Submodule Import Resolution: 2 passed in 0.06s (validates imports from `src.noorheroes.modules.admin.schemas.skill_domain_admin` per §8 and `src.noorheroes.modules.admin.schemas`).
  - SQLite Async Integration: 2 passed in 0.10s (multi-table transactions in memory testing persistence, node counting, deactivation blocking, force override, and audit logging).
- **Core Exceptions Suite (`tests/core/test_exceptions.py`)**: 24 passed in 0.30s (100% green, unit tests covering `SkillDomainAdminNotFoundError`, `DuplicateSkillDomainError`, and `SkillDomainDeactivationBlockedError`).
- **Full Admin Bounded Context Suite (`tests/modules/admin/`)**: 344 passed in 10.82s across all 22 test files (100% green, zero regressions).
- **Full Feature A.9 Learning & Admin Fleet**: 292 passed in 3.65s (100% green, zero behavioral regressions across B-01 through B-09).
- **Dual-Wire Wire Serialization & OpenAPI Contract**: Pydantic v2 schemas (`SkillDomainCreateRequest`, `SkillDomainUpdateRequest`, `SkillDomainResponse`) enforce `extra="forbid"`, `populate_by_name=True`, and dual-wire camelCase/snake_case aliasing via `NoorHeroesBaseModel`.
- **Database & Architecture Integrity**: Reuses existing `skill_domain` table from B-01 without schema modifications. Clean Architecture zero-commit repository pattern maintained.
