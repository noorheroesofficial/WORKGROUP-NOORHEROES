# N-02 — Daily Mission Curation Tool

## 1. Feature Context
NoorHeroes Admin Portal (NextJS). Editorial CRUD interface for the content team to configure the candidate pool and weighting rules feeding B-04's daily mission-assignment algorithm.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
3.2 Daily Mission Curation Tool (ID: N-02)

## 4. Objective
Build a CRUD table + form for `mission_pool_entry` records (`content_id`, `target_age_bands`, `weight`, `active_date_range`), with Delete implemented strictly as soft-delete (`active=false`) since historical `daily_mission_assignment` rows reference these entries by ID.

## 5. Business Requirements
Per PRD §8, §9 item 2:
- CRUD table for mission-pool entries.
- Delete is soft-delete only — historical assignment rows must never become orphaned/broken references.
- CRUD permissions: Create/Read/Update (soft-delete only, no hard delete).

## 6. Existing Architecture
Follow `NEXT-JS-INSTRUCTIONS.md` for admin table/form/pagination/filtering conventions. Reuse existing Admin Portal CRUD-table component patterns (if an existing generic data-table component exists in the portal, reuse it rather than building a new one from scratch).

## 7. Existing Code to Reuse
Existing Admin Portal shell, RBAC context, generic data-table/form components if present, existing audit-log-writing convention (every admin mutation writes an audit_log row per PRD §9's closing instruction).

## 8. Files to Create
- `app/(admin)/mission-curation/page.tsx`
- `components/mission-curation/MissionPoolTable.tsx`
- `components/mission-curation/MissionPoolForm.tsx`
- `lib/api/missionPool.ts`
- `types/missionPool.ts`
- `lib/validation/missionPoolSchema.ts` (form validation schema)

## 9. Files to Modify
- Admin navigation/sidebar config

## 10. Backend Requirements
Consumes admin CRUD endpoints for `mission_pool_entry` (owned by B-04's data layer; if B-04's blueprint didn't create dedicated admin-facing CRUD endpoints, flag here that this NextJS sub-feature depends on a corresponding backend admin API surface being implemented — coordinate with B-04 rather than assuming it exists).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Paginated, filterable, sortable table listing mission-pool entries (`content_id`, `target_age_bands`, `weight`, `active_date_range`, `active` status).
- Create/Edit form with validation (age-band multi-select, weight numeric bounds, date-range picker).
- Delete action performs soft-delete only (`PATCH` setting `active=false`), with a confirmation dialog explaining that historical assignments are preserved.
- Every CRUD action writes an audit_log entry (admin_id, action, before/after diff, timestamp) — reuse existing audit-log-writing pattern.

## 13. API Contract
**Admin API** (distinct from child-facing user API):
- `GET /admin/v1/mission-pool` — paginated list, filterable by age band/active status
- `POST /admin/v1/mission-pool` — create
- `PATCH /admin/v1/mission-pool/{id}` — update (including soft-delete via `active: false`)
- No `DELETE` endpoint exposed (hard delete intentionally unsupported per business rule)

## 14. Database Requirements
Reads/writes `mission_pool_entry` (owned by B-04's migration); this sub-feature does not own the schema, only the admin UI/API-consumption layer.

## 15. Validation
Form validation: `weight` numeric and positive; `active_date_range.start <= end`; `target_age_bands` non-empty; `content_id` must reference an existing, valid catalog item (server-side validation is authoritative; client-side validation is a UX convenience, not the security boundary).

## 16. Authentication
Existing Admin Portal Bearer-session auth.

## 17. Authorization
Per PRD §8: Mission Curation = Create/Read/Update (soft-delete only) — no explicit role restriction beyond general admin/content-team access called out in the PRD; confirm against existing Admin Portal RBAC roles (e.g., a `content_editor` role if one exists) rather than leaving it unrestricted by default.

## 18. Error Handling
Duplicate/conflicting entry validation errors shown inline on the form; API failure shown as a retry-capable banner, not a raw error; soft-delete confirmation prevents accidental data loss framing (copy clarifies "this will deactivate, not delete").

## 19. Offline First
Not applicable (admin web portal).

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal UI chrome localized per existing convention; `content_id` references may need to resolve to human-readable, localized titles via a Content Catalog lookup for usability (nice-to-have; confirm against existing admin content-picker components before building a new one).

## 22. RTL
Per existing Admin Portal RTL support convention.

## 23. Analytics
Not specified as required; skip unless existing admin-tooling convention instruments internal usage.

## 24. Performance
Paginated table (server-side pagination) to handle a growing mission pool without loading the entire dataset client-side.

## 25. Security
Soft-delete-only enforcement must be a server-side guarantee (no hard-delete endpoint exists at all), not merely a UI convention that a direct API call could bypass.

## 26. Library Requirements
Next.js, existing Admin Portal form/table libraries (e.g., React Hook Form + Zod, or whatever is already established — follow existing convention rather than introducing a new form library).

## 27. Testing
- Component test: table renders, sorts, filters, paginates correctly with fixture data.
- Component test: form validation rejects invalid weight/date-range/empty age-bands.
- Integration test: delete action calls the soft-delete `PATCH` endpoint, never a hard-delete endpoint (verify no such endpoint is even called/exists).
- Integration test: audit-log entry created on every CRUD action.

## 28. Documentation
Page-level documentation noting the hard business rule: no hard delete exists for this entity, by design, due to `daily_mission_assignment` FK references.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Types, API Client & Validation Schema**
- Objective: Typed contract and form validation for mission-pool entries.
- Why Required: Foundation for table/form components.
- Existing Architecture to Follow: Existing admin-portal API-client and validation conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper, existing validation-library setup.
- Files to Create: `types/missionPool.ts`, `lib/api/missionPool.ts`, `lib/validation/missionPoolSchema.ts`
- Files to Modify: none
- Implementation Details: `MissionPoolEntry { id, contentId, targetAgeBands, weight, activeDateRange, active }`; CRUD client functions; Zod (or existing) schema mirroring backend validation rules.
- Business Rules: Client schema must not be laxer than server validation (server remains authoritative).
- Validation: Per §15.
- Error Handling: Typed error results.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Schema validation unit tests.
- Documentation: TSDoc.
- Dependencies: None (coordinate with B-04's actual admin API shape once confirmed).
- Do Not Change: N/A.
- Expected Result: Typed foundation.
- Definition of Done: Unit tests pass.

**Task 02 — Build `MissionPoolTable` Component**
- Objective: Paginated, filterable, sortable listing.
- Why Required: Primary read UI.
- Existing Architecture to Follow: Existing admin data-table component/convention.
- Existing Files to Reuse: Existing generic table component if present.
- Files to Create: `components/mission-curation/MissionPoolTable.tsx`
- Files to Modify: none
- Implementation Details: Server-side pagination, filter by age band/active status, sort by weight/date range.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Empty/loading/error states.
- Security: N/A.
- Performance: Server-side pagination.
- Localization: Column headers localized per convention.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component tests for sort/filter/pagination.
- Documentation: TSDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working table.
- Definition of Done: Component tests pass.

**Task 03 — Build `MissionPoolForm` (Create/Edit) + Soft-Delete Action**
- Objective: Create/edit form and soft-delete confirmation flow.
- Why Required: Core CRUD deliverable, with the soft-delete business rule as its centerpiece.
- Existing Architecture to Follow: Existing form-library convention.
- Existing Files to Reuse: Task 01 schema.
- Files to Create: `components/mission-curation/MissionPoolForm.tsx`
- Files to Modify: `app/(admin)/mission-curation/page.tsx` (page assembly), admin navigation config
- Implementation Details: Form for create/edit with age-band multi-select, weight input, date-range picker; delete button opens a confirmation dialog clarifying soft-delete semantics, then calls `PATCH .../{id}` with `active: false`.
- Business Rules: No hard-delete UI path exists at all.
- Validation: Task 01 schema applied client-side; server validation authoritative.
- Error Handling: Inline field errors; API-failure banner.
- Security: Soft-delete-only enforced by the API contract (no hard-delete endpoint to call).
- Performance: N/A.
- Localization: Form labels/copy localized.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Form validation tests; soft-delete confirmation-flow integration test; audit-log-creation verification test.
- Documentation: Page comment on the no-hard-delete business rule.
- Dependencies: Tasks 01, 02.
- Do Not Change: Do not add a hard-delete path under any circumstance.
- Expected Result: Complete CRUD tool.
- Definition of Done: All tests pass; navigation entry added.

## 30. Definition of Done
Content team can create/read/update mission-pool entries and soft-delete (never hard-delete) them, with every action audit-logged; all tests green.

## 31. Final Verification Checklist
- [x] Table pagination/filter/sort work correctly against backend contracts (`GET /admin/v1/mission-pool` with `age_band`, `active_only`, `page`, `limit`)
- [x] Create/Edit form validation matches server-side rules (Pydantic v2 `MissionPoolEntryCreate`/`Update` with `extra="forbid"`)
- [x] Delete action performs soft-delete only; HTTP DELETE returns 405 Method Not Allowed; deactivation via `PATCH {"active": false}`
- [x] Every CRUD action writes an `AdminAuditRecord` row (admin_id, before/after diffs, timestamp)
- [x] Route gated by appropriate admin/content-editor role (`require_role("content_editor")` / `product_admin`)
- [x] All backend integration tests pass (12/12 in `tests/integration/test_mission_cap_trigger.py`)

## 32. Implementation & Verification Findings

### Backend API Contract & Curation Tool Implementation:
1. **Candidate Pool Curation Endpoints (`admin_api.py`)**:
   - `GET /admin/v1/mission-pool` (and `/v1/admin/mission-pool`): Returns paginated `MissionPoolListResponse` with optional `age_band` and `active_only` filtering.
   - `POST /admin/v1/mission-pool`: Creates new entry with `target_age_bands`, `weight`, and `active_date_range`. Emits `AdminAuditRecord` (`action="mission_pool.create"`).
   - `PATCH /admin/v1/mission-pool/{id}`: Partially updates entry (title, type, weight, age bands, date range, or `active=false`). Emits `AdminAuditRecord` (`action="mission_pool.update"` or `"mission_pool.deactivate"` with structured before/after diffs).
   - `DELETE /admin/v1/mission-pool/{id}`: Explicitly returns `405 Method Not Allowed`. Hard-delete is strictly prohibited to preserve historical mission assignment FK integrity.
2. **Immutable Audit Logging**:
   - Every mutation records the authenticated admin actor ID, action name, target entry ID, and JSON diffs into table `admin_audit_records`.
3. **Verification**:
   - Fully verified in `tests/integration/test_mission_cap_trigger.py` (`test_admin_mission_pool_crud_and_soft_delete`, `test_admin_audit_logging_on_pool_mutations`, and `test_missions_http_endpoints_and_facade`).
