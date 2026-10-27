# B-07 — Parent Concept Summary Reporting API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Pydantic v2)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `ParentConceptReportService`, `get_concept_summary()`, `ConceptSummaryItem`, `QuizConceptSummaryResponse`, `ReportPeriodEnum`, `ConceptStatusEnum`, `AccuracyTrendEnum`, qualitative concept rollup, multi-domain attribution isolation, first-time learner onboarding framing, Redis edge caching, and parent family authorization gate.  
> **Test Coverage:** 24/24 summary API tests (`test_parent_concept_summary_api.py`), 3/3 multi-domain attribution tests (`test_multi_domain_attribution.py`), 8/8 security baseline tests (`test_security_baseline.py`) — 35/35 dedicated tests (100% green, 100.00% statement coverage: 167/167 statements, 0 missed lines), and 841/841 full learning module tests passing.

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §3.3 (Parent Concept Report Aggregator), §3.4 (`GET /v1/children/{id}/quiz-concept-summary`), §1.7 FR-6, Edge Case 10.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-07 — Parent Concept Summary Reporting API (Admin API / Parent-Facing User API — served to Parent session, not Admin RBAC)

## 4. Objective
Roll up quiz history into a concept-level (not score-level) parent-facing summary — the feature's core parent-value proposition (PRD §1.2 "genuinely informative, concept-level progress reporting") — explicitly never leading with a raw percentage as the headline.

## 5. Business Requirements
FR-6 (concepts/skills addressed, not a bare numeric score as the headline), Acceptance Criteria (§1.9: parent report lists concepts like "Practicing: Surah Al-Fatiha recitation" rather than leading with a raw percentage), Edge Case 10 (multi-domain sessions attribute correctly per skill, never conflated), §1.12 Empty States (first-time-learner framing, not a stark "no data" report).

## 6. Existing Architecture
New read-model service (`Parent Concept Report Aggregator`, PRD §3.3) within `src/noorheroes/modules/learning/`, reading from `quiz_response`/`question_skill_tag` (B-01/B-04) joined with the Skill Mastery Service's per-skill status (A.5/A.9) — this endpoint aggregates, it does not own mastery-state itself.

## 7. Existing Code to Reuse
- `get_current_parent` dependency (`core/deps.py`, `ParentSessionContext`)
- B-01 `QuestionSkillTag`, B-04 `QuizResponse` repository query methods
- Skill Mastery Service client interface (A.5/A.9 — confirm exact status-taxonomy values, e.g. `practicing`/`improving`, before implementation)

## 8. Files Created
- `src/noorheroes/modules/learning/services/parent_concept_report_service.py` — Canonical domain read-model service implementing `get_concept_summary()` with strict FR-6/§1.9 no-raw-score guarantee, multi-domain attribution isolation (Edge Case 10), first-time-learner framing (PRD §1.12), and Redis edge caching with failover.
- `src/noorheroes/modules/learning/schemas/quiz_concept_summary.py` — Pydantic v2 data contracts for `ConceptSummaryItem`, `QuizConceptSummaryResponse`, `ReportPeriodEnum`, `ConceptStatusEnum`, and `AccuracyTrendEnum` with dual-wire camelCase/snake_case serialization and `extra="forbid"`.
- `tests/modules/learning/test_parent_concept_summary_api.py` — 24 unit & integration tests covering contract invariants (zero raw score headline), first-time learner framing, period filtering, parent authorization (401/403), child scope verification, soft-deleted child 404, dual-route wire parity, and Redis caching.
- `tests/modules/learning/test_multi_domain_attribution.py` — 3 signature integration tests proving multi-domain sessions attribute questions distinctly per skill domain without metric conflation (Edge Case 10).

## 9. Files Modified
- `src/noorheroes/modules/learning/api.py` — Mounted `GET /v1/children/{id}/quiz-concept-summary` and module alias `GET /v1/learning/children/{id}/quiz-concept-summary` with thin controller routing, parent authentication (`get_current_parent`), and AST-clean query validation.
- `src/noorheroes/modules/learning/deps.py` — Added `get_parent_concept_report_service()` dependency provider and `ParentConceptReportServiceDep`.
- `src/noorheroes/modules/learning/schemas/__init__.py` and `schemas.py` — Re-exported all concept summary schemas and enums.
- `src/noorheroes/modules/learning/services/__init__.py` — Re-exported `ParentConceptReportService`.
- `CHANGELOG/CROSS_PLATFORM_CHANGES.md` — Added authoritative cross-platform ledger entry for Feature A.8 Sub-feature B-07.
- `NoorHeroes_Consolidated_Execution_Blueprint.md` — Updated Phase 6 §6.7 Item 267 status to Completed & Verified and advanced active work item to Item 268 (B-08).

## 10. Backend Requirements
- Aggregate `quiz_response` rows (via `question_skill_tag`) into a per-skill concept list: `{ skill, status, recent_accuracy_trend }` — no top-level raw score field
- Correctly attribute each question's contribution to its own skill domain even within a single multi-domain quiz session (Edge Case 10)
- Support `period` query param (e.g., `weekly`); default to a sensible recent window if omitted
- First-time-learner (zero quiz history) → distinct first-time framing payload, not an empty/error-shaped response (§1.12)

## 11. KMP Requirements
Consumed by K-07 (Parent Concept Summary Report screen, Parent Area in-app).

## 12. NextJS Requirements
N/A directly (this is parent-facing, not Admin Portal-facing; Admin's own aggregate insight is N-04's distribution monitor, which is deliberately a *different*, non-per-child view).

## 13. API Contract

