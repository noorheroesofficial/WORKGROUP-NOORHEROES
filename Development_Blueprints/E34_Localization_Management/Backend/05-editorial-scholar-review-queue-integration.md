# B-05 — Editorial/Scholar Review Queue Integration

## 1. Feature Context
The routing layer that sends general UI copy through editorial-only review while Islamic-content-adjacent strings — dua transliterations, prayer-related copy — pass through the same scholar-review discipline E.29 already established, reusing that queue infrastructure directly rather than building a parallel workflow.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
1.5 Editorial/Scholar Review Queue Integration (ID: **B-05**)

## 4. Objective
Wire `locale_string_version`'s review-stage transitions (Draft → Machine-Assisted → Editorial Review → [Scholar Review] → Published) into E.29's existing review-queue infrastructure, with content-category-based routing.

## 5. Business Requirements
- FR-5: Draft → Machine-Assisted → Editorial Review → Scholar Review → Published; unreviewed translations never reach child delivery APIs (enforced structurally by B-02, this sub-feature governs the workflow that gets a string TO published status).
- FR-10: Islamic-content-adjacent strings route through the same scholar-review discipline as E.29, distinct from general UI copy which requires only editorial review.
- Edge Case 2: a scholar rejection returns the specific locale's version to Draft, without affecting the same string's already-published translations in other locales.
- §5 Backend AI prompt intro: reuse E.29's existing Editorial/Scholar Review Queue infrastructure — do not build a parallel review workflow.

## 6. Existing Architecture
`localization` bounded context service consuming E.29's `content` bounded context review-queue service (`app/content/services/review_workflow_service.py`) — this sub-feature adds a `content_category` classification (`general_ui` vs `islamic_content_adjacent`) and routes accordingly, without duplicating E.29's segregation-of-duties or decision-recording logic.

## 7. Existing Code to Reuse
- E.29 B-03: `app/content/services/review_workflow_service.py::ReviewWorkflowService` (the actual state-machine/segregation-of-duties engine, reused directly)
- E.29 B-04: the scholar/child-safety review queue read APIs (pattern reused for a Localization-scoped queue view)
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/localization/services/translation_review_routing_service.py` — classifies a string's `content_category` and dispatches to E.29's `ReviewWorkflowService` with the correct review-stage sequence
- `app/localization/schemas/translation_review_schema.py`

## 9. Files to Modify
- E.29's `app/content/services/review_workflow_service.py` — confirm it accepts a generic "reviewable item" reference (not hardcoded to `content_version`) so `locale_string_version` can be registered as a second reviewable item type without modifying its core segregation-of-duties logic (additive, not a rewrite)
- `app/localization/services/string_table_service.py` (B-01) — call `TranslationReviewRoutingService` on string creation/update to initiate the review sequence

## 10. Backend Requirements
- `TranslationReviewRoutingService.classify_and_route()`: determines `content_category` from the string key's namespace/tag (e.g., keys under a `dua.*`/`prayer.*` namespace, or an explicit `is_islamic_content_adjacent` flag set at string-creation time) — general UI copy routes `Editorial Review → Published`; Islamic-content-adjacent routes `Editorial Review → Scholar Review → Published`, reusing E.29's exact `ReviewWorkflowService.submit_decision()` call for each stage.
- On a scholar rejection, only the specific `(string_id, locale_code)` version reverts to `Draft` — other locales' already-published versions of the same key are entirely untouched (confirmed via a locale-scoped rollback, never a cross-locale one).
- No parallel segregation-of-duties/self-review-prevention logic is written here — every such guarantee is inherited by calling E.29's existing engine.

## 11. Required API / API Contract
Internal service, largely surfaced via E.29's existing review-queue read/decision endpoints (`GET /v1/admin/reviews`, `PATCH /v1/admin/reviews/{id}`), filtered/scoped to `item_type='locale_string_version'` — no new admin-facing endpoint required beyond what E.29 already exposes, confirmed by extending E.29's queue-item polymorphism rather than adding a duplicate queue.

## 12. Database Requirements
No new tables — extends E.29's review-queue item reference to optionally point at `locale_string_version.version_id` in addition to `content_version.version_id` (a polymorphic or nullable dual-FK pattern, confirmed against E.29's actual schema).

## 13. Validation
`content_category` classification is deterministic and re-checked on every string update (a key's namespace doesn't change after creation, but the classification call itself isn't cached indefinitely in a way that could go stale).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("localization_manager")` for editorial-stage actions on general UI copy; `require_admin_scope("scholar_reviewer")` for the scholar-review stage on Islamic-content-adjacent strings (identical role gating to E.29).

