# B-03 — Review Workflow State Machine & Segregation-of-Duties Engine

## 1. Feature Context
The other of the two highest-priority guarantees in E.29: a reviewer can never approve a content version they personally edited. This is enforced twice — once in application code, once as a database CHECK constraint that would reject the same violation even via a direct SQL INSERT bypassing every layer of this codebase.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.3 Review Workflow State Machine & Segregation-of-Duties Engine (ID: **B-03**)

## 4. Objective
Implement the internal `ReviewWorkflowService` driving Draft → Editorial → Scholar → Child-Safety → Scheduled/Published/Suspended/Archived, with a dual-layer (application + database) segregation-of-duties check and full audit-trail writes on every transition.

## 5. Business Requirements
- FR-7: canonical lifecycle with every transition recording actor, reason, version, and audit ID.
- FR-9: segregation of duties non-negotiable — a reviewer cannot silently edit and approve the same version; publication is a separate permission from review approval; emergency suspension is safety-roles-only and always audited.
- Edge Case 1–2: SoD applies per-content-item/per-version, not as a blanket cross-item restriction — the same person may review unrelated items, and may re-review a *different* version of the same item after another editor's changes.
- Edge Case 5: escalation without a clear assignee still succeeds, routed to a Scholar Review Board lead role.

## 6. Existing Architecture
Internal service inside `modules/content_cms/` — no public HTTP surface of its own (B-04 exposes the queue/decision endpoints that call into this engine). Reuses B-01's `content_version.last_edited_by` as the authoritative edit-identity record.

## 7. Existing Code to Reuse
- `modules/content_cms/repository.py::ContentVersionRepository` (B-01, read `last_edited_by`)
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28 B-05)
- `common/base_service.py`
- `core/exceptions.py`

## 8. Files to Create
- `src/noorheroes/modules/content_cms/review/models.py` — `ContentReviewOrm`
- `alembic/versions/xxxx_create_content_review_with_sod_check.py` — includes the database-level SoD CHECK constraint
- `src/noorheroes/modules/content_cms/review/repository.py` — `ContentReviewRepository`
- `src/noorheroes/modules/content_cms/review/workflow_engine.py` — `ReviewWorkflowService(BaseService)`
- `tests/modules/content_cms/review/test_workflow_engine.py`
- `tests/modules/content_cms/review/test_segregation_of_duties_db_constraint.py`

## 9. Files to Modify
- None outside this sub-feature's own files; B-04 (Scholar/Child-Safety Queue API) calls into `ReviewWorkflowService` from its own router.

## 10. Backend Requirements
- `ReviewWorkflowService.submit_decision(version_id, reviewer_id, stage, decision, comments, timestamped_comments)`: first checks — at the application layer — whether `reviewer_id == content_version.last_edited_by` for the target `version_id`; if so, raises `SegregationOfDutiesViolation` (`403`) before any further processing.
- On `decision='approve'` at `stage='scholar'`: transitions the version's `review_stage` to `child_safety`. On `decision='approve'` at `stage='child_safety'`: transitions to `scheduled`/publish-eligible (does not itself publish — that is B-06's exclusive action).
- On `decision='reject'`: transitions the content item to `archived`, reason logged.
- On `decision='escalate'`: marks the item `escalated`, removes it from the normal queue, and assigns it to a configured Scholar Review Board lead role (or a fallback senior-role query if no specific assignee is configured) — never fails or leaves the item stuck.
- Every transition calls `AuditLogService.log_action()` with actor, reason, version, and a unique audit ID.
- The SoD check compares against the *specific version's* `last_edited_by`, never a blanket "has this admin ever edited anything in this content item" check — explicitly scoped per Edge Cases 1–2.

## 11. API Contract
No public HTTP endpoint of its own. Internal service contract:
```
ReviewWorkflowService.submit_decision(version_id, reviewer_id, stage, decision, comments, timestamped_comments) -> ContentReview
```
Called exclusively from B-04's `PATCH /v1/admin/reviews/{id}`.

## 12. Database Requirements
- `content_review`: FK `version_id`, `reviewer_id`; CHECK `decision IN ('approve','request_changes','reject','escalate')`; index `(version_id, stage)`.
- **Database-level segregation-of-duties CHECK constraint**: `CHECK (reviewer_id != (SELECT last_edited_by FROM content_version WHERE version_id = content_review.version_id))` — defense-in-depth alongside the application-layer check, verified by a direct-INSERT bypass test.

## 13. Validation
- `decision` restricted to the four enum values.
- `stage` must match the version's current `review_stage` — a decision submitted for the wrong stage is rejected (`409 STAGE_MISMATCH`).

## 14. Authentication
N/A — internal service; the calling endpoint (B-04) is already authenticated.

