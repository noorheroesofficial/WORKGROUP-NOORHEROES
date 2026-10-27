# B-06 — Content Publish & Scheduling API (with Episode-Sequencing Validation)

## 1. Feature Context
The final gate before anything reaches a child: publish is blocked unless a version has genuinely completed both Scholar and Child-Safety approval — no partial-approval state is ever publishable — and, for episodic series, unless the preceding episode's unlock threshold is configured.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.6 Content Publish & Scheduling API (ID: **B-06**)

## 4. Objective
Implement `PATCH /v1/admin/content/{id}/publish`, requiring the distinct `publisher` role, verifying both required `content_review` approvals exist, enforcing episode-sequencing validation, and triggering B-05's question version-lock on success.

## 5. Business Requirements
- FR-6: episode N+1 cannot publish without episode N's unlock threshold configured.
- FR-9: publication is a separate permission from review approval.
- Acceptance Criteria: only a version that has completed every required gate (editorial, safety, scholar, child-safety) is publishable — no partial-approval state is publishable.

## 6. Existing Architecture
`modules/content_cms/publish/` sub-package, reading `content_review` (B-03) and `content_version`/`content_item` (B-01), calling B-05's `lock_all_for_content()` and B-02's CDN/media finalization as needed.

## 7. Existing Code to Reuse
- `modules/content_cms/review/repository.py::ContentReviewRepository` (B-03)
- `modules/content_cms/repository.py::ContentItemRepository`, `ContentVersionRepository` (B-01)
- `modules/content_cms/quiz/service.py::QuizQuestionService.lock_all_for_content()` (B-05)
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28)

## 8. Files to Create
- `src/noorheroes/modules/content_cms/publish/schemas.py` — `PublishRequest`, `PublishResponse`
- `src/noorheroes/modules/content_cms/publish/service.py` — `PublishService(BaseService)`
- `src/noorheroes/modules/content_cms/publish/episode_sequencing.py` — sequencing validation helper
- `src/noorheroes/modules/content_cms/publish/api.py` — publish route additions to `ContentRouter`
- `tests/modules/content_cms/publish/test_publish_eligibility.py`
- `tests/modules/content_cms/publish/test_episode_sequencing.py`

## 9. Files to Modify
- `src/noorheroes/modules/content_cms/api.py` (B-01) — add `PATCH /v1/admin/content/{id}/publish`

## 10. Backend Requirements
- `PublishService.publish(content_id, actor_id, scheduled_at=None)`: queries `content_review` for the target version, requires a row with `decision='approve', stage='scholar'` **and** a row with `decision='approve', stage='child_safety'` — reject (`409 INCOMPLETE_APPROVAL`) if either is missing.
- `episode_sequencing.validate(content_item)`: for `content_type='episode'` with a configured `sequence_position`, looks up the immediately-preceding `sequence_position` episode in the same series and rejects (`409 PRECEDING_EPISODE_UNLOCK_THRESHOLD_MISSING`) if that episode's `unlock_threshold` field is unpopulated.
- On successful publish: sets `content_item.status='published'`, calls `QuizQuestionService.lock_all_for_content()`, supports an optional `scheduled_at` for future-dated publish (state `scheduled` until the scheduled time, then a background job flips to `published`).
- `require_admin_scope("publisher")` — a role distinct from `content_editor`/`scholar_reviewer`/`child_safety_reviewer`, per FR-9's explicit separate-permission requirement.

## 11. API Contract

### `PATCH /v1/admin/content/{id}/publish`
- Auth: `publisher` role. Request: `{ scheduled_at?: "..." }`. Response 200: `{ status: "published"|"scheduled" }`. Errors: `409 INCOMPLETE_APPROVAL`, `409 PRECEDING_EPISODE_UNLOCK_THRESHOLD_MISSING`.

## 12. Database Requirements
No new tables — reads `content_review`, `content_item`, `content_version`.

