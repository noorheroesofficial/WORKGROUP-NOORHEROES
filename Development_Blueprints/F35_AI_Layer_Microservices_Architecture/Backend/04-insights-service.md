# B-04 — Insights Service

## 1. Feature Context
The service generating parent-facing habit/growth summaries — deliberately restricted to observable-pattern description, never diagnosis, sibling comparison, or false certainty, and routing exclusively through C.20's already-hardened Content Safety Validator rather than inventing a second safety gate.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.4 Insights Service (ID: **B-04**)

## 4. Objective
Build `POST /v1/ai/insights/generate`, producing privacy-preserving, PII-minimized parent reports that route through C.20's existing Content Safety Validator before persistence, with zero new validation logic.

## 5. Business Requirements
- FR-1: parent reports, habit analytics, growth insights; controls: privacy-preserving aggregation, child PII minimized.
- FR-8: may summarize consistency, skill strengths/refresh needs, story themes, healthy usage, suggested next activity; must NOT diagnose developmental/behavioral/religious conditions, compare siblings, infer sensitive traits, or present uncertain conclusions as settled fact.
- Edge Case 4: the service has no access to external context (e.g., a support-ticket-mentioned life event) by design — it correctly limits itself to describing the observable pattern without speculating about causes.

## 6. Existing Architecture
`ai` module, `app/ai/services/insights_service.py`, calling C.20's `app/parent_dashboard/services/content_safety_validator.py::ContentSafetyValidator` before any report is persisted as a deliverable.

## 7. Existing Code to Reuse
- C.20's `ContentSafetyValidator` (called as-is, zero reimplementation)
- A.9's mastery/skill data, A.7's habit-tracking data (consumed read-only, not duplicated)

## 8. Files to Create
- `app/ai/routers/insights_router.py`
- `app/ai/services/insights_service.py`
- `app/ai/repositories/insights_data_repository.py` — aggregates habit/mastery/engagement data strictly from the platform's own tables, no external inputs
- `app/ai/schemas/insights_schema.py`

## 9. Files to Modify
- `app/ai/routers/__init__.py` — register router

## 10. Backend Requirements
- `InsightsDataRepository`: reads ONLY the platform's own habit/mastery/engagement/content-interaction tables — no code path accepts or references any external context (support tickets, free-text parent notes, etc.), by construction, ensuring Edge Case 4's "no access to external context" guarantee is structural, not a discipline the summarization logic has to remember to honor.
- `InsightsService.generate()`: assembles a summary strictly from observable pattern data (streaks, skill-mastery deltas, theme-tag frequency, usage-duration trends), calls `ContentSafetyValidator.validate()` (C.20's existing gate) on the assembled draft before returning/persisting it — this service introduces no second, parallel safety check.
- Aggregation is privacy-preserving: no raw per-event child PII surfaces in the output, only aggregated pattern descriptions.

## 11. Required API / API Contract
`POST /v1/ai/insights/generate` `{child_id, report_period}` → `200` report draft, routed through C.20's validator before being marked deliverable.

## 12. Database Requirements
No new tables — reads A.7/A.9/C.22's existing data; writes to C.20's existing report-storage schema (not owned here).

## 13. Validation
`report_period` valid date range; `child_id` existence check.

## 14. Authentication
Internal service-to-service auth (called by C.20's Report Generation Service).

## 15. Authorization
Internal call scope only.

## 16. Error Handling
`ContentSafetyValidator` rejection: the draft is not persisted as a deliverable report, propagated per C.20's existing error semantics (not reimplemented here).

## 17. Security
Zero duplicated safety-validation logic and zero external-context input path are this sub-feature's two guarantees — mandatory tests confirm (a) every generated draft passes through C.20's actual `ContentSafetyValidator.validate()` call before persistence, and (b) the repository layer has no method signature accepting any external-context parameter (support-ticket text, free-form notes, etc.).

## 18. Analytics
`ai_insight_generated` per §1.19.

## 19. Performance
Aggregation queries indexed on `(child_id, period)` across the underlying habit/mastery/engagement tables.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: pattern-aggregation logic (streaks, mastery deltas, theme frequency). Integration: **mandatory** — every generated draft is passed to C.20's `ContentSafetyValidator` before being marked deliverable, confirmed via a mock-call-assertion test; **mandatory** — structural test confirming no repository/service method in this module accepts an external-context parameter; a fixture summary correctly describes an observable pattern (e.g., "consistency dipped during this period") without any causal speculation.

## 22. Documentation
OpenAPI docstring noting this service has no external-context input surface by design, and that it reuses (never duplicates) C.20's Content Safety Validator.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define Schemas**
Objective: `InsightsGenerateRequest`, `InsightsDraft`. Files: `schemas/insights_schema.py`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `InsightsDataRepository` with No External-Context Surface**
Objective: Reads strictly from platform's own tables. Files: `repositories/insights_data_repository.py`. Dependencies: Task 01. Tests: **mandatory** — no-external-context-parameter structural test. Definition of Done: test passes.

**Task 03 — Implement `InsightsService` with Mandatory Validator Pass-Through**
Objective: Assembles draft, calls C.20's `ContentSafetyValidator.validate()` before returning. Files: `services/insights_service.py`. Dependencies: Task 02, C.20. Tests: **mandatory** — validator-called-before-persistence test. Definition of Done: test passes.

**Task 04 — Implement the Router Endpoint**
Objective: `POST /v1/ai/insights/generate`. Files: `routers/insights_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Verify Observable-Pattern-Only Summarization**
Objective: Fixture test confirming no causal speculation appears in generated summaries. Dependencies: Task 03. Tests: pattern-description-only test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero parallel safety-validation logic exists anywhere in this service. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Every draft routes through C.20's actual `ContentSafetyValidator` before persistence — mandatory test passing
- [ ] No method anywhere in this service accepts an external-context parameter — mandatory structural test passing
- [ ] Summaries describe observable patterns only, zero causal speculation
- [ ] Aggregation is privacy-preserving, no raw per-event PII in output

## 25. Definition of Done
Parent insight reports are generated from the platform's own observable data only, safety-gated entirely through C.20's existing validator, with zero risk of diagnosis, sibling comparison, or external-context speculation ever reaching a parent.