## 15. Authorization
N/A — internal service; B-04 enforces `scholar_reviewer`/`child_safety_reviewer` role matching before calling in.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Reviewer's identity matches the version's `last_edited_by` | `403 SEGREGATION_OF_DUTIES_VIOLATION`, rejected before any state change |
| Direct database INSERT into `content_review` violating the CHECK constraint | Rejected at the database layer, independent of any application code |
| Decision submitted for a stage that doesn't match the version's current `review_stage` | `409 STAGE_MISMATCH` |
| Escalation with no configured assignee | Still succeeds, routed to a fallback senior-role query (Edge Case 5) |
| Database failure mid-transition | `503`, full rollback, logged |

## 17. Security
- **Dual-layer enforcement is this engine's entire reason for existing**: the application-layer check catches the violation early with a clear error; the database CHECK constraint guarantees the invariant holds even if every line of application code were bypassed — the PRD explicitly treats this as the platform's most zero-tolerance guarantee in the entire module.
- SoD scoping is precise (per-version, not per-person-blanket) — verified by tests that a reviewer *can* review unrelated items and *can* re-review a later version of the same item after edits by the same or another editor.

## 18. Analytics
Internal engine — every transition audited via `AuditLogService`; `segregation_of_duties_violation_blocked` is emitted as a distinct internal/security signal event, separate from normal review-decision audit entries, so it can be alerted on independently (per PRD DevOps §10).

## 19. Performance
SoD check is a single indexed lookup (`content_version.last_edited_by` by `version_id`) — no N+1, no full-table scan.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: application-layer SoD rejection, per-version (not blanket) scoping (Edge Cases 1–2 explicit tests), stage-mismatch rejection, escalation-with-no-assignee fallback.
- **Mandatory database-level test**: attempt a direct SQL `INSERT` into `content_review` that would violate the SoD CHECK constraint and confirm the database itself rejects it, independent of any application-layer check (per PRD backend AI-prompt requirement #1).
- **Mandatory API-level test**: a fixture admin edits a `content_version`, then attempts to submit a `content_review` decision for that same version as the reviewer, and confirm `403 SEGREGATION_OF_DUTIES_VIOLATION`.
- Integration: full request-changes → re-edit → same-reviewer-approves-new-version cycle (confirming this is explicitly permitted, per Edge Case 2).

## 22. Documentation
Module README documents the dual-layer SoD model and the exact per-version (not blanket) scoping rule as a permanent architectural invariant, since this is the platform's single most safety-critical guarantee in the entire Admin Portal per the PRD.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ContentReviewOrm` Model & Migration with Database-Level SoD Constraint**
Objective: Add the table and the CHECK constraint comparing `reviewer_id` against the target version's `last_edited_by`. Follow: existing SQLAlchemy/Alembic conventions. Do Not Change: `content_version` schema (B-01) beyond what's already there. Tests: **mandatory** — direct-INSERT bypass test. Definition of Done: bypass test passes.

**Task 02 — Implement `ContentReviewRepository`**
Objective: Data access for review decisions. Follow: `BaseRepository`. Tests: stage-scoped query correctness. Definition of Done: repository methods covered.

**Task 03 — Implement `ReviewWorkflowService.submit_decision()` Application-Layer SoD Check**
Objective: Pre-flight identity comparison before any state change. Dependencies: Task 02, B-01's `ContentVersionRepository`. Tests: **mandatory** — API-level self-approval-rejection test; per-version-not-blanket scoping tests (Edge Cases 1–2). Definition of Done: all mandatory tests pass.

**Task 04 — Implement Stage Transition Logic**
Objective: approve/request_changes/reject/escalate branching per §10. Dependencies: Task 03. Tests: stage-mismatch rejection, escalation-fallback-routing test. Definition of Done: tests pass.

**Task 05 — Wire Audit Logging with `segregation_of_duties_violation_blocked` as a Distinct Event**
Objective: `AuditLogService.log_action()` on every transition; a separately-flagged internal/security event on SoD rejection specifically. Dependencies: E.28 B-05. Tests: distinct-event-type assertion. Definition of Done: test passes.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including both mandatory tests. Definition of Done: all green in CI, registered as required CI gates per PRD DevOps §10.

**Task 07 — Final Code Review**
Objective: Confirm the dual-layer guarantee holds with zero bypass path; confirm SoD scoping is genuinely per-version, not accidentally per-person-blanket. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Application-layer SoD check rejects a reviewer approving their own edited version, before any state change
- [ ] Database-level CHECK constraint independently rejects the same violation via a direct INSERT bypass test
- [ ] SoD scoping is per-version, not blanket — same reviewer can review unrelated items and later versions of the same item
- [ ] Escalation with no configured assignee still succeeds, routed to a fallback senior role
- [ ] Every transition writes an audit entry with actor, reason, version, and a unique audit ID
- [ ] `segregation_of_duties_violation_blocked` emitted as a distinct, alertable internal/security event
- [ ] Both mandatory tests (DB-constraint bypass, API-level self-approval) registered as CI-blocking gates
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
The review workflow state machine drives content through every required gate with a provably dual-layer-enforced segregation-of-duties guarantee — the platform's single most zero-tolerance security property in the Admin Portal, consumed by B-04's queue API and feeding B-06's publish-eligibility check.
