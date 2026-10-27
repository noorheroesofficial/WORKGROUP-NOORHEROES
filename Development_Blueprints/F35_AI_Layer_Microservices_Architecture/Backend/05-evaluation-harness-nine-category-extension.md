# B-05 — Evaluation Harness 9-Category Extension

## 1. Feature Context
The release gate every model or prompt change in this entire AI layer must clear — extending E.30's existing harness with nine independently-scored test categories, so a single critical failure (say, accent-specific pronunciation bias) can never be diluted or hidden by eight passing categories' aggregate score.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.5 Evaluation Harness 9-Category Extension (ID: **B-05**)

## 4. Objective
Extend E.30's Evaluation Harness with the nine named test categories from FR-9, each independently reporting pass/fail, never collapsed into a single aggregate score.

## 5. Business Requirements
- FR-9: maintain ongoing test suites for age appropriateness, Islamic factuality, refusal correctness, citation correctness, PII leakage, toxicity/unsafe-advice detection, multilingual consistency, pronunciation-scoring bias across accents, and recommendation diversity; release gate requires offline evaluation, reviewer sign-off for high-risk features, canary release, and a defined rollback path.
- §5 Backend AI prompt item 4 (mandatory): a single category's failure (e.g., pronunciation-scoring bias) is correctly surfaced as a release-blocking critical finding even when all 8 others pass, never averaged/aggregated into a score that could mask it.
- Edge Case 2: a religious-rulings-category (Islamic factuality) test failure is release-blocking regardless of strong aggregate metrics.
- Edge Case 6: an accent-specific pronunciation-scoring bias finding is treated as a critical finding, not lower-priority than a safety finding.

## 6. Existing Architecture
Extends E.30's existing `app/ai_safety/services/evaluation_harness_service.py` — this sub-feature is additive (new test-category definitions and independent-reporting logic), not a rewrite of E.30's harness engine.

## 7. Existing Code to Reuse
- E.30's `EvaluationHarnessService` (extended, not duplicated)
- E.30's Evaluation Harness Dashboard (consumes this sub-feature's per-category output, no new UI needed per PRD §8)

## 8. Files to Create
- `app/ai_safety/services/evaluation_categories/` — nine individual category-test-runner modules (`age_appropriateness.py`, `islamic_factuality.py`, `refusal_correctness.py`, `citation_correctness.py`, `pii_leakage.py`, `toxicity_unsafe_advice.py`, `multilingual_consistency.py`, `pronunciation_scoring_bias.py`, `recommendation_diversity.py`)
- `app/ai_safety/schemas/evaluation_category_result_schema.py` — `CategoryResult { category_name, status: 'pass'|'fail', details }`, never a merged score

## 9. Files to Modify
- `app/ai_safety/services/evaluation_harness_service.py` — extend `run_evaluation()` to invoke all nine category runners and collect their results as an array of independent `CategoryResult` objects, never averaged into one number; extend the release-gate decision logic to block on ANY single `status='fail'`, regardless of the other eight results

## 10. Backend Requirements
- Each category runner is an independently invokable module implementing a common `run(model_version) -> CategoryResult` interface — this uniformity ensures no category can be silently skipped or its result silently merged into another's.
- `EvaluationHarnessService.run_evaluation()`: invokes all nine runners, collects results into `evaluation_run.category_results: list[CategoryResult]` (a JSON array field or a related table, never a single scalar score column) — the release-gate decision (`ReleaseGateDecision.decide()`) iterates this list and blocks if ANY entry has `status='fail'`.
- `pronunciation_scoring_bias.py` runner: evaluates scoring consistency across multiple recorded accent/dialect fixture sets, flagging any statistically significant disadvantage for a specific regional variant as `status='fail'`.
- `islamic_factuality.py` runner: evaluates model output against the approved corpus specifically for religious-rulings-category test cases, at the same elevated confidence bar as B-03's Learning Service.

## 11. Required API / API Contract
Extends E.30's existing `POST /v1/ai/evaluation-runs` / `GET /v1/ai/evaluation-runs/{id}` — response now includes `category_results: [{category_name, status, details}, ...]` for all nine categories, never a single aggregate score field.

## 12. Database Requirements
Extends E.30's `evaluation_run` table (or a related `evaluation_category_result` child table) to store per-category results as discrete rows/entries rather than a single scalar.