## 16. Error Handling
Standard propagation of E.29's existing review-workflow error semantics (self-approval rejection, invalid stage transition, etc.) — no new error classes introduced here.

## 17. Security
Zero duplicated segregation-of-duties logic is this sub-feature's guarantee — mandatory test confirms this service's implementation contains no self-approval-prevention code of its own, only calls into E.29's existing engine, so any future security fix to that engine automatically applies here too. Second mandatory test confirms a scholar rejection on one locale's version never reverts a different locale's already-published version of the same key.

## 18. Analytics
`editorial_review_completed`, `scholar_review_completed` (shared event type with E.29, per §1.19) — the same event taxonomy, tagged with `item_type='locale_string_version'`.

## 19. Performance
No new query paths beyond E.29's existing, already-optimized review-queue infrastructure.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: `content_category` classification logic. Integration: **mandatory** — general UI copy string completes review via Editorial-only path; **mandatory** — Islamic-content-adjacent string requires Scholar Review in addition to Editorial Review; **mandatory** — scholar rejection reverts only the specific locale's version, other locales' published versions of the same key are unaffected; **mandatory** — structural test confirming zero duplicated segregation-of-duties code exists in this service.

## 22. Documentation
Docstring explaining the `content_category` routing rule and explicitly stating this service delegates all workflow-state-machine logic to E.29.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Confirm E.29's `ReviewWorkflowService` Accepts a Generic Reviewable-Item Reference**
Objective: Verify (and additively extend if needed) polymorphic item-type support, without touching its core segregation-of-duties logic. Files: E.29's `services/review_workflow_service.py` (additive change only). Tests: existing E.29 tests remain green. Definition of Done: confirmed additive, non-breaking.

**Task 02 — Implement `content_category` Classification**
Objective: Namespace/flag-based routing determination. Files: `services/translation_review_routing_service.py`. Dependencies: Task 01. Tests: classification tests. Definition of Done: tests pass.

**Task 03 — Wire Editorial-Only Path for General UI Copy**
Objective: Editorial Review → Published sequence via E.29's engine. Dependencies: Task 02. Tests: **mandatory** — general-UI-copy-editorial-only-path test. Definition of Done: test passes.

**Task 04 — Wire Scholar-Review Path for Islamic-Content-Adjacent Strings**
Objective: Editorial Review → Scholar Review → Published sequence. Dependencies: Task 02. Tests: **mandatory** — Islamic-content-adjacent-requires-scholar-review test. Definition of Done: test passes.

**Task 05 — Implement Locale-Scoped Rejection Rollback**
Objective: Rejection reverts only the specific `(string_id, locale_code)` version. Dependencies: Task 03, Task 04. Tests: **mandatory** — cross-locale-isolation-on-rejection test. Definition of Done: test passes.

**Task 06 — Integrate with B-01's Update Flow**
Objective: `StringTableService` triggers review routing on create/update. Dependencies: Task 02, B-01. Tests: integration test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, all mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero duplicated workflow/segregation-of-duties logic exists in this service — every such guarantee is inherited from E.29. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] General UI copy completes review via Editorial-only path — mandatory test passing
- [ ] Islamic-content-adjacent strings require Scholar Review in addition — mandatory test passing
- [ ] Scholar rejection reverts only the specific locale's version — mandatory test passing
- [ ] Zero duplicated segregation-of-duties code exists in this service — mandatory structural test passing
- [ ] `localization_manager`/`scholar_reviewer` scopes correctly gate their respective stages

## 25. Definition of Done
Translation strings flow through the correct review discipline for their content category, entirely powered by E.29's already-hardened review engine — no parallel workflow, no duplicated safety logic, and locale-scoped isolation on rejection.
