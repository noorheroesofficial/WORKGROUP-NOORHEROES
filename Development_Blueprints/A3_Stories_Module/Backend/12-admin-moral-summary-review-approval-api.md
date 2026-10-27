# B-12 — Admin Moral Summary Review & Approval API

## 1. Feature Context
The scholar-facing safety-net editor: surfaces low-confidence AI-generated morals for human review and lets a `scholar_reviewer` author/approve the `human_reviewed=true` fallback that B-06's engine falls back to. Approval authority is restricted with defense-in-depth (UI + API) since this directly gates what children can see.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.12 Admin Moral Summary Review & Approval API (ID: **B-12**)

## 4. Objective
Implement a paginated review queue and approval workflow inside the existing `ai_safety` + `admin` modules, reading B-06's persisted `content_moral_version` rows and gating approval behind the `scholar_reviewer` RBAC scope with full audit logging.

## 5. Business Requirements
- §8 Admin Requirements: Moral Summary Review Queue — full CRUD gated by scholar-approval requirement before any moral can be marked `human_reviewed=true` and used live.
- §9 Admin AI Code-Generation Prompt: queue shows rows where `ai_generated=true` and `ai_confidence_score` below the configured threshold (read from shared config, not hardcoded); approve requires `scholar_reviewer` role, enforced via RBAC context; disable (not just server-reject) for unauthorized users.

## 6. Existing Architecture
Extends the existing `ai_safety` module (`AISafetyService`, `SafetyAuditRepository`) with a review-queue read/write path over B-06's `content_moral_version` table, plus the existing `admin` module's audit pattern.

## 7. Existing Code to Reuse
- `modules/ai_safety/moral_summary_repository.py::ContentMoralVersionRepository` (B-06, extend with review-queue query methods)
- `modules/admin/service.py::AdminService.log_action()`
- `core/deps.py::get_current_admin`, `require_admin_scope()`

## 8. Files to Create
- `src/noorheroes/modules/ai_safety/review_schemas.py` — `MoralReviewQueueItem`, `MoralApprovalRequest`
- `src/noorheroes/modules/ai_safety/review_service.py` — `MoralReviewService(BaseService)`
- `tests/modules/ai_safety/test_moral_review_service.py`
- `tests/modules/ai_safety/test_moral_review_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/ai_safety/api.py::AISafetyRouter` — add `GET /admin/v1/moral-summaries/review-queue`, `POST /admin/v1/moral-summaries/{version_id}/approve`, `GET /admin/v1/config/moral-confidence-threshold`
- `src/noorheroes/modules/ai_safety/moral_summary_repository.py::ContentMoralVersionRepository` (B-06) — add `list_low_confidence(threshold, cursor)`

## 10. Backend Requirements
- `MoralReviewService.list_review_queue(cursor)`: paginated query for `content_moral_version` where `ai_generated=true AND ai_confidence_score < threshold`, threshold read from a shared config source (same config B-06 reads, never a separately hardcoded value in this module).
- `MoralReviewService.approve(version_id, reviewer_id, replacement_text)`: creates a new `content_moral_version` row with `human_reviewed=true, ai_generated=false`, linked to the same `episode_id`+`locale` — never mutates the flagged AI row in place (preserves the original for audit trail).
- Approval requires `scholar_reviewer` scope — enforced via `require_admin_scope("scholar_reviewer")` at the router dependency layer, in addition to N-02's frontend button-disabling.
- Every approval writes an audit log row.

## 11. API Contract

### `GET /admin/v1/moral-summaries/review-queue`
- Auth: Admin Bearer + `scholar_reviewer` scope (read may be broader — confirm against existing admin read-scope conventions). Response 200: paginated low-confidence rows with AI text + confidence score.

### `GET /admin/v1/config/moral-confidence-threshold`
- Auth: Admin Bearer. Response 200: `{ "threshold": 0.75 }` — the same value B-06 reads at runtime, exposed for frontend display only (read-only here, not settable through this endpoint).

