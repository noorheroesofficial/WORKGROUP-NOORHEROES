# Blueprint: Admin AI Safety Event Taxonomy Management API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/ai_safety/` (admin sub-router) or `src/noorheroes/modules/admin/`, consuming `ai_safety`'s models. Delivers Admin CRUD for `ai_safety_event` category definitions and their pre-templated `summary_text` patterns, consumed by B-03's ingestion consumer.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-09 — Admin AI Safety Event Taxonomy Management API.

## 4. Objective
Provide `content_editor`/`trust_safety`-restricted CRUD for the category/template library that governs `ai_safety_event.summary_text` generation, enforcing a placeholder-only template constraint server-side so this admin surface can never become an indirect vector for exposing raw free-form user input.

## 5. Business Requirements
Source: PRD §8, §9, §12.5.
- CRUD for `ai_safety_event` category definitions and pre-templated `summary_text` patterns (e.g., `category="topic_blocked"` → template `"A question about {topic} was redirected to approved content"`).
- Each template field validated to contain only placeholder-style variables from an allowed list — no free-form text injection point — enforced server-side at save time.
- Restricted to `content_editor`/`trust_safety` roles.
- Every change writes an `audit_log` row.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.2 (`admin` context) and §5.3 (`ai_safety` context): this is a new admin-facing CRUD surface within the existing `ai_safety` bounded context, following the platform's established `AdminRouter`/`require_admin_scope()` pattern (`core/deps.py`).

## 7. Existing Code to Reuse
- `require_admin_scope(required_scope: str)` (`core/deps.py`) — reused for `content_editor`/`trust_safety` role restriction.
- `AdminSessionContext` (`core/deps.py`).
- The `admin` bounded context's `AuditLog` model (`src/noorheroes/modules/admin/`) — the platform's established audit-write mechanism, confirmed in use by A.7 B-09 ("Reuse the existing audit-log mechanism (`admin` context's `AuditLog` model) rather than creating a parallel one") and A.1 B-09 (`AdminService.log_action()` writing an `AdminAuditLog`/`AuditLog` row with admin_id, action, before/after diff, timestamp). This blueprint reuses that same model/write pattern, not a new one.
- `BaseRepository`/`BaseService` generics for standard CRUD scaffolding.

## 8. Files to Create
- `src/noorheroes/modules/ai_safety/admin_schemas.py` — `AiSafetyCategoryCreateRequest`, `AiSafetyCategoryUpdateRequest`, `AiSafetyCategoryResponse`
- `src/noorheroes/modules/ai_safety/admin_service.py` — `AiSafetyTaxonomyAdminService`
- `src/noorheroes/modules/ai_safety/admin_api.py` — admin CRUD routes
- `tests/modules/ai_safety/test_admin_ai_safety_taxonomy_api.py`
- `tests/modules/ai_safety/test_ai_safety_template_validation.py`

## 9. Files to Modify
- `src/noorheroes/modules/ai_safety/models.py` — add `AiSafetyCategoryDefinition` model (`category`, `summary_text_template`, `is_active`, `created_by`, `updated_at`)
- `alembic/versions/xxxx_create_ai_safety_category_definition.py`
- App-level admin router registration — mount `admin_api.py`'s router

## 10. Backend Requirements
- Routes (all under `content_editor`/`trust_safety` `require_admin_scope`):
  - `POST /v1/admin/ai-safety/categories` — create
  - `GET /v1/admin/ai-safety/categories` — list
  - `GET /v1/admin/ai-safety/categories/{category}` — retrieve
  - `PATCH /v1/admin/ai-safety/categories/{category}` — update
  - `POST /v1/admin/ai-safety/categories/{category}/disable` — disable/retire
- **Template validation (server-side, mandatory at save time):** `summary_text_template` must match a regex/parser that permits only `{allowed_placeholder}` tokens from a fixed allow-list (e.g., `{topic}`, `{category}`) — any other content is treated as literal safe text, but the validator must reject templates containing patterns resembling unescaped free-form injection points (e.g., no arbitrary `{}` beyond the allow-list, no raw HTML/script-like content).
- Every create/update/disable writes an `audit_log` row: `admin_id`, `action`, `category`, `before`/`after` diff, `timestamp`.
- Duplicate `category` creation rejected with `409 CONFLICT`.