## 13. Validation
All nine categories must report a result for every evaluation run — a missing category result is itself treated as a run-completion failure (not silently treated as "passing by omission").

## 14. Authentication
Internal/CI-triggered; consumed by E.30's existing admin-facing dashboard under its own auth.

## 15. Authorization
Inherits E.30's existing scope gating for evaluation-run visibility/triggering.

## 16. Error Handling
A missing/incomplete category result blocks the release gate just as a `status='fail'` would — an evaluation run is never considered "passing" with an incomplete category set.

## 17. Security
Independent, non-aggregated per-category reporting is this sub-feature's single highest-priority guarantee alongside B-02/B-03 — mandatory test confirms a fixture run with 8 passing categories and exactly 1 failing category (pronunciation-scoring bias) is correctly surfaced as release-blocking, and that no code path in `ReleaseGateDecision.decide()` computes or relies on any averaged/aggregate score across the nine results.

## 18. Analytics
`ai_evaluation_suite_run_completed` (shared event type with E.30), `ai_release_gate_passed`/`ai_release_gate_blocked` (shared with E.30) per §1.19.

## 19. Performance
Category runners execute independently (parallelizable); overall run duration bounded by the slowest single category, not the sum, where infrastructure supports concurrent execution.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries (reuses E.30's evaluation infrastructure).

## 21. Testing
Unit: each of the nine category runners' pass/fail determination logic. Integration: **mandatory** — 8-pass-1-fail fixture run correctly blocks the release gate, with the specific failing category identified in the response, never masked by aggregate scoring; **mandatory** — a missing category result (e.g., a runner that errors before completing) is treated as a gate-blocking condition, not silently omitted; religious-rulings (Islamic factuality) category failure blocks regardless of the other eight categories' strength (Edge Case 2); accent-bias (pronunciation-scoring) category failure treated with equal severity to a safety-category failure (Edge Case 6).

## 22. Documentation
Docstring on `CategoryResult`/`ReleaseGateDecision` explicitly stating no aggregate/averaged score exists anywhere in the release-gate decision path.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define `CategoryResult` Schema**
Objective: Independent per-category result shape, no scalar aggregate field anywhere. Files: `schemas/evaluation_category_result_schema.py`. Tests: schema validation. Definition of Done: schema used by Task 02.

**Task 02 — Implement the Nine Category Runner Modules**
Objective: Each implementing the common `run(model_version) -> CategoryResult` interface. Files: `services/evaluation_categories/*.py` (9 files). Dependencies: Task 01. Tests: per-runner pass/fail-determination tests. Definition of Done: all nine tests pass.

**Task 03 — Extend `EvaluationHarnessService.run_evaluation()`**
Objective: Invoke all nine runners, collect into an independent-results array. Files: `services/evaluation_harness_service.py` (extended). Dependencies: Task 02. Tests: all-nine-invoked-and-collected test. Definition of Done: test passes.

**Task 04 — Extend `ReleaseGateDecision.decide()` for Any-Single-Failure Blocking**
Objective: Block on ANY `status='fail'`, no averaging anywhere in the decision path. Dependencies: Task 03. Tests: **mandatory** — 8-pass-1-fail fixture blocks correctly. Definition of Done: test passes.

**Task 05 — Implement Missing-Category-Result Handling**
Objective: Incomplete category set treated as gate-blocking. Dependencies: Task 04. Tests: **mandatory** — missing-category-blocks test. Definition of Done: test passes.

**Task 06 — Verify Religious-Rulings and Accent-Bias Equal-Severity Handling**
Objective: Confirm Edge Cases 2 and 6 hold. Dependencies: Task 04. Tests: both edge-case fixture tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero averaging/aggregation logic exists anywhere in `ReleaseGateDecision`. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] All nine categories independently report pass/fail, zero aggregate scoring anywhere — mandatory 8-pass-1-fail test passing
- [ ] A missing category result blocks the release gate, never silently passes — mandatory test passing
- [ ] Religious-rulings-category (Islamic factuality) failure blocks regardless of other categories' strength
- [ ] Accent-bias (pronunciation-scoring) failure treated with equal severity to safety-category failures

## 25. Definition of Done
Every model/prompt change is gated by nine genuinely independent, non-maskable evaluation categories — no single critical failure can ever be diluted by strong performance elsewhere.
