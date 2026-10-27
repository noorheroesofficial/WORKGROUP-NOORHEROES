# B-06 — Admin Fact Editorial & Scholar-Approval Workflow API

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). This is the Admin API counterpart to B-01's data model — CRUD for facts/versions, the scholar-review queue, and the hard, server-enforced Disputed-Topic AI-assist disable. Architecturally isolated from the child-facing User APIs (B-02/B-03/B-04).

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.6 Admin Fact Editorial & Scholar-Approval Workflow API (ID: B-06) — **Admin API**

## 4. Objective
Implement full CRUD for facts/versions, an approve/reject/revoke scholar-review workflow, and a server-side-enforced Disputed-Topic Flag that hard-disables AI-assist drafting for facts under a flagged topic — enforced at the endpoint itself, never merely a UI-hideable control.

## 5. Business Requirements
- §8 Admin Requirements: Fact Editor (full CRUD, delete=withdraw, behind `content_editor`), Disputed-Topic Flag (update-only behind `trust_safety`/`scholar_lead`), Scholar Approval Workflow (approve/reject/revoke behind `scholar_reviewer`), Seasonal Topic Tagging (part of Fact Editor form, `content_editor`).
- FR-3: disputed/jurisprudentially-sensitive topics stay out of child-facing AI-auto-generation — a hard, zero-exception rule.
- Edge Case 8: admin attempts to mark a fact approved without an actual scholar-review record → rejected by validation.
- §12.5 Admin Security: Disputed-Topic AI-assist disable enforced server-side at the AI-assist endpoint itself, not merely a hideable UI button.

**Cross-reference:** the ongoing production monitoring for this endpoint's enforcement (periodic integrity audit, bypass-sampling canary) is implemented separately in B-09, not duplicated here — this blueprint owns the one-time enforcement mechanism and its CI-blocking test; B-09 owns its continuous production verification.

## 6. Existing Architecture
Extends `content` bounded context's admin surface, reusing the scholar-review queue pattern already established across A.3/A.5/A.6's admin APIs — confirm the exact existing endpoint/service shape for that shared review-queue pattern before writing a new one (Rule 30).

## 7. Existing Code to Reuse
- A.3/A.5/A.6's existing scholar-review queue service/endpoints (reuse the pattern, extend to cover `fact_version` rows — do not build a parallel review-queue mechanism).
- B-01: `FactRepository`, `FactVersionRepository`, `ScholarApprovalRepository`.
- `core/deps.py` → `get_current_admin`, `require_admin_scope()`.
- Existing `audit_log` infrastructure (used by A.3/A.5/A.6 admin mutations) — reuse for every mutating action here.
- Existing Topic Registry model/endpoints (for the Disputed-Topic Flag, if a Topic Registry already exists as a standalone entity — confirm before assuming).