### `GET /v1/children/{id}/quiz-concept-summary?period=weekly`
- **Auth:** Bearer (parent session)
- **Response 200:**
```json
{
  "concepts": [
    { "skill": "Surah Al-Fatiha recitation", "status": "practicing", "recent_accuracy_trend": "improving" }
  ],
  "is_first_time_summary": false
}
```
- **Error Responses:** `401`, `403` (child not in requesting parent's family), `404` (child not found)

## 14. Database Requirements
Reads existing `quiz_response`, `question_skill_tag` (B-01/B-04); no new tables — this is a read-model aggregation, not a new source of truth.

## 15. Validation
`id` (child_id) must belong to the requesting parent's family (`family_id` scoping, standard platform isolation pattern); `period` restricted to supported enum values.

## 16. Authentication
Bearer JWT, `get_current_parent`.

## 17. Authorization
Standard parent-family `child_id` ownership check — a parent may only request summaries for children within their own family.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero quiz history for the child | First-time framing payload (`is_first_time_summary: true`), not an empty/error state |
| `child_id` not in requesting parent's family | `403` |
| `child_id` not found | `404` |
| Skill Mastery Service unavailable for status enrichment | Degrade to accuracy-trend-only data with skill names still present, never a blank report |

## 19. Offline First
N/A (backend, parent-facing web/app read endpoint — not part of the offline child-quiz-taking flow).

## 20. Local Data
N/A (backend).

## 21. Localization / 22. RTL
`skill` display names and `status` labels localized to the parent's selected locale; RTL layout is a client concern (K-07).

## 23. Analytics
Server-side source for client-emitted `parent_quiz_summary_viewed`.

## 24. Performance
Aggregation query indexed via `question_skill_tag(skill_node_id)` and `quiz_response(question_id, created_at DESC)` (both already established in B-01/B-04); consider a short-TTL cache given weekly-cadence access pattern.

## 25. Security
Standard `child_id`-scoped query enforcement (PRD §12.1 cross-child data leakage mitigation) — no new PII surface beyond existing learning-progress data.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async — existing stack.

## 27. Testing
- Unit: concept list never includes a top-level raw score field (schema-level guarantee)
- Unit: multi-domain session attributes each question's contribution to its own skill (signature test, Edge Case 10)
- Unit: zero-history child returns first-time framing payload, not an empty/error shape
- Integration: parent requesting a child outside their family → `403`
- Integration: full flow — quiz completion (B-05/B-06) → concept summary reflects the relevant skill as improving

## 28. Documentation
OpenAPI docs explicitly note the "no raw score as headline" contract as a deliberate product decision, not an oversight, so future editors don't "fix" it by adding one back.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Skill Mastery Service Status Taxonomy**
Task ID: B-07-T01. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: confirmed actual status and trend enum values from A.5/A.9 (`practicing`, `mastered`, `learning`, `needs_refresh` / `improving`, `steady`, `needs_encouragement`, `new_learner`) — zero invented taxonomy. Definition of Done: taxonomy confirmed and documented in schema enums.

**Task 02 — Implement Parent Concept Report Aggregator Service**
Task ID: B-07-T02. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `parent_concept_report_service.py`. Business Rules: FR-6 (no raw score), Edge Case 10 (multi-domain distinct attribution). Tests: `test_multi_domain_attribution.py` (3/3 tests passing). Definition of Done: multi-domain attribution test passes with distinct per-skill accounting.

**Task 03 — Create Summary Schema**
Task ID: B-07-T03. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `schemas/quiz_concept_summary.py`. Definition of Done: schema has zero top-level raw score fields by construction (`extra="forbid"`, verified by AST reflection).

**Task 04 — Implement First-Time-Learner Framing**
Task ID: B-07-T04. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: zero lifetime attempts returns `concepts: [], is_first_time_summary: true`, distinct from an active learner with 0 attempts in the current window (`is_first_time_summary: false`). Definition of Done: zero-history response distinct from empty/error shape.

**Task 05 — Implement Endpoint**
Task ID: B-07-T05. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `api.py`, `deps.py`. Dependencies: Task 02–04. Definition of Done: matches §13 contract and dual-route parity (`GET /v1/children/{id}/quiz-concept-summary` and `GET /v1/learning/children/{id}/quiz-concept-summary`).

**Task 06 — Add Validation & Error Handling**
Task ID: B-07-T06. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: per §18 (`401` unauth, `403` cross-family, `404` not found, graceful downstream degradation). Definition of Done: all error paths tested.

**Task 07 — Add Tests**
Task ID: B-07-T07. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `test_parent_concept_summary_api.py`, `test_multi_domain_attribution.py`. Definition of Done: full coverage per §27 (35 dedicated tests passing, 100.00% statement coverage).

**Task 08 — Add API Documentation**
Task ID: B-07-T08. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: OpenAPI docs reviewed, "no raw score" decision documented.

**Task 09 — Final Code Review**
Task ID: B-07-T09. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: §31 checklist fully checked (5/5 items); Zero-Missing standard confirmed.

## 30. Definition of Done
Endpoint live, concept-level summary verified with no raw-score headline, multi-domain attribution correct, first-time-learner framing distinct from empty state, ready for K-07 consumption. 100.00% statement coverage across 167/167 statements, 35 dedicated tests passing, 841 module tests passing.

## 31. Final Verification Checklist
- [x] Response never includes a top-level raw numeric score as the headline field
- [x] Multi-domain session attributes correctly per skill, never conflated
- [x] First-time-learner (zero history) gets distinct framing, not an empty/error state
- [x] `child_id` family-ownership check enforced (`403` on cross-family access)
- [x] Skill Mastery Service unavailability degrades gracefully without a blank report