### `POST /admin/v1/moral-summaries/{version_id}/approve`
- Auth: Admin Bearer + `scholar_reviewer` scope. Request: `{ "replacement_text": "..." }`. Response 200: newly created `human_reviewed=true` version. Errors: `403 FORBIDDEN` (wrong role), `404 VERSION_NOT_FOUND`.

## 12. Database Requirements
- Reads/writes `content_moral_version` (B-06's table) — no new tables.

## 13. Validation
- `replacement_text` required, non-empty, length-bounded appropriate to age-band vocabulary norms (defer exact bound to existing content-length conventions elsewhere in `content`).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("scholar_reviewer")` strictly enforced on the approval endpoint — this is the primary security control preventing an unqualified admin from approving child-facing moral content.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Non-scholar-reviewer attempts approval | `403 FORBIDDEN` at the API layer (independent of frontend button state) |
| Unknown `version_id` | `404 VERSION_NOT_FOUND` |
| Empty/missing replacement text | `422` |
| Database failure | `503`, logged, no partial audit-log write |

## 17. Security
- Defense-in-depth RBAC: N-02's frontend disables the approve button for non-scholar-reviewers, this API independently rejects the same request server-side.
- Original flagged AI row never mutated — approval always creates a new versioned row, preserving a complete audit trail of what the AI produced versus what was approved.

## 18. Analytics
Internal admin action — audited via `AdminAuditLog`, not the child-facing analytics taxonomy.

## 19. Performance
Low-volume admin surface — standard indexed query on `(episode_id, locale)` plus a confidence-score filter is sufficient; no special caching needed.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: threshold read from shared config (not hardcoded — test asserts the same config value B-06 uses), non-scholar-reviewer rejection.
- Integration: approval creates a new row without mutating the original flagged row; approved row is subsequently returned by B-06's `get_human_reviewed()` lookup (end-to-end confirmation that the approval actually takes effect for the live fallback path).

## 22. Documentation
Update OpenAPI schema; document the shared confidence-threshold config key name.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `MoralReviewQueueItem`/`MoralApprovalRequest` Schemas**
Objective: Define request/response shapes. Follow: existing Pydantic v2 conventions. Tests: schema validation. Definition of Done: schemas used by Task 03.

**Task 02 — Extend `ContentMoralVersionRepository` with `list_low_confidence()`**
Objective: Paginated query filtered by `ai_generated=true AND ai_confidence_score < threshold`. Follow: `BaseRepository` pagination pattern from B-01. Tests: filter correctness at the threshold boundary. Definition of Done: test passes.

**Task 03 — Implement `MoralReviewService.approve()`**
Objective: Create new `human_reviewed=true` version without mutating the original. Dependencies: Task 02, `AdminService.log_action()`. Business Rules: original row untouched. Tests: approval creates a new row, original preserved, audit log written. Definition of Done: tests pass.

**Task 04 — Add Router Endpoints with `scholar_reviewer` Scope**
Objective: Wire the three admin routes with strict RBAC on the approval endpoint. Tests: covered by Task 06, plus an explicit non-scholar-reviewer `403` test. Definition of Done: endpoints live, RBAC verified.

**Task 05 — Wire End-to-End Confirmation with B-06**
Objective: Integration test confirming an approved replacement is what B-06's `get_human_reviewed()` subsequently returns. Dependencies: B-06. Definition of Done: end-to-end test passes.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 08 — Final Code Review**
Objective: Confirm `scholar_reviewer` scope is enforced independent of frontend state, confirm original AI-flagged rows are never mutated. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Review queue filters strictly on `ai_generated=true AND ai_confidence_score < threshold` (shared config, not hardcoded)
- [ ] Approval endpoint rejects non-`scholar_reviewer` requests with `403` at the API layer
- [ ] Approval creates a new versioned row; the original flagged AI row is never mutated
- [ ] Approved replacement is confirmed end-to-end to be what B-06's fallback lookup returns
- [ ] Every approval writes an immutable audit log row
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Scholars can review and approve safe moral-summary fallbacks through an audited, role-gated workflow that provably feeds B-06's live fallback path — closing the loop on the feature's core child-safety guarantee.