## 8. Files to Create
- `src/noorheroes/modules/content/api/admin_facts_router.py` — full CRUD + approval workflow endpoints.
- `src/noorheroes/modules/content/services/admin_fact_service.py` — `AdminFactService(BaseService)`.
- `src/noorheroes/modules/content/models/topic_registry.py` — `TopicOrm` with `is_jurisprudentially_sensitive` flag (if a Topic Registry doesn't already exist elsewhere).
- `tests/modules/content/test_admin_fact_crud.py`.
- `tests/modules/content/test_disputed_topic_ai_assist_bypass.py`.
- `tests/modules/content/test_scholar_approval_workflow.py`.

## 9. Files to Modify
- `src/noorheroes/api/router.py` — register `admin_facts_router`.
- Existing AI-assist endpoint (wherever the CMS's AI-drafting-assist tool lives, if one exists) — add the disputed-topic check as a hard gate.

## 10. Backend Requirements
- `POST /v1/admin/facts` — create fact + initial draft version. Role: `content_editor`.
- `PUT /v1/admin/facts/{id}/versions` — create a new version from an edit (never mutates a published version in place). Role: `content_editor`.
- `GET /v1/admin/facts` — list/search/filter by topic, locale, age-band, status, paginated. Role: `content_editor`.
- `DELETE /v1/admin/facts/{id}` — soft-delete (`is_withdrawn = true`). Role: `content_editor`.
- `POST /v1/admin/facts/versions/{version_id}/approve` — Role: `scholar_reviewer`. Rejects (422) if no genuine scholar-review record context is attached (Edge Case 8 tooling-bypass prevention).
- `POST /v1/admin/facts/versions/{version_id}/reject` — Role: `scholar_reviewer`.
- `POST /v1/admin/facts/versions/{version_id}/revoke` — Role: `scholar_reviewer`, required `reason` field, sets `revoked_at`.
- `PATCH /v1/admin/topics/{id}/disputed-flag` — Role: `trust_safety` or `scholar_lead` (deliberately a higher bar than `content_editor`).
- AI-assist endpoint (existing CMS tool, if present) — add server-side check: `if topic.is_jurisprudentially_sensitive: raise ForbiddenError` — checked at the endpoint itself, independent of any UI state.
- Every mutating action writes an immutable `audit_log` row; Disputed-Topic changes and Approval Revocations flagged `high_sensitivity=true`.

## 11. KMP Requirements
N/A — admin-only.

## 12. NextJS Requirements
Consumed by N-01 (Fact Editor), N-02 (Disputed-Topic Flag), N-03 (Scholar Approval Workflow), N-04 (Seasonal Topic Tagging).

## 13. API Contract
**Endpoint:** `POST /v1/admin/facts/versions/{version_id}/approve`
**Auth:** Bearer, admin (`scholar_reviewer` scope)
**Request:** `{ "reviewer_notes": "..." }`
**Response 200:** `{ "version_id": "...", "status": "published", "scholar_approval": {...} }`
**Error Responses:** `403` (wrong role), `422` (no valid review context — Edge Case 8), `404` (unknown version).

**Endpoint:** `PATCH /v1/admin/topics/{id}/disputed-flag`
**Auth:** Bearer, admin (`trust_safety` or `scholar_lead` scope)
**Request:** `{ "is_jurisprudentially_sensitive": true }`
**Response 200:** `{ "topic_id": "...", "is_jurisprudentially_sensitive": true }`
**Error Responses:** `403` (wrong role — including a `content_editor` attempting this, which must be rejected).

## 14. Database Requirements
Writes: `fact`, `fact_version`, `scholar_approval` (B-01 tables), new `topic` table (or extends existing Topic Registry) with `is_jurisprudentially_sensitive boolean default false`, `audit_log` (existing table, new rows).

## 15. Validation
- Approval endpoint rejects a request lacking a genuine review record/context (Edge Case 8) — validated server-side, not merely a required-field check on the client form.
- Disputed-flag PATCH validated as boolean; role-gated independently of the general `content_editor` CRUD role.

## 16. Authentication
`Depends(get_current_admin)` on all endpoints.

## 17. Authorization
Role matrix per §5/§10: `content_editor` (CRUD, seasonal tagging), `scholar_reviewer` (approve/reject/revoke), `trust_safety`/`scholar_lead` (disputed-topic flag) — each endpoint checks its specific required scope via `require_admin_scope()`, not a single generic "admin" check.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Approve without valid review record | `422`, rejected (Edge Case 8) |
| Wrong role attempts an action | `403` |
| AI-assist called directly for a disputed-topic fact (UI bypass attempt) | `403`, rejected server-side |
| Unknown fact/version id | `404` |
| Revoke without a reason | `422` |

## 19. Offline First
N/A — admin web context.

## 20. Local Data
N/A.

## 21. Localization
Fact CRUD accepts per-locale text variants (English, Hindi, Arabic, Urdu) as part of the version payload.

## 22. RTL
N/A at API layer — client (N-01) handles RTL rendering of Arabic/Urdu text fields.

## 23. Analytics
None emitted by this API directly; `fact_scholar_approval_revoked_excluded` internal signal originates from B-02's selection service reacting to a revocation performed here, not from this endpoint itself.

## 24. Security
- Disputed-Topic AI-assist disable is this sub-feature's defining security control: enforced at the AI-assist endpoint itself so a determined editor cannot bypass it via direct API access even if the UI button is hidden.
- Revocation and disputed-topic changes are audit-logged as `high_sensitivity`, supporting the PRD's monitoring/alerting requirement (§10) for production sampling canaries.
- Role separation ensures a `content_editor` cannot self-approve their own authored content (approve requires `scholar_reviewer`) or toggle disputed-topic status (requires `trust_safety`/`scholar_lead`).

## 25. Compliance
Voluntary content-governance commitment held to engineering-enforced rigor per PRD §12.8 — no additional regulatory surface beyond platform baseline.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, existing RBAC scope-checking utilities — no new libraries.

## 27. Testing
- Unit: approve without valid review record → `422`.
- Unit: wrong-role attempts on every role-gated endpoint → `403`.
- **Security test:** direct API call to AI-assist endpoint for a disputed-topic-flagged fact, bypassing the admin UI entirely → `403`, verifying server-side (not just UI) enforcement.
- Integration: full create → edit (new version) → approve → publish → revoke lifecycle via the admin API.
- Integration: audit_log row written and correctly flagged `high_sensitivity` for revocation and disputed-topic-flag changes.

## 28. Documentation
OpenAPI docstrings for all endpoints; explicit documentation of the role matrix and the Edge Case 8 / disputed-topic bypass-prevention rationale.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Topic Registry / Disputed-Flag Model**
Objective: Confirm whether a Topic Registry already exists platform-wide; extend it with `is_jurisprudentially_sensitive`, or create one if genuinely absent.
Why Required: FR-3's enforcement point requires a queryable topic-level flag.
Dependencies: None (research + model task).
Expected Result: `topic.is_jurisprudentially_sensitive` column/table confirmed or created.
Definition of Done: No duplicate Topic Registry created if one already exists elsewhere in the platform.

**Task 02 — Admin CRUD Endpoints**
Objective: `POST/PUT/GET/DELETE /v1/admin/facts...` per §10.
Files to Create: `api/admin_facts_router.py`, `services/admin_fact_service.py`.
Dependencies: B-01, Task 01.
Expected Result: Full CRUD functioning with correct versioning semantics (never in-place mutation of published rows).
Definition of Done: Passes Task 06 tests.

**Task 03 — Scholar Approval Workflow Endpoints**
Objective: approve/reject/revoke endpoints, reusing A.3/A.5/A.6's confirmed review-queue pattern.
Dependencies: Task 02.
Expected Result: Edge Case 8 validation enforced; revoke requires reason field.
Definition of Done: Passes Task 06 tests.

**Task 04 — Disputed-Topic Flag Endpoint + AI-Assist Hard Gate**
Objective: `PATCH /v1/admin/topics/{id}/disputed-flag`; server-side check added to the existing AI-assist endpoint.
Files to Modify: existing AI-assist endpoint file (confirm location before modifying).
Dependencies: Task 01.
Expected Result: A disputed-topic fact's AI-assist call is rejected server-side regardless of UI state.
Definition of Done: Passes the Task 06 security bypass test.

**Task 05 — Audit Logging**
Objective: Every mutating endpoint writes an `audit_log` row; revocation/disputed-topic changes flagged `high_sensitivity`.
Dependencies: Tasks 02–04.
Definition of Done: Verified via Task 06 integration test.

**Task 06 — Tests**
Objective: Full coverage per §27, including the mandatory security bypass test.
Dependencies: Tasks 01–05.
Definition of Done: All green; security bypass test is CI-blocking.

**Task 07 — Documentation**
Dependencies: Task 06.
Definition of Done: OpenAPI docs and role matrix documented.

## 30. Definition of Done
- Full CRUD, versioning, and approval workflow functioning per role matrix.
- Disputed-Topic AI-assist disable verified enforced server-side, not just UI-hidden.
- Edge Case 8 (approval-without-review-record) rejected.
- Every mutation audit-logged, high-sensitivity actions flagged.
- All tests green including the CI-blocking security bypass test.

## 31. Final Verification Checklist
- [ ] Role matrix enforced per endpoint (`content_editor`/`scholar_reviewer`/`trust_safety`|`scholar_lead`)
- [ ] Direct AI-assist API bypass attempt for disputed-topic fact rejected server-side
- [ ] Approval without valid review record rejected (Edge Case 8)
- [ ] Revoke requires reason field
- [ ] Every mutation writes an audit_log row; revocation/disputed-topic changes flagged high-sensitivity
- [ ] No parallel review-queue mechanism built — reuses A.3/A.5/A.6 pattern
- [ ] Documentation updated