## 11. KMP Requirements
N/A — this is an admin-only surface, not consumed by the KMP app directly (the KMP app only ever sees the categorical `category` value and resolved `summary_text` via B-03's read endpoint, never the template management surface itself).

## 12. NextJS Requirements
Consumed by N-01 (`AI Safety Event Taxonomy Management` admin page).

## 13. API Contract

**Admin API** — `POST /v1/admin/ai-safety/categories`
- **Auth:** Bearer, admin session, `content_editor` or `trust_safety` scope
- **Request:**
```json
{ "category": "topic_blocked", "summary_text_template": "A question about {topic} was redirected to approved content", "concerning_default": false }
```
- **Response 201:** `AiSafetyCategoryResponse` — `{ "category": "string", "summary_text_template": "string", "is_active": true, "created_by": "string", "updated_at": "ISO-8601" }`
- **Validation:** Template placeholder allow-list enforced; duplicate `category` rejected
- **Error Responses:** `409` duplicate category, `422` invalid template, `401` invalid admin session, `403` insufficient role scope

**Admin API** — `GET /v1/admin/ai-safety/categories`
- **Response 200:** `{ "items": [AiSafetyCategoryResponse, ...], "next_cursor": "string | null", "has_more": false }` — cursor-paginated, matching the Admin Portal's established list-response shape (`{ items, next_cursor, has_more }`, confirmed via C.20 B-06/N-01's content-safety audit log endpoint) rather than an unpaginated array, so N-01's `usePaginationState`/`DataTable` integration follows the same pattern as every other admin list page.

**Admin API** — `PATCH /v1/admin/ai-safety/categories/{category}`
- **Request:** partial `AiSafetyCategoryUpdateRequest`
- **Response 200:** updated `AiSafetyCategoryResponse`
- **Error Responses:** `404` unknown category, `422` invalid template

**Admin API** — `POST /v1/admin/ai-safety/categories/{category}/disable`
- **Response 200:** `{ "category": "string", "is_active": false }`

## 14. Database Requirements
`ai_safety_category_definition` table: `category` (PK, string enum-backed), `summary_text_template` (text, placeholder-constrained), `concerning_default` (boolean), `is_active` (boolean), `created_by` (FK admin), `created_at`, `updated_at`. Referenced by `ai_safety_event.category` (B-03) as the source-of-truth taxonomy.

## 15. Validation
- `category` required, unique, must match the platform's category-naming convention (lowercase snake_case).
- `summary_text_template` required, must pass the placeholder-allow-list validator.
- Role scope (`content_editor` or `trust_safety`) required for every mutating action.

## 16. Authentication
Bearer admin session (`AdminSessionContext`).

## 17. Authorization
`require_admin_scope("content_editor")` or `require_admin_scope("trust_safety")` — either scope permitted for full CRUD per PRD §8.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate category on create | `409 CONFLICT` |
| Invalid template (disallowed placeholder/injection-shaped content) | `422` with a specific validation-error message |
| Unauthorized admin request | `401` |
| Forbidden (wrong role scope) | `403` |
| Unknown category on update/disable | `404` |

## 19. Offline First
N/A (admin web surface, always-online).

## 20. Local Data
N/A.

## 21. Localization
`summary_text_template` may itself need per-locale variants (English/Hindi/Arabic/Urdu) — confirm with product/localization team whether this table needs a `locale` column or whether localization is resolved by a separate `modules/localization/` lookup keyed by `category`; do not invent a schema for this without confirming the platform's existing localization-key convention (project instruction #30).

## 22. RTL
N/A (backend; template content for RTL locales must render correctly when consumed downstream by B-03/K-03 — verified there, not here).

## 23. Analytics
N/A (admin CRUD action, not a user-facing analytics event).

## 24. Performance
Low-traffic admin CRUD surface; no special performance requirements beyond standard indexed lookups.

## 25. Security
The placeholder-only template validation is this endpoint's primary security control — it prevents `summary_text_template` from ever becoming an indirect vector through which raw/arbitrary text could later flow into the structurally-redacted `ai_safety_event.summary_text` field (B-03), which is otherwise guaranteed to be free-form-text-injection-safe by that table's own schema constraints.

## 26. Library Requirements
No new dependencies; standard regex/parser for placeholder validation.