## 13. Validation
Both-approvals check and episode-sequencing check both run before any state mutation; either failing blocks the entire publish attempt atomically.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("publisher")` — exclusively; neither `content_editor` nor `scholar_reviewer`/`child_safety_reviewer` roles satisfy this check even if held by the same admin account (per Edge Case 9's precise "checks the action, not the person" framing).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Only Scholar approval present, Child-Safety missing | `409 INCOMPLETE_APPROVAL` |
| Episode N+1 published attempt, N's unlock threshold unconfigured | `409 PRECEDING_EPISODE_UNLOCK_THRESHOLD_MISSING` |
| Non-`publisher` role attempts publish | `403 FORBIDDEN` |
| Scheduled publish job encounters a since-suspended item | Publish aborted, logged, item remains in its current state |
| Database failure | `503`, full rollback, logged |

## 17. Security
This endpoint is the single choke point through which content actually becomes visible to children — its both-approvals-required and episode-sequencing checks are the last structural defenses against partial-approval or gap-containing content ever reaching production, backed by an audit entry on every publish.

## 18. Analytics
`content_published`, `content_scheduled`, `episode_unlock_threshold_validation_blocked` audited via `AuditLogService`.

## 19. Performance
Both-approvals lookup and episode-sequencing lookup are both single indexed queries; no heavy computation on the publish path.

## 20. Library Requirements
No new libraries; scheduled-publish background flip reuses the existing Celery infrastructure (mirrors B-02's task pattern).

## 21. Testing
- Unit: both-approvals-required rejection with only one present, episode-sequencing rejection.
- **Mandatory test**: a version with only scholar approval (missing child-safety approval) is rejected from publishing (per PRD backend AI-prompt requirement #5).
- **Mandatory test**: episode N+1 publish blocked when episode N's `unlock_threshold` is unconfigured (per PRD backend AI-prompt requirement #6).
- Integration: full both-approvals-present → publish → quiz-questions-locked flow.

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement Both-Approvals-Required Check**
Objective: Query `content_review` for both required stage/decision rows. Dependencies: B-03. Tests: **mandatory** — single-approval rejection test. Definition of Done: test passes.

**Task 02 — Implement Episode-Sequencing Validation**
Objective: `episode_sequencing.validate()` per §10. Dependencies: B-01. Tests: **mandatory** — N+1-blocked-without-N's-threshold test. Definition of Done: test passes.

**Task 03 — Implement `PublishService.publish()`**
Objective: Orchestrates both checks, status transition, quiz-lock call, optional scheduling. Dependencies: Task 01–02, B-05. Tests: full happy-path and both rejection paths. Definition of Done: tests pass.

**Task 04 — Add Router Endpoint with `publisher`-Only Scope**
Objective: Wire the publish route. Tests: role-rejection test (a `content_editor`/`scholar_reviewer`-only admin cannot publish). Definition of Done: test passes.

**Task 05 — Implement Scheduled-Publish Background Job**
Objective: Celery task flipping `scheduled` → `published` at the configured time. Dependencies: Task 03. Tests: scheduled-flip timing test. Definition of Done: test passes.

**Task 06 — Wire Audit Logging**
Objective: `content_published`/`content_scheduled` events. Dependencies: E.28 B-05. Tests: audit row assertions. Definition of Done: test passes.

**Task 07 — Add Unit & Integration Tests**
Objective: Full coverage per §21, both mandatory tests included. Definition of Done: all green in CI, registered as required CI gates.

**Task 08 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 09 — Final Code Review**
Objective: Confirm no partial-approval state is ever publishable under any code path; confirm `publisher` role is genuinely distinct from the review roles. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Publish requires both Scholar AND Child-Safety approval rows — verified by a mandatory single-approval-rejection test
- [ ] Episode N+1 cannot publish without episode N's unlock threshold configured — verified by a mandatory test
- [ ] Only `publisher` role can call this endpoint, distinct from review roles
- [ ] Successful publish triggers B-05's irreversible quiz-question version lock
- [ ] Scheduled publish correctly flips state at the configured time via background job
- [ ] Every publish/schedule action audited

## 25. Definition of Done
Publish is a provably all-gates-complete, role-separated, episode-sequencing-safe action — the final structural guarantee behind the platform's "nothing reaches a child without genuinely completing every review stage" promise.
