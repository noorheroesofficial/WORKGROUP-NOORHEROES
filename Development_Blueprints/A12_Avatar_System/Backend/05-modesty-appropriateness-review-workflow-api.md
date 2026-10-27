# B-05 — Modesty & Appropriateness Review Workflow API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Implements the approval gate every newly-submitted avatar asset (base or item) must pass before becoming visible/purchasable/unlockable by children, enforcing segregation of duties between the submitting admin and the approving reviewer.

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-05 Modesty & Appropriateness Review Workflow API

## 4. Objective
Implement `status`-transition endpoints (`pending_review` → `published` | `rejected`) for `avatar_items` and `avatars`, enforcing that the approving admin_id must differ from the submitting admin_id, backing FR-12 and PRD §8's "segregation of duties: the asset's original creator should not be the sole approver" requirement.

## 5. Business Requirements
- Every new avatar item asset routes through the same content-governance review pipeline used elsewhere before publish — "it's just a cosmetic" is never an exemption (FR-12).
- Segregation of duties: a reviewer cannot silently edit and approve the same version, and specifically the submitting admin cannot self-approve (PRD §8, consistent with A.3's Scholar Review Workflow principle referenced in §12.5).
- Rejected items return to a draft/editable state with reviewer notes, not a dead end requiring re-creation from scratch.
- Approval gate applies to both `avatar_items` (B-03) and `avatars` base entries (B-04) — one shared review surface, not two parallel implementations.

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01. Mirrors A.3 Story Module's Scholar Review Workflow pattern (moral-summary review/approval — see A.3 Backend blueprint 12) for the general "reviewer cannot be the submitter" segregation-of-duties control, applied here to avatar assets specifically. Adds a `status` column (`pending_review` | `published` | `rejected`) to `avatar_items` and `avatars` (both established in B-01/B-03/B-04) rather than a separate review-queue table, since the review state is intrinsic to the catalog row's lifecycle, not a separate entity — consistent with how B-03/B-04 already describe items as created "in a pending-review state."

## 7. Existing Code to Reuse
- `AvatarItem`/`Avatar` models (B-01), extended with a `status` column in this task's migration
- `get_current_admin`/`require_admin_scope()` (`core/deps.py`)
- `AdminAuditRepository.log_action()` (`modules/admin/repository.py`)
- Segregation-of-duties check pattern referenced by A.3's Scholar Review Workflow blueprint (submitter_admin_id ≠ approver_admin_id comparison)

## 8. Files to Create
- `src/noorheroes/modules/avatars/review_schemas.py` (`ReviewQueueItemResponse`, `ApproveRequest`, `RejectRequest`)
- `src/noorheroes/modules/avatars/review_api.py` (`AvatarReviewRouter`)
- `alembic/versions/<rev>_add_status_submitted_by_to_avatar_tables.py`
- `tests/modules/avatars/test_modesty_review_workflow.py`
- `tests/modules/avatars/test_review_segregation_of_duties.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/models.py` — add `status CHECK IN ('pending_review','published','rejected')`, `submitted_by_admin_id UUID FK`, `reviewed_by_admin_id UUID FK NULLABLE`, `review_notes TEXT NULLABLE` to both `AvatarItem` and `Avatar`
- `src/noorheroes/modules/avatars/repository.py` — add `list_pending_review()`, `approve_item()`, `reject_item()` (parameterized by entity type: item vs. base)
- `src/noorheroes/modules/avatars/admin_api.py` (B-03) — set `status='pending_review'`, `submitted_by_admin_id=current_admin.admin_id` on create
- `main.py` — register `AvatarReviewRouter`

## 10. Backend Requirements
- `GET /v1/admin/avatars/review-queue` lists all `pending_review` items (both bases and catalog items) for the requesting admin's review, filterable by entity type.
- `POST /v1/admin/avatars/review-queue/{entityType}/{entityId}/approve` sets `status='published'`, `reviewed_by_admin_id=current_admin.admin_id` — **rejects with `403 SELF_APPROVAL_FORBIDDEN` if `current_admin.admin_id == submitted_by_admin_id`**, regardless of role.
- `POST /v1/admin/avatars/review-queue/{entityType}/{entityId}/reject` sets `status='rejected'`, `reviewed_by_admin_id`, `review_notes` — same segregation-of-duties check applies.
- Only `status='published'` items are ever returned by B-01's child-facing `GET /v1/children/{id}/inventory` or by B-03's/B-04's public-facing list paths — `pending_review`/`rejected` items are invisible to children by construction.
- Invalid state transitions (e.g., approving an already-published item, rejecting an already-rejected item) return a clear `409`, not a silent no-op or crash.
- Every approval/rejection writes an immutable `AdminAuditLog` row including both `submitted_by_admin_id` and `reviewed_by_admin_id` for traceability.

## 11. KMP Requirements
Not applicable — admin-only surface. This gate indirectly governs what children ever see (only `published` items reach B-01's response).

## 12. NextJS Requirements
Not applicable directly; consumed by N-03's Modesty & Appropriateness Review Queue.

## 13. API Contract

**Required API 1**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/avatars/review-queue?entity_type=item|base`
- **Response 200:** `{ "items": [ { "entity_type": "item", "entity_id": "uuid", "name": "...", "submitted_by_admin_id": "uuid", "submitted_at": "..." } ] }`
- **Authentication:** Bearer, admin session
- **Authorization:** `trust_safety` or `content_editor` scope

**Required API 2**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/avatars/review-queue/{entityType}/{entityId}/approve`
- **Response 200:** `{ "status": "published" }`
- **Authorization:** `trust_safety` or `content_editor` scope, **and** `current_admin.admin_id != submitted_by_admin_id`
- **Error Responses:** `401`; `403 SELF_APPROVAL_FORBIDDEN`; `404`; `409` invalid state transition

**Required API 3**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/avatars/review-queue/{entityType}/{entityId}/reject`
- **Request:** `{ "review_notes": "..." }`
- **Response 200:** `{ "status": "rejected" }`
- **Authorization:** same segregation-of-duties rule as approve
- **Error Responses:** `401`; `403 SELF_APPROVAL_FORBIDDEN`; `404`; `409`; `422` missing notes

## 14. Database Requirements
Extends `avatar_items`/`avatars` (B-01) with `status`, `submitted_by_admin_id`, `reviewed_by_admin_id`, `review_notes` columns per §9. Index `(status)` on both tables for the review-queue list query and for B-01/B-03/B-04's published-only filtering.

## 15. Validation
- `reject` requires non-empty `review_notes`.
- State-transition validity enforced server-side: only `pending_review` → `published`/`rejected` is a legal transition via these endpoints; a `rejected` item must be re-edited (via B-03/B-04's update path, which resets `status` back to `pending_review`) before it can be resubmitted.

## 16. Authentication
Bearer JWT, admin session via `get_current_admin`.

## 17. Authorization
`trust_safety` or `content_editor` scope required; the segregation-of-duties check (`submitted_by_admin_id != current_admin.admin_id`) is enforced **in addition to**, not instead of, role-scope checks.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Submitting admin attempts to approve their own submission | `403 SELF_APPROVAL_FORBIDDEN` |
| Approve/reject attempted on an already-published/rejected item | `409` invalid state transition |
| Reject without `review_notes` | `422` |
| Unauthorized/forbidden request | `401`/`403` |
| Database failure | `500`/`503` |

## 19. Offline First / 20. Local Data
N/A (backend, admin-only, online-by-design surface).

## 21. Localization
`review_notes` is admin-internal text, not user-facing; no localization requirement. Item/base `name` continues to follow B-01's translation-key convention.

## 22. RTL
N/A at the API layer.

## 23. Analytics
Not applicable (internal admin tooling); `AdminAuditLog` entries (including both submitter and reviewer IDs) are the operational record of truth for the content-governance review pipeline.

## 24. Performance
Low-traffic admin surface; standard indexed query on `(status)`.

## 25. Security
Segregation of duties (submitter ≠ approver) is this sub-feature's defining security control (§12.5 of the PRD) — verified by a CI-blocking test attempting self-approval. RBAC (`trust_safety`/`content_editor` scope) is a secondary control layered on top, not a substitute.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic.

## 27. Testing
- Unit: state-transition validity logic (`pending_review` → `published`/`rejected` only).
- Integration (P0): submitting admin attempts to approve their own submission → assert `403 SELF_APPROVAL_FORBIDDEN` (PRD §12.9 checklist item, CI-blocking).
- Integration: reject → item returns to `pending_review` upon re-edit via B-03/B-04's update path → resubmit → approve by a different admin succeeds.
- Integration: confirm B-01's child-facing inventory endpoint never returns a `pending_review`/`rejected` item.
- Integration: invalid state transition (double-approve) returns `409`.

## 28. Documentation
OpenAPI documentation for all three endpoints; document the segregation-of-duties guarantee explicitly in the `avatars` context architecture notes, cross-referencing A.3's Scholar Review Workflow as the platform-wide precedent for this pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Review-State Columns to Avatar Models**
- Task ID: B-05-T01
- Objective: `status`, `submitted_by_admin_id`, `reviewed_by_admin_id`, `review_notes` on `AvatarItem` and `Avatar`.
- Files to Modify: `src/noorheroes/modules/avatars/models.py`
- Files to Create: `alembic/versions/<rev>_add_status_submitted_by_to_avatar_tables.py`
- Validation: CHECK constraint on `status` enum.
- Tests: migration applies/rolls back cleanly.
- Definition of Done: columns present, indexed on `(status)`.

**Task 02 — Update B-03/B-04 Create Paths to Set Initial Review State**
- Task ID: B-05-T02
- Objective: new items/bases are created with `status='pending_review'`, `submitted_by_admin_id=current_admin.admin_id`.
- Files to Modify: `src/noorheroes/modules/avatars/admin_api.py`
- Definition of Done: newly-created rows always start in `pending_review`, never `published` by default.

**Task 03 — Implement Review-Queue Repository Methods**
- Task ID: B-05-T03
- Objective: `list_pending_review()`, `approve_item()`, `reject_item()` with the segregation-of-duties check embedded in the mutation methods (not left to the router alone), as defense-in-depth.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Tests: repository-level segregation-of-duties test.
- Definition of Done: repository methods reject self-approval even if called directly.

**Task 04 — Implement `AvatarReviewRouter`**
- Task ID: B-05-T04
- Objective: wire the three endpoints with RBAC + segregation-of-duties enforcement.
- Files to Create/Modify: `src/noorheroes/modules/avatars/review_api.py`; modify `main.py`.
- Authentication/Authorization: `Depends(get_current_admin)` + `require_admin_scope(...)` + explicit submitter/approver comparison.
- Implementation Details: audit-log every approve/reject including both admin IDs.
- Tests: integration tests for all three endpoints.
- Definition of Done: endpoints live, documented, audit-logged.

**Task 05 — Add Self-Approval Rejection Test (P0)**
- Task ID: B-05-T05
- Files to Create: `tests/modules/avatars/test_review_segregation_of_duties.py`
- Definition of Done: test passes, registered as CI-blocking per PRD §12.9.

**Task 06 — Update B-01/B-03/B-04 Read Paths to Filter by `status='published'`**
- Task ID: B-05-T06
- Objective: confirm child-facing and public-facing catalog reads exclude non-published rows.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py` (query filters on existing read methods from B-01/B-03/B-04)
- Tests: integration test confirming a `pending_review` item never appears in `GET /v1/children/{id}/inventory`.
- Definition of Done: no non-published row ever reaches a child-facing response.

**Task 07 — Add Full Workflow Test Suite & Documentation**
- Task ID: B-05-T07
- Files to Create: `tests/modules/avatars/test_modesty_review_workflow.py`
- Documentation: OpenAPI + `avatars` context architecture notes.
- Definition of Done: suite green, docs complete.

**Task 08 — Final Code Review**
- Task ID: B-05-T08
- Do Not Change: existing A.3 Scholar Review Workflow implementation (reference only); PostgreSQL credentials.
- Expected Result: PR merge-ready, CI green including the self-approval P0 gate.

## 30. Definition of Done
Review-queue, approve, and reject endpoints live, RBAC-guarded, and structurally prevent self-approval. Only `published` avatar assets ever reach child-facing surfaces. Rejected items are re-editable and resubmittable.

## 31. Final Verification Checklist
- [ ] `status`/`submitted_by_admin_id`/`reviewed_by_admin_id`/`review_notes` columns added and indexed
- [ ] New items/bases created via B-03/B-04 always start in `pending_review`
- [ ] Self-approval structurally rejected at the repository layer, not just the router (CI-blocking test passing)
- [ ] Invalid state transitions return `409`
- [ ] Only `published` items ever appear in child-facing responses (regression test passing)
- [ ] Every approve/reject action writes an immutable audit log row with both admin IDs
- [ ] Unit + integration tests passing
- [ ] OpenAPI documentation complete
- [ ] No PostgreSQL credential changes
- [ ] No unrelated existing-context code modified