## 27. Testing
1. Unit test: create category with a valid template succeeds.
2. Unit test: create category with a duplicate name returns `409`.
3. **Template validation test:** template containing a disallowed placeholder or injection-shaped content is rejected with `422`.
4. Unit test: update category template revalidates the new template.
5. Unit test: disable category sets `is_active: false`, does not delete the row.
6. Unit test: unauthorized/forbidden requests rejected for non-`content_editor`/`trust_safety` roles.
7. Unit test: every mutating action writes an `audit_log` row with correct before/after diff.
8. Integration test: full CRUD lifecycle through the admin gate.

## 28. Documentation
OpenAPI docstrings per route; admin module README documenting the placeholder allow-list and its rationale (defense against indirect free-form-text injection into the AI Safety Event Store).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create AiSafetyCategoryDefinition Model and Migration**
- Task ID: B09-T01
- Objective: Persist the taxonomy/template library.
- Why This Is Required: Source-of-truth for B-03's ingestion consumer and N-01's admin UI.
- Existing Architecture to Follow: SQLAlchemy 2.0 model conventions.
- Existing Files to Reuse: `ai_safety/models.py` (extend).
- Files to Create: migration file.
- Files to Modify: `models.py`.
- Implementation Details: Columns per §14.
- Business Rules: PRD §8.
- Validation: N/A (schema-level).
- Error Handling: N/A.
- Security: N/A.
- Performance: Indexed PK on `category`.
- Localization: Flag open question per §21 for follow-up.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Table docstring.
- Dependencies: none.
- Do Not Change: `ai_safety_event` table (B-03).
- Expected Result: Table exists, migration applies.
- Definition of Done: Model importable, migration clean.

**Task 02 — Implement Placeholder Template Validator**
- Task ID: B09-T02
- Objective: Server-side validation rejecting non-allow-listed placeholder/injection-shaped templates.
- Why This Is Required: This is the endpoint's primary security control.
- Existing Architecture to Follow: Pydantic validator pattern.
- Existing Files to Reuse: none new.
- Files to Create: none (inline in `admin_schemas.py` or a small `template_validation.py` util).
- Files to Modify: `admin_schemas.py`.
- Implementation Details: Regex/parser enforcing the fixed placeholder allow-list.
- Business Rules: PRD §8, §9.
- Validation: This task IS the validation.
- Error Handling: `422` with specific message.
- Security: Primary control for this endpoint.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04 (dedicated template-validation test file).
- Documentation: Docstring explaining the allow-list rationale.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Invalid templates rejected before persistence.
- Definition of Done: Task 04's template-validation tests pass.

**Task 03 — Implement AiSafetyTaxonomyAdminService and Routes**
- Task ID: B09-T03
- Objective: Full CRUD with RBAC and audit logging.
- Why This Is Required: Delivers the admin contract.
- Existing Architecture to Follow: `require_admin_scope()`; `admin` context's `AuditLog` model / `AdminService.log_action()` write pattern.
- Existing Files to Reuse: `core/deps.py`, `modules/admin/`'s `AuditLog` model.
- Files to Create: `admin_service.py`, `admin_api.py`.
- Files to Modify: App-level admin router registration.
- Implementation Details: Per §10.
- Business Rules: PRD §8.
- Validation: Task 02's validator applied at create/update.
- Error Handling: Per §18.
- Security: RBAC enforcement, audit logging.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summaries.
- Dependencies: Tasks 01–02.
- Do Not Change: Existing admin router mounting pattern.
- Expected Result: Full CRUD live and RBAC-restricted.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Test Suite**
- Task ID: B09-T04
- Objective: Cover §27.
- Why This Is Required: QA coverage including the security-critical template validator.
- Existing Architecture to Follow: pytest + admin fixture factories.
- Existing Files to Reuse: Admin session/role fixtures.
- Files to Create: `test_admin_ai_safety_taxonomy_api.py`, `test_ai_safety_template_validation.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: Template validation and RBAC tests are critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Admin CRUD for `ai_safety_event` categories/templates live, restricted to `content_editor`/`trust_safety`, placeholder-only template validation enforced server-side, every change audit-logged, all tests green.

## 31. Final Verification Checklist
- [ ] Placeholder-only template validation verified (rejects non-allow-listed/injection-shaped content)
- [ ] RBAC restricted to `content_editor`/`trust_safety`
- [ ] Every mutating action writes an `audit_log` row
- [ ] Duplicate category rejected with `409`
- [ ] Disable does not delete the row (soft-disable only)
- [ ] Localization schema question flagged for follow-up, not silently invented
- [ ] OpenAPI docs reflect the full CRUD contract
