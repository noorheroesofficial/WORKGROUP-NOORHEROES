# B-08 — Cross-Domain Parent Mastery Summary API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Endpoints Delivered:** `GET /v1/children/{id}/mastery-summary`, `GET /v1/learning/children/{id}/mastery-summary` (Canonical & Module Alias)  
> **Schemas Delivered:** `MasterySummaryResponse`, `DomainSummarySection`, `SkillSummaryItem`, `MasteryTrendEnum`, `PARENT_MASTERY_SUMMARY_RESPONSES` in `src/noorheroes/modules/learning/schemas/parent_mastery_summary.py`  
> **Service Layer:** `ParentMasterySummaryService.get_mastery_summary()`, `compute_skill_mastery_trend()` in `src/noorheroes/modules/learning/services/parent_mastery_summary_service.py` with multi-tenant child scope check, active domain validation, batch trend derivation, and 120s Redis caching with live DB fallback  
> **Parent-Reporting Invariant (FR-11 & FR-3):** Strict structural continuous score, percentage, and formula version omission enforced via mandatory CI reflection gate (`test_no_raw_score_schema_introspection.py`)  
> **Multi-Language Localization:** Formats multi-domain rollup copy and trend descriptors across `en`, `hi`, `ur`, and `ar` with native script formatting via `src/noorheroes/core/i18n.py`  
> **Test Coverage:** 100% Green across 41 dedicated B-08 tests (`test_parent_mastery_summary_service.py` [19], `test_parent_mastery_summary_api.py` [13], `test_no_raw_score_schema_introspection.py` [9]), and 123 total learning context tests.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Gives parents one endpoint that rolls up concept-level mastery progress across every domain a child engages with (Quran, Arabic, Tajweed today; any future domain automatically), rather than requiring a separate report per domain.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-08 — Cross-Domain Parent Mastery Summary API (Parent API)

## 4. Objective
Implement `GET /v1/children/{id}/mastery-summary?domain=`, returning concept-level summaries (skill labels + state + trend) with an optional `domain` filter, and a true cross-domain rollup when the filter is omitted — never exposing a single raw aggregate score as the headline metric.

## 5. Business Requirements
- FR-11: Domain-agnostic Parent Report contract — concept-level summaries, never a single raw aggregate score as the headline metric.
- User Story: "As a parent, I want every learning domain in the app to report progress in the same consistent, trustworthy way."
- Consistent with A.5 FR-17 / A.6 / A.8 §3.4's shared parent-reporting principle.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. `learning` bounded context. A.5 already has `08-parent-learning-progress-report-api.md` (domain-specific report) and A.8 has `07-parent-concept-summary-reporting-api.md` (quiz-level reporting) — this sub-feature is the cross-domain aggregation layer sitting above both, per the PRD's explicit framing of this as new/generalized work, not a duplicate of either.

