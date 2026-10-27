# B-04 — Scholar & Child-Safety Review Queue API

## 1. Feature Context
The public HTTP surface reviewers actually use: role-scoped queues (Scholar sees Scholar-stage items, Child-Safety sees Child-Safety-stage items) and a single decision endpoint that delegates all state-machine and segregation-of-duties logic to B-03.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.4 Scholar & Child-Safety Review Queue API (ID: **B-04**)

## 4. Objective
Implement `GET /v1/admin/reviews` (role-scoped) and `PATCH /v1/admin/reviews/{id}` (delegating to B-03's `ReviewWorkflowService`), with queue results strictly filtered to safety-pipeline-passed media (via B-02's exclusion filter) and fully populated source-viewer/diff/timestamped-comment data.

## 5. Business Requirements
- FR-8: assigned queue, source viewer, side-by-side version diff, timestamped comments for audio/video, regional/jurisprudential notes, Approve/Request Changes/Reject/Escalate actions.
- FR-5 (cross-cutting from B-02): a queue response must never include an item whose media hasn't passed the safety pipeline.

## 6. Existing Architecture
`modules/content_cms/review/api.py::ReviewRouter`, thin HTTP layer over B-03's engine and B-01's version/diff data, reusing B-02's `filter_pass_only()` helper in its queue query.

## 7. Existing Code to Reuse
- `modules/content_cms/review/workflow_engine.py::ReviewWorkflowService` (B-03)
- `modules/content_cms/repository.py::ContentVersionRepository`, diff logic (B-01)
- `modules/content_cms/media/repository.py::MediaAssetRepository.filter_pass_only()` (B-02)
- `core/deps.py::get_current_admin`, `require_admin_scope()`

## 8. Files to Create
- `src/noorheroes/modules/content_cms/review/schemas.py` — `ReviewQueueItemResponse`, `ReviewDetailResponse`, `ReviewDecisionRequest`
- `src/noorheroes/modules/content_cms/review/api.py` — `ReviewRouter`
- `tests/modules/content_cms/review/test_review_queue_api.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `ReviewRouter` under `/v1/admin/reviews`

## 10. Backend Requirements
- `GET /v1/admin/reviews`: scoped by the requesting admin's role — `scholar_reviewer` sees only `review_stage='scholar'` items, `child_safety_reviewer` sees only `review_stage='child_safety'` items; underlying query joins B-02's `filter_pass_only()` so a quarantined/pending-media item is structurally absent from the result, never merely hidden client-side.
- `GET /v1/admin/reviews/{id}`: full detail — source viewer payload, version diff (via B-01), timestamped media comments, regional/jurisprudential notes field.
- `PATCH /v1/admin/reviews/{id}`: validates the requesting admin's role matches the item's current `review_stage`, then delegates entirely to `ReviewWorkflowService.submit_decision()` — this router contains zero SoD or state-machine logic of its own.

## 11. API Contract

### `GET /v1/admin/reviews`
- Auth: `scholar_reviewer` or `child_safety_reviewer` role. Response 200: role-scoped, safety-pipeline-filtered queue.

### `GET /v1/admin/reviews/{id}`
- Auth: matching reviewer role. Response 200: full review detail (source viewer, diff, comments).

### `PATCH /v1/admin/reviews/{id}`
- Auth: `scholar_reviewer` or `child_safety_reviewer`, matching the review stage. Request: `{ "decision": "approve"|"request_changes"|"reject"|"escalate", "comments": [...], "timestamped_comments": [...] }`. Response 200: updated review record. Errors: `403 SEGREGATION_OF_DUTIES_VIOLATION` (from B-03), `409 STAGE_MISMATCH`.

## 12. Database Requirements
No new tables — reads `content_review` (B-03), `content_version` (B-01), `media_asset`/`safety_pipeline_result` (B-02).

## 13. Validation
`decision` restricted to the four enum values (defensive re-validation alongside B-03's own check).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
Role-stage matching is the primary authorization gate: a `scholar_reviewer` cannot act on a `child_safety` item and vice versa, checked before delegating to B-03.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Non-matching role attempts a decision on the wrong stage | `403 FORBIDDEN` (role/stage mismatch, distinct from B-03's SoD `403`) |
| Item under review references quarantined/pending media | Never appears in queue results at all |
| SoD violation | `403 SEGREGATION_OF_DUTIES_VIOLATION` (from B-03) |
| Empty queue | `200` with empty array — "Queue clear" state, not an error |
| Database failure | `503`, logged |

## 17. Security
Zero independent SoD/state-machine logic in this router — entirely delegated to B-03, eliminating any risk of a divergent, weaker enforcement path being accidentally introduced at the API layer.

## 18. Analytics
Audited via `AuditLogService` (through B-03's transition calls); `scholar_review_opened`, `content_submitted_for_scholar_review`, `content_submitted_for_child_safety_review` recorded as audit-log entries at the appropriate call sites.

## 19. Performance
Queue query joins content_version + content_review + media/safety-pipeline-status with proper indexing (`content_review(version_id, stage)`) — no N+1 across queue items.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: role-stage-matching rejection, empty-queue response shape.
- Integration: **mandatory** — confirm a quarantined-media-referencing draft never appears in either queue's listing, end-to-end through this API (not just at B-02's repository layer).
- Integration: full Approve-at-scholar-stage → item-appears-in-child-safety-queue transition, verified through this API.

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement Queue/Detail/Decision Schemas**
Objective: Response/request shapes. Follow: existing Pydantic v2 conventions. Tests: schema validation. Definition of Done: schemas used by Task 03.

**Task 02 — Implement Role-Scoped Queue Query**
Objective: `GET /v1/admin/reviews` filtered by role and by B-02's `filter_pass_only()`. Dependencies: B-02, B-03. Tests: role-scoping test, **mandatory** end-to-end quarantine-exclusion test. Definition of Done: both tests pass.

**Task 03 — Implement Detail Endpoint**
Objective: `GET /v1/admin/reviews/{id}` assembling source viewer, diff (via B-01), comments. Dependencies: B-01. Tests: detail-assembly test. Definition of Done: test passes.

**Task 04 — Implement Decision Endpoint Delegating to B-03**
Objective: role-stage match check, then pure delegation to `ReviewWorkflowService.submit_decision()`. Dependencies: B-03. Tests: role-stage-mismatch rejection, full delegation flow test. Definition of Done: tests pass.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm zero SoD/state-machine logic exists in this router outside of delegation to B-03; confirm the quarantine-exclusion filter is genuinely reused, not reimplemented. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Queue results strictly role-scoped by review stage
- [ ] Quarantined/pending-media items never appear in any queue result, verified end-to-end through this API
- [ ] Decision endpoint delegates entirely to B-03 — zero local SoD/state-machine logic
- [ ] Empty queue returns a valid "Queue clear" empty response, not an error
- [ ] Role-stage mismatch rejected distinctly from a SoD violation

## 25. Definition of Done
Scholar and Child-Safety reviewers have a role-scoped, safety-pipeline-filtered queue and a single decision path that provably delegates every state-machine and segregation-of-duties guarantee to B-03.