## 7. Existing Code to Reuse
- Parent-session auth dependency (`get_current_parent` or equivalent, mirroring `get_current_child`'s pattern).
- A.5 B-08's concept-level reporting shape/philosophy (reused as the per-domain building block this endpoint aggregates, not reimplemented).
- B-05's `skill_node_state` query patterns (extended for cross-domain aggregation).

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/parent_mastery_summary.py` — `MasterySummaryResponse`, `DomainSummarySection`.
- `src/noorheroes/modules/learning/services/parent_mastery_summary_service.py` — `ParentMasterySummaryService(BaseService)`.
- `tests/modules/learning/test_parent_mastery_summary_service.py`
- `tests/modules/learning/test_parent_mastery_summary_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `GET /v1/children/{id}/mastery-summary` route (likely under a parent-facing router prefix, e.g. `/v1/children/` consistent with existing parent-area endpoint conventions).

## 10. Backend Requirements
- **Router:** `GET /v1/children/{id}/mastery-summary?domain=`, Bearer (parent session), `id` (child) must belong to the authenticated parent's family.
- **Aggregation logic:** when `domain` is omitted, query `skill_node_state` across ALL registered domains (via B-01's registry) for the child, group by domain, and return a `DomainSummarySection` per domain plus an overall qualitative rollup (e.g., "making steady progress across Quran and Arabic," never "68% average mastery").
- **Trend computation:** derive a simple qualitative trend (`improving`/`steady`/`needs_attention`) per skill or domain from recent `mastery_evidence_log` activity, not a numeric delta exposed raw.
- **Never expose raw score:** identical structural guarantee to B-05 — response schema has no numeric mastery/confidence field.

## 11. KMP Requirements
Consumed by K-06 (Cross-Domain Parent Mastery Summary screen, Parent Area).

## 12. NextJS Requirements
N/A directly (this is the in-app Parent Area's data source, not an Admin Portal feature; Admin's read-only visibility into aggregate patterns is a distinct concern owned by N-05).

## 13. API Contract

**`GET /v1/children/{id}/mastery-summary?domain={optional}`**
- **Auth:** Bearer (parent session)
- **Response 200:**
```json
{
  "child_id": "uuid",
  "domains": [
    {
      "domain": "quran",
      "skills": [
        { "skill_node_id": "uuid", "label": "Surah Al-Fatiha", "state": "mastered", "trend": "steady" }
      ]
    }
  ]
}
```
- **Authentication:** Bearer JWT, parent-session scope.
- **Authorization:** `{id}` (child) must belong to the authenticated parent's family.
- **Validation:** `domain` (if present) must be registered/active.
- **Error Responses:** `401`, `403` (child not in parent's family), `422` (invalid domain filter), `500`.

## 14. Database Requirements
Reads `skill_node_state`, `mastery_evidence_log`, `skill_node` (for `label`/domain metadata) — no new tables.

## 15. Validation
- `{id}` must resolve to an active child in the caller's family.
- `domain` filter (if provided) validated against `SkillDomainService`.
- Child with zero evidence in any domain returns an appropriate empty/default structure, not an error.

## 16. Authentication
Bearer JWT, parent-session scope (distinct dependency from `get_current_child` — do not reuse the child-session guard here).

## 17. Authorization
`{id}` must belong to the authenticated parent's family; reject cross-family access as `403` without leaking existence via a different error code.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Child has zero evidence in a domain | That domain's `skills` array is empty or the domain is simply omitted from `domains` — not an error |
| Parent requests a child not in their family | `403` |
| Invalid `domain` filter | `422` |
| DB failure | `500`, generic error body, correlation-ID logged |

## 19. Offline First
N/A (backend). Client-side K-06 may cache last-fetched summary for offline viewing.

## 20. Local Data
N/A (backend).

## 21. Localization
`label` and trend descriptors must be localized (EN/HI/AR/UR) via the existing `localization` context content-key pattern, consistent with A.5/A.8's parent-reporting localization approach.

## 22. RTL
N/A (backend; layout owned by K-06).

## 23. Analytics
`cross_domain_mastery_summary_viewed` fired client-side (K-06) on successful load.

## 24. Performance
Aggregation query across domains must remain efficient as domain count grows — index `(child_id, state)` on `skill_node_state` already supports this; avoid N+1 queries per domain (single query grouped in application code or a single grouped SQL query, not one query per domain).

## 25. Security
Parent-session scoping is the primary control; no raw score exposure (same structural guarantee as B-05).

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: aggregation grouping logic, trend derivation.
- Integration: cross-family rejection, empty-domain handling, multi-domain rollup correctness.
- Schema introspection: extend B-05's no-raw-score test to cover this response model too (Cross-Cutting API Concern, A.9 PRD §3.5 — "every child-facing AND parent-facing response schema").

## 28. Documentation
OpenAPI schema; note in parent-area documentation that this supersedes/complements A.5's domain-specific report as the cross-domain entry point.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement ParentMasterySummaryService Aggregation** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-08-T01
- Objective: Cross-domain grouping/aggregation logic.
- Why This Is Required: Core deliverable of this sub-feature — a true single-call cross-domain view.
- Existing Architecture to Follow: `BaseService` pattern.
- Existing Files to Reuse: B-01's `SkillDomainService`, B-05's query patterns.
- Files to Create: `services/parent_mastery_summary_service.py`.
- Files to Modify: None.
- Implementation Details: Single grouped query across `skill_node_state`/`skill_node` for the child, optionally filtered by `domain`, grouped into `DomainSummarySection` list; trend derived from recent `mastery_evidence_log` activity per skill.
- Business Rules: Never surface a raw numeric aggregate as the headline value.
- Validation: Per §15. Error Handling: Per §18.
- Security: Parent-family scoping. Performance: Single grouped query, no N+1.
- Localization: Content-key resolution for labels/trends. RTL: N/A (delegated).
- Analytics: N/A (client-fired).
- Tests: `test_parent_mastery_summary_service.py`.
- Documentation: Docstring.
- Dependencies: B-01, B-05.
- Do Not Change: A.5's existing domain-specific report endpoint (this is additive, not a replacement).
- Expected Result: Working aggregation service.
- Definition of Done: Unit tests green including multi-domain and empty-domain cases.

**Task 02 — Implement GET /v1/children/{id}/mastery-summary Router** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-08-T02
- Objective: Wire the parent-facing endpoint.
- Why This Is Required: Directly backs K-06.
- Existing Architecture to Follow: Router → Service → Repository; parent-session auth dependency.
- Existing Files to Reuse: Parent-session guard (existing pattern from Parent Area endpoints elsewhere in the platform).
- Files to Create: `schemas/parent_mastery_summary.py`.
- Files to Modify: `api.py`.
- Implementation Details: Standard router wiring calling Task 01's service.
- Business Rules: Per §10. Validation: Per §15. Error Handling: Per §18.
- Security: Family-scoped authorization enforced.
- Performance: Per §24. Localization: Delegated to service. RTL: N/A. Analytics: N/A.
- Tests: `test_parent_mastery_summary_api.py`.
- Documentation: OpenAPI schema.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working endpoint.
- Definition of Done: Integration tests green.

**Task 03 — Extend No-Raw-Score Schema Introspection to Parent-Facing Models** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-08-T03
- Objective: Ensure the parent-facing response is covered by the same structural guarantee as child-facing responses.
- Why This Is Required: A.9 PRD §3.5 explicitly states this covers "every child-facing AND even parent-facing response schema."
- Existing Architecture to Follow: B-05's introspection test, extended.
- Existing Files to Reuse: `test_no_raw_score_schema_introspection.py` (from B-05) — extend its model-registry scope to include this endpoint's response model rather than writing a parallel test.
- Files to Create: None (extend existing file).
- Files to Modify: `tests/modules/learning/test_no_raw_score_schema_introspection.py`.
- Implementation Details: Add `MasterySummaryResponse`/`DomainSummarySection` to the set of models the introspection sweep covers.
- Business Rules: N/A. Validation/Error Handling/Security: this IS the control. Performance: N/A. Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: This task IS the test extension.
- Documentation: Update test docstring's model-coverage list.
- Dependencies: Task 02, B-05.
- Do Not Change: N/A.
- Expected Result: Full coverage across child- and parent-facing schemas.
- Definition of Done: Extended introspection test green.

## 30. Definition of Done
`GET /v1/children/{id}/mastery-summary` live, correctly aggregating across all registered domains (or filtering to one), returning localized concept-level summaries with no raw score exposure, covered by the shared schema-introspection guarantee.

## 31. Final Verification Checklist
- [x] Cross-domain rollup correct when `domain` omitted
- [x] Single-domain filter correct when provided
- [x] Parent-family authorization enforced (403 on mismatch)
- [x] No raw score field in response (introspection test extended and green)
- [x] Localized labels/trends (EN/HI/AR/UR)
- [x] No N+1 query pattern across domains
- [x] Empty-domain/zero-evidence case handled gracefully

## 32. Verification Evidence & Test Results
- **Dedicated B-08 Suite (`test_parent_mastery_summary_service.py`, `test_parent_mastery_summary_api.py`, `test_no_raw_score_schema_introspection.py`)**: 41 passed in 2.17s (100% green).
  - Unit Service & Trend Calculation Suite: 19 passed in 0.45s.
  - Integration API Route Suite: 13 passed in 0.40s.
  - Mandatory FR-3 / FR-11 CI Schema & Wire Introspection Gate: 9 passed in 0.15s.
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 123 passed in 3.35s (100% green, 0 regressions across B-01 through B-08).
- **Dual-Wire Wire Serialization & OpenApi Contract**: Guaranteed zero continuous float scores, percentages, or formula versions leaked over the wire or in documentation schemas.
- **Multilingual Support**: Fully localized in English, Hindi, Urdu, and Arabic with authentic native-script formatting.

